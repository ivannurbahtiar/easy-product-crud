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
            
        if not product_id or not event.get('body'):
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing ID or request body'})
            }
            
        data = json.loads(event['body'])
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Build dynamic query
        updates = []
        params = []
        if name is not None:
            updates.append("name = %s")
            params.append(name)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if price is not None:
            updates.append("price = %s")
            params.append(price)
            
        if not updates:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'No fields to update'})
            }
            
        params.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s RETURNING *"
        
        logger.info(f"Updating product ID {product_id} with query: {query}")
        cur.execute(query, tuple(params))
        updated_item = cur.fetchone()
        
        if not updated_item:
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
            'body': json.dumps(updated_item, default=str)
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
