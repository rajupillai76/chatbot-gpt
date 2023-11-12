# chatbot-gpt

This chatbot-gpt python code enables you to run a AI powered NLP chatbot that can analyze documents in a folder and answer any questions. The chatbot can also connect to
a postgres database and query tables. 
If the chatbot is not able to answer,then it will offer to open a JIRA ticket. 

What you need 

### Python Libraries
1. openai==0.28.1
2. PyPDF==3.17.0
3. langchain==0.0.330
4. llama-index==0.8.59
5. gradio==4.1.1
6. sqlalchemy==2.0.23
7. psycopg2


### Postgres 
1. Database
2. tables

### JIRA
1. API connecivity to open ticket 

### OpenAI / ChatGPT 
1. API key

### Questions you can ask 

1. How do I make a payment ?
2. How many transactions are available ?  - based on the keywords you have specified on the SQL_EXECUTION_MATCH in the constants.py it will go query the database. 
