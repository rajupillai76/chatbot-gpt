OPENAI_API_KEY='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'
SQL_CONNECTION='postgresql+psycopg2://postgres:password1!@localhost:5432/postgres'

SQL_EXECUTION_MATCH = [
    ['date'], 
    ['sql'], 
    ['query'], 
    ['customer', 'name'],
    ['reservation', 'confirmation'],
    ['payment', 'status'],
    ['transaction', 'date']

]


JIRA_MATCH_TO_OPEN_TICKET = [
    ['I\'m sorry', 'couldn\'t find any relevant information', 'you please provide'],
    ['I\'m sorry', 'cannot provide an answer'],
    ['I\'m sorry', 'I am not able to reset'],
    ['I\'m sorry', 'but cannot answer'],
    ['I\'m sorry', 'I don\'t have the capability','would need to contact the appropriate'],
    ['I\'m sorry', 'I don\'t have enough information', 'you please provide more context'],
    ['There is no information provided in the context'],
    ['does not provide any information'],
    ['There is no information in the given context'],
    ['I\'m sorry','no relevant information']
]
JIRA_QUESTION_MESSAGE='I\'m sorry, but based on the given context information, I cannot provide an answer to your query "{0}". <b style="color: coral;">Would you like to open a ticket?</b>'
JIRA_YES_ANSWER=['yes', 'si', 'sim', 'of course', 'sure', 'why not', 'ok']
JIRA_ASK_DETAILS=['Great, one more thing, give a brief description']
JIRA_TICKET_GENERATED='Ticket created successfully, Ticket number: <a href="{0}"> {0} </a>'
JIRA_TICKET_NOT_GENERATED='The Ticket could not be created. Please try again later'
JIRA_TICKET_ACTION_CANCELED='Alright I will not create the ticket'
