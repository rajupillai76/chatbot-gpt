
from .constants import JIRA_MATCH_TO_OPEN_TICKET, JIRA_QUESTION_MESSAGE, JIRA_YES_ANSWER, \
    JIRA_ASK_DETAILS,JIRA_TICKET_GENERATED, JIRA_TICKET_NOT_GENERATED,JIRA_TICKET_ACTION_CANCELED, SQL_EXECUTION_MATCH
from .jira import Jira

jiraObj = Jira()

def check_response_if_jt_requested(history, curr_user_comment):
    resp = {}
    resp['is_custom']=False
    print('history:{0}'.format(history))
    print('curr_user_comment:{0}'.format(history))
    # Checking if previous chatbot comment was asking to open a jira ticket
    if (check_preview_response(history)):
        # checking current user message is affirmative to create a jira ticket
        if(search_match(curr_user_comment, JIRA_YES_ANSWER, False)):
            resp['is_custom'] = True
            resp['message'] = JIRA_ASK_DETAILS[0]
        else:
            resp['is_custom'] = True
            resp['message'] = JIRA_TICKET_ACTION_CANCELED
    elif check_final_jira_confirmation(history):
        #Send jira ticket
        resp['is_custom'] = True
        history.append([curr_user_comment, ''])
        jiraObj.addJiraTicket(history, curr_user_comment)
        if jiraObj.TICKET_NUMBER is not None:
            resp['message'] = JIRA_TICKET_GENERATED.format(jiraObj.TICKET_URL)
        else:
            resp['message'] = JIRA_TICKET_NOT_GENERATED
    return resp

def ask_create_jira(curr_chatbot_response, curr_user_comment):
    resp = {}
    resp['is_custom']=False

    if curr_chatbot_response \
        and len(curr_chatbot_response) > 1:
        for matching in JIRA_MATCH_TO_OPEN_TICKET:
            resp_search_match = search_match(curr_chatbot_response, matching, True)
            if resp_search_match == True:
                resp['is_custom'] = True
                resp['message'] = JIRA_QUESTION_MESSAGE.format(curr_user_comment)
                return resp


def check_preview_response(history):
    if history and len(history) > 0:
        user_comment = history[-1][0] # Getting last user_comment 
        chatbot_comment = history[-1][1] # Getting last chatbot_comment
        jira_question = JIRA_QUESTION_MESSAGE.format(user_comment)
        print('*********check_preview_response************')
        print('jira_question: {0}'.format(jira_question))
        print('chatbot_comment: {0}'.format(chatbot_comment))
        print('*******************************************')
        if jira_question == chatbot_comment:
            return True
    return False

def query_to_sql(curr_chatbot_response):
    if curr_chatbot_response \
        and len(curr_chatbot_response) > 1:
        for matching in SQL_EXECUTION_MATCH:
            resp_search_match = search_match(curr_chatbot_response, matching, True)
            if resp_search_match == True:
                return True


def check_final_jira_confirmation(history):
    if history and len(history) > 0:
        chatbot_comment = history[-1][1] # Getting last chatbot_comment
        print('chatbot_comment: {0}'.format(chatbot_comment))
        print('JIRA_ASK_DETAILS: {0}'.format(JIRA_ASK_DETAILS[0]))
        return chatbot_comment == JIRA_ASK_DETAILS[0]
    return False

'''
match_all = True all items in the list must match to return True
match_all = False First match return True
'''
def search_match(txt_value, container, match_all):
    match_count = 0
    for val in container:
        if val in txt_value:
            match_count += 1
        if match_all == False and match_count > 0:
            return True
    print('txt_value "{0}" was found {1}/{2} times'.format(txt_value, match_count, len(container)))
    return (match_count == len(container))
