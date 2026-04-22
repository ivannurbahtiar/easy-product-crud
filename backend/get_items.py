import json
import os
import psycopg2
import logging
from psycopg2.extras import RealDictCursor

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_connection():
    """Establishes a connection to the PostgreSQL database using environment variables."""
    try:
        return psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            port=os.environ.get('DB_PORT', '5432'),
            connect_timeout=5
        )
    except KeyError as e:
        logger.error(f"Missing environment variable: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

def lambda_handler(event, context):
    logger.info(f"Event: {json.dumps(event)}")
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Check if ID is provided in pathParameters (API Gateway Proxy)
        product_id = event.get('pathParameters', {}).get('id') if event.get('pathParameters') else None
            
        if product_id:
            logger.info(f"Fetching product with ID: {product_id}")
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            result = cur.fetchone()
            if not result:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({'error': 'Product not found'})
                }
        else:
            logger.info("Fetching all products")
            cur.execute("SELECT * FROM products ORDER BY id ASC")
            result = cur.fetchall()
            
        cur.close()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result, default=str)
        }
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'Internal Server Error', 'details': str(e)})
        }
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")
