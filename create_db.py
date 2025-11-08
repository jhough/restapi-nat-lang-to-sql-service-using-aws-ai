
import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('orders.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Read the schema from the .sql file
with open('database_schema.sql', 'r') as f:
    schema = f.read()

# Execute the schema to create the tables
cursor.executescript(schema)

# Insert some sample data
cursor.execute("INSERT INTO customers (id, name, email) VALUES (1, 'John Doe', 'john.doe@example.com')")
cursor.execute("INSERT INTO customers (id, name, email) VALUES (2, 'Jane Smith', 'jane.smith@example.com')")
cursor.execute("INSERT INTO customers (id, name, email) VALUES (3, 'Peter Jones', 'peter.jones@example.com')")
cursor.execute("INSERT INTO customers (id, name, email) VALUES (4, 'Susan Miller', 'susan.miller@example.com')")
cursor.execute("INSERT INTO customers (id, name, email) VALUES (5, 'Chris Green', 'chris.green@example.com')")


cursor.execute("INSERT INTO products (id, name, price) VALUES (1, 'Laptop', 1200.00)")
cursor.execute("INSERT INTO products (id, name, price) VALUES (2, 'Mouse', 25.00)")
cursor.execute("INSERT INTO products (id, name, price) VALUES (3, 'Keyboard', 75.00)")
cursor.execute("INSERT INTO products (id, name, price) VALUES (4, 'Monitor', 300.00)")
cursor.execute("INSERT INTO products (id, name, price) VALUES (5, 'Webcam', 50.00)")


cursor.execute("INSERT INTO orders (id, customer_id, product_id, order_date) VALUES (1, 1, 1, '2023-01-15')")
cursor.execute("INSERT INTO orders (id, customer_id, product_id, order_date) VALUES (2, 1, 2, '2023-01-15')")
cursor.execute("INSERT INTO orders (id, customer_id, product_id, order_date) VALUES (3, 2, 3, '2023-01-16')")
cursor.execute("INSERT INTO orders (id, customer_id, product_id, order_date) VALUES (4, 3, 4, '2023-01-17')")
cursor.execute("INSERT INTO orders (id, customer_id, product_id, order_date) VALUES (5, 4, 5, '2023-01-18')")
cursor.execute("INSERT INTO orders (id, customer_id, product_id, order_date) VALUES (6, 5, 1, '2023-01-19')")
cursor.execute("INSERT INTO orders (id, customer_id, product_id, order_date) VALUES (7, 3, 2, '2023-01-20')")
cursor.execute("INSERT INTO orders (id, customer_id, product_id, order_date) VALUES (8, 4, 3, '2023-01-21')")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database 'orders.db' created and populated with sample data.")
