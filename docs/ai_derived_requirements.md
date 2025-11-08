# Software Requirements Specification: Natural Language to SQL API

**Note:** This document was automatically derived (reverse-engineered) using AI based on the app's codebase.

## 1. High-Level Summary

This application is a REST API service that translates natural language questions into SQL queries. It uses the AWS Bedrock service (specifically, the Anthropic Claude model) to generate a SQL statement from a user's question. The generated SQL is then executed against a local SQLite database, and the results are returned to the user in JSON format.

## 2. Technologies Used

*   **Languages:** Python
*   **Frameworks/Libraries:**
    *   Flask: For creating the REST API server.
    *   boto3: AWS SDK for Python, used to interact with AWS Bedrock.
    *   sqlite3: For interacting with the local SQLite database.
*   **Database:** SQLite
*   **Platforms/Infrastructure:** AWS Bedrock

## 3. Functional Requirements

### 3.1. User Roles

A single user role is implied: an API client or developer who can send requests to the service.

### 3.2. Feature: Natural Language Query Processing

*   **FR-1.1:** The system **shall** expose a `/query` endpoint that accepts HTTP POST requests.
*   **FR-1.2:** The system **shall** expect a JSON payload in the POST request body containing a `question` field (e.g., `{"question": "how many customers are there?"}`).
*   **FR-1.3:** The system **shall** return a 400 Bad Request error if the `question` field is not provided in the request body.
*   **FR-1.4:** The system **shall** construct a detailed prompt for an AI model by combining predefined instructions, the database schema, and the user's question.
*   **FR-1.5:** The system **shall** send the constructed prompt to the AWS Bedrock Anthropic Claude Haiku model for processing.
*   **FR-1.6:** The system **shall** receive a single SQL query string in response from the AI model.
*   **FR-1.7:** The system **shall** execute the received SQL query against the `orders.db` SQLite database.
*   **FR-1.8:** The system **shall** return the query results as a JSON object, including a list of column names and a list of rows.
*   **FR-1.9:** The system **shall** return a JSON object with an `error` key if the SQL query execution fails.

## 4. Non-Functional Requirements

*   **NFR-1 (Security):** The system **shall** rely on standard AWS authentication mechanisms (e.g., IAM roles, environment variables for credentials) via the `boto3` library to securely connect to the AWS Bedrock service.
*   **NFR-2 (Reliability):** The system **shall** handle and log errors that occur during the invocation of the AI model.
*   **NFR-3 (Reliability):** The system **shall** gracefully handle SQL errors during database query execution and return a descriptive error message in the API response.
*   **NFR-4 (Maintainability):** The system **shall** be configured through constants defined at the top of the main service file (`restapi_service.py`), including the database file name and prompt instruction file paths.
*   **NFR-5 (Deployment):** The system **shall** run as a development server on port 5005 by default. For production, a WSGI server is required.

## 5. Data Model

The application uses a relational data model stored in a SQLite database with the following schema:

### 5.1. customers

*   `id`: (INTEGER, Primary Key, The unique identifier for a customer)
*   `name`: (VARCHAR(255), The name of the customer)
*   `email`: (VARCHAR(255), The email address of the customer)

### 5.2. products

*   `id`: (INTEGER, Primary Key, The unique identifier for a product)
*   `name`: (VARCHAR(255), The name of the product)
*   `price`: (DECIMAL(10, 2), The price of the product)

### 5.3. orders

*   `id`: (INTEGER, Primary Key, The unique identifier for an order)
*   `customer_id`: (INTEGER, Foreign Key, References `customers.id`)
*   `product_id`: (INTEGER, Foreign Key, References `products.id`)
*   `order_date`: (DATE, The date the order was placed)
*   **Relations:**
    *   Has a many-to-one relationship with `customers` via `customer_id`.
    *   Has a many-to-one relationship with `products` via `product_id`.

## 6. External Dependencies

*   **AWS Bedrock (Anthropic Claude Haiku model):** Used as the core engine for translating natural language questions into SQL queries. The application sends a prompt and receives a SQL statement.
