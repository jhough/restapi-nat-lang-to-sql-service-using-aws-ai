
import json
import sqlite3
from flask import Flask, request, jsonify

import boto3
import json
from botocore.exceptions import ClientError

# Configuration
DB_FILE = "orders.db"
PORT = 5005
PROMPT_INSTRUCTIONS_FILE = "natlang_to_sql_prompt_instructions.md"
DB_SCHEMA_FILE = "database_schema.sql"

app = Flask(__name__)


def invoke_model(prompt):

    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Claude 3 Haiku.
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    # Format the request payload using the model's native structure.
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]
#    print(response_text)

    return response_text


def get_prompt_template():
    with open(PROMPT_INSTRUCTIONS_FILE, "r") as f:
        instructions = f.read()
    with open(DB_SCHEMA_FILE, "r") as f:
        schema = f.read()
    return f"{instructions}\n\nDatabase Schema:\n{schema}\n\nQuestion: {{question}}"


def query_database(sql_query):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        return {"columns": columns, "rows": rows}
    except sqlite3.Error as e:
        return {"error": str(e)}


@app.route("/query", methods=["POST"])
def handle_query():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Question not provided"}), 400

    question = data["question"]
    prompt_template = get_prompt_template()
    prompt = prompt_template.format(question=question)


    # call the Bedrock model
    sql_query = invoke_model(prompt)


    if not sql_query:
        return jsonify({"error": "Failed to generate SQL query"}), 500

    # Execute the query
    query_result = query_database(sql_query)
    return jsonify(query_result)


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
