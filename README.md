# Python REST API Natural Language to SQL App - Using AWS Bedrock with Anthropic Claude LLM

This is a Proof of Concept REST API app that accepts a natural language question, uses AI to generate a SQL query statement from the question, and queries a local database for the results.

Author: Jim Hough

- [Requirements (AI reverse-engineered)](docs/ai_derived_requirements.md)
- [Architecture Design (AI reverse-engineered)](docs/ai_derived_architecture.md)

## Python packages required (imports)

* Flask
* boto3
* sqlite3

To install the packages listed in the requirements.txt file, run the following command in your terminal:

`pip install -r requirements.txt`

This command tells pip (the Python package installer) to read the requirements.txt file and install all the packages listed in it.

## Create local SQLite database

`python create_db.py`

This will create a database file named, `orders.db`, if it does not exist. It will execute the schema (database_schema.sql) to create the tables. It will insert some sample data.

## Usage

To call the API with a question:

1. Run the REST API app:

`python restapi_service.py`

You should see output like this:

```bash
 * Serving Flask app 'restapi_service'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5005
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 630-388-349
```

2. In a separate terminal, use the following curl command to send a question to the API:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "how many customers do we have?"}' \
  http://127.0.0.1:5005/query
```

Replace "how many customers do we have?" with your own natural language question.


## FYI: This is the prompt used to create the initial version of this application

```
# Persona:
You are an expert Python software engineer.

# Task:
Create the code for a Python REST API service. The service is run by starting a command from the command line. The service accepts a natural language question and returns the results from a database.

# Instructions:
* Accept a natural language question as input.
* Then make an LLM prompt by combining the content from a file named natlang_to_sql_prompt_instructions.md and a file named database_schema.sql and the question.
* Send this prompt to the AWS Bedrock Anthropic Claude API.
* Receive a SQL query statement back from the API call.
* Use the SQL to query a local SQLite database file named orders.db.
* Return the results of that query in JSON format.
* Make this service run on port 5005.
```