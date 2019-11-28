import json
import boto3

client = boto3.client("sns")

def lambda_handler(event, context):
    db = boto3.resource('dynamodb', region_name='us-east-1')
    
    customerRequest = eventParser(event)
    
    saveCustomerRequest(db, customerRequest)
    
    response = client.publish(PhoneNumber = '+27840550099', Message = createMessage(customerRequest))

    LexResponse= {"dialogAction":{
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message":{
            "contentType": "PlainText",
            "content": "Thank you for your request, our customer care center will contact you or an agent to will come to your home to assist you."
            }
        }
    }
    
    return LexResponse


def createMessage(customerRequest):
    name_and_surname = customerRequest["name_and_surname"]
    policy_number = customerRequest["policy_number"]
    policy_action = customerRequest["policy_action"]
    policy_type = customerRequest["policy_type"]
    date =  customerRequest["appointment_date"]
    time = customerRequest["appointment_time"]

    message = f'Customer Request alert!\n{name_and_surname}, policy number: {policy_number} would like to {policy_action} their policy to a {policy_type} policy on {date} {time}'
    
    return message
    
def saveCustomerRequest(dynamodb, customerRequest):
    table = dynamodb.Table('customerRequests')
    
    response = table.put_item(
        Item={
            "policyNumber": customerRequest["policy_number"],
            "nameSurname": customerRequest["name_and_surname"],
            "policyAction": customerRequest["policy_action"],
            "policyType": customerRequest["policy_type"],
            "appointmentTime": customerRequest["appointment_time"],
            "appointmentDate": customerRequest["appointment_date"],
            "reuestFufilled": False
        }
    )
    
def eventParser(event):
    event_dict = {
    "policy_number": event['currentIntent']['slots']['PolicyNumber'],
    "name_and_surname" : event['currentIntent']['slots']['NameAndSurname'],
    "policy_action":  event['currentIntent']['slots']['PolicyAction'],
    "policy_type": event['currentIntent']['slots']['PolicyType'],
    "appointment_date" : event['currentIntent']['slots']['Date'],
    "appointment_time" : event['currentIntent']['slots']['Time']
    }
    
    return event_dict