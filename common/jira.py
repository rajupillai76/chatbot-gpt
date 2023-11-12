#!/usr/local/bin/python3.8
import json
import random
import string

import requests


class Jira:
    """
  Methods
  -------
  add_comment(comment: str, ticket_number: str)
    - adds comment to specific ticket, returns comment URL
  create_ticket(summary: str, description: str)
    - creates ticket with summary and description, returns ticket URL
  get_description(ticket_number: str)
    - gets description for specific ticket, returns description
  add_description(ticket_number: str, description: str)
    - add/update description for specific ticket, returns description
  """

    def __init__(self):
        self.TICKET_NUMBER = None
        self.TICKET_URL = None
        self.base_url = "https://mysandbox.atlassian.net"
        self.base_api_url = self.base_url + "/rest/api"
        self.user = "john.doe@blah.com"
        self.api_key = "BXXT3xFfGF0IbCSFceKd9O7x0nBVFuaBSImo5LpsH_w26Xskk6jI10edas23P8CKMeZG6jUsgb0ClNp09n9S27wyGQYqgE-S_8AvfpzcndJ7Y2l3ndqhwODT1UiiB2N7E9z-c_vwi26h8Y_ShHUhuS71N2GSu1noWWc_A4TEw3_XnC87YmA=341CEE56"

    def with_context(self, description):
        return {
            "content": [
                {
                    "content": [
                        {
                            "text": description,
                            "type": "text"
                        }
                    ],
                    "type": "paragraph"
                }
            ],
            "type": "doc",
            "version": 1
        }

    def get_create_ticket_payload(self, summary, description):
        return {
            "fields": {
                "description": self.with_context(description),
                "issuetype": {
                    "name": "Support Request"
                },
                "project": {
                    "key": "GO"
                },
                "summary": summary,
                "customfield_11310": {  # Application
                    "value": "Cash"
                },
                "customfield_11315": {  # Assignment Group
                    "value": "Production Ops"
                }
            }
        }

    def add_description_payload(self, new_description):
        return {
            "fields": {
                "description": new_description,
            }
        }

    def get_comment_payload(self, comment):
        return {
            "body": comment
        }

    def make_request(self, url, payload=None, method=None):
        try:
            if method == "post":
                r = requests.post(url, auth=(self.user, self.api_key), json=payload)
            elif method == "put":
                r = requests.put(url, auth=(self.user, self.api_key), json=payload)
            else:
                r = requests.get(url, auth=(self.user, self.api_key))
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        try:
            json = r.json()
            return json
        except Exception as e:
            return {}

    def add_comment(self, comment, ticket_number):
        payload = self.get_comment_payload(comment)
        url = self.base_api_url + f"/2/issue/{ticket_number}/comment"
        response = self.make_request(url, payload=payload, method="post")
        comment_id = response["id"]
        comment_url = self.base_url + f"/browse/{ticket_number}?focusedCommentId={comment_id}"
        return comment_url

    def create_ticket(self, summary, description):
        payload = self.get_create_ticket_payload(summary, description)
        url = self.base_api_url + "/3/issue"
        response = self.make_request(url, payload=payload, method="post")
        ticket_number = response["id"]
        ticket_url = self.base_url + f"/browse/{response['key']}"
        return [ticket_number, ticket_url]

    def get_description(self, ticket_number):
        url = self.base_api_url + f"/3/issue/{ticket_number}?fields=description"
        response = self.make_request(url, method="get")
        description = response["fields"]["description"]
        return description

    def add_description(self, ticket_number, description):
        payload = self.add_description_payload(description)
        print("payload", json.dumps(payload))
        url = self.base_api_url + f"/3/issue/{ticket_number}"
        response = self.make_request(url, payload=payload, method="put")
        return response

    def addJiraTicket(self, history, input_text):
        try:
            if self.TICKET_NUMBER is None:
                response = self.create_ticket(input_text, input_text)
        #            f"Jira ticket created for Red Queen's AI ChatBot ({self.generate_random_code()})", input_text)
                print("Jira ticket was created: ", response[1])
                print("Jira ticket was created: ", response)
                self.TICKET_NUMBER = response[0]
                self.TICKET_URL = response[1]
                self.saveAllConversation(history, self.TICKET_NUMBER)
            else:
                print("Jira ticket was created: you can add comment in ->", self.TICKET_NUMBER)
                print("history:", history)
                self.saveAllConversation(history, self.TICKET_NUMBER)
        except Exception as e:
            self.TICKET_NUMBER = None
            print(f"Error in creating Jira task: {e}")

    def saveAllConversation(self, history, TICKET_NUMBER):
        # Initialize a list to store formatted conversation
        formatted_conversation = []

        # Process the array and extract user messages and bot responses
        for i in range(len(history)):
            # Ensure there are at least two elements in the subarray
            if len(history[i]) >= 2:
                user_message = history[i][0]
                bot_response = history[i][1]

                # Format user message
                user_message_formatted = {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "User: ",
                            "marks": [
                                {
                                    "type": "textColor",
                                    "attrs": {
                                        "color": "#0052cc"
                                    }
                                },
                                {
                                    "type": "strong"
                                }
                            ]
                        },
                        {
                            "type": "text",
                            "text": f" {user_message}"
                        }
                    ]
                }

                # Format bot response
                bot_response_formatted = {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Red Queen's AI ChatBot: ",
                            "marks": [
                                {
                                    "type": "textColor",
                                    "attrs": {
                                        "color": "#ff5630"
                                    }
                                },
                                {
                                    "type": "strong"
                                }
                            ]
                        },
                        {
                            "type": "text",
                            "text": f" {bot_response}"
                        }
                    ]
                }

                formatted_conversation.append(user_message_formatted)
                formatted_conversation.append(bot_response_formatted)

        # Convert the formatted conversation to ADF
        adf_conversation = {
            "version": 1,
            "type": "doc",
            "content": formatted_conversation
        }

        # update description
        self.add_description(TICKET_NUMBER, adf_conversation)

    def generate_random_code(self):
        # Possible characters (digits and uppercase letters)
        characters = string.digits + string.ascii_uppercase
        # Generate a random code of 6 characters
        code = ''.join(random.choice(characters) for _ in range(6))
        return code
