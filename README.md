# Aether Serverless CRUD (AWS Lambda + PostgreSQL)

A high-performance, premium serverless CRUD system utilizing AWS Lambda (Python 3.12) and PostgreSQL. This project features a state-of-the-art "Neural Nexus" dashboard for cloud entity management.

## 📁 Project Structure

```text
.
├── backend/            # AWS Lambda source code (Python 3.12)
│   ├── get_items.py    # Handler for GET /products & GET /products/{id}
│   ├── create_item.py  # Handler for POST /products
│   ├── update_item.py  # Handler for PUT /products/{id}
│   └── delete_item.py  # Handler for DELETE /products/{id}
├── database/           # Database scripts
│   ├── schema.sql      # Database table initialization
│   └── seed.sql        # Sample data for testing
└── frontend/           # Ultra-premium web dashboard
    └── index.html      # "Aether" Dashboard interface
```

## 🌐 API Reference

| Method | Endpoint | Lambda Source | Description | Body (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/products` | `get_items.py` | Retrieves all inventory products | N/A |
| **GET** | `/products/{id}` | `get_items.py` | Retrieves a specific product by ID | N/A |
| **POST** | `/products` | `create_item.py` | Creates a new product entity | `{ "name": "...", "description": "...", "price": 0.0 }` |
| **PUT** | `/products/{id}` | `update_item.py` | Updates an existing entity | `{ "name": "...", "description": "...", "price": 0.0 }` |
| **DELETE** | `/products/{id}` | `delete_item.py` | Purges an entity from the cluster | N/A |

## ⚙️ Lambda Environment Variables

The following environment variables **must** be configured in every Lambda function under *Configuration > Environment variables*:

| Variable | Required | Description | Example |
| :--- | :--- | :--- | :--- |
| `DB_HOST` | **Yes** | PostgreSQL endpoint/host address | `xxxx.xxxx.us-east-1.rds.amazonaws.com` |
| `DB_NAME` | **Yes** | Target database name | `postgres` |
| `DB_USER` | **Yes** | Database username | `admin` |
| `DB_PASSWORD` | **Yes** | Database password | `your_secret_password` |
| `DB_PORT` | No | PostgreSQL port (Default: 5432) | `5432` |

## 🚀 Deployment Guide

### 1. Database Setup
Execute the scripts in the `/database` folder on your PostgreSQL instance (RDS, Aurora, or local).
- First: `schema.sql`
- Second: `seed.sql`

### 2. AWS Lambda Setup
- Create 4 Lambda functions with **Python 3.12** runtime.
- **Critical**: Add a **Lambda Layer** containing `psycopg2` (e.g., Klayers or internal layers).
- Configure the environment variables as shown above.
- Ensure the Lambda IAM role has proper VPC or Network access to your DB.

### 3. API Gateway Integration
- Create a **REST API** (or HTTP API).
- Configure proxy resources or specific routes matching the API table above.
- **Enable CORS**: This is vital for the frontend to communicate with the API.

### 4. Dashboard Usage
1. Open `frontend/index.html` in any modern browser.
2. Enter your API Gateway **Prod** URL in the bridge input.
3. Click **Sync Node** to establish a neural connection to your database.

---
*Created with ❤️ for Advanced Cloud Management.*
