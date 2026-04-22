import json
import os
import psycopg2
import logging
from psycopg2.extras import RealDictCursor

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_connection():
    try:
        return psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            port=os.environ.get('DB_PORT', '5432'),
            connect_timeout=5
        )
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

def lambda_handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    conn = None
    try:
        product_id = event.get('pathParameters', {}).get('id') if event.get('pathParameters') else None
            
        if not product_id:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing ID'})
            }
            
        conn = get_connection()
        cur = conn.cursor()
        
        logger.info(f"Deleting product ID: {product_id}")
        cur.execute("DELETE FROM products WHERE id = %s RETURNING id", (product_id,))
        deleted_id = cur.fetchone()
        
        if not deleted_id:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Product not found'})
            }
            
        conn.commit()
        cur.close()
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'message': f'Product {product_id} deleted successfully'})
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")
