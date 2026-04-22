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
        if not event.get('body'):
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Missing request body'})
            }
            
        data = json.loads(event['body'])
        name = data.get('name')
        description = data.get('description', '')
        price = data.get('price', 0.0)
        
        if not name:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Name is required'})
            }
            
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        logger.info(f"Inserting product: {name}")
        cur.execute(
            "INSERT INTO products (name, description, price) VALUES (%s, %s, %s) RETURNING *",
            (name, description, price)
        )
        
        new_item = cur.fetchone()
        conn.commit()
        cur.close()
        
        return {
            'statusCode': 201,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps(new_item, default=str)
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
