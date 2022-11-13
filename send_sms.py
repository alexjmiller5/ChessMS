from twilio.rest import Client
import database.query as database

import time

# Your Account SID from twilio.com/console
account_sid = "AC9af6e77f68ee8a3df8d4935caac08984"
# Your Auth Token from twilio.com/console
auth_token  = "ea317c10616edf03724ca862c6468dfd"

# our Trilio phone number:
trilio_number = "+17088477513"

client = Client(account_sid, auth_token)

# message = client.messages.create(
#     to="+16177980895", 
#     from_="+17088477513",
#     body="Hello from Python!")

# print(message.sid)

while True:
    # wait for a second between each refreshes
    # time.sleep(0.1)

    last_sms = client.messages.list()[0]

    sent_phone = last_sms.from_

    if sent_phone == trilio_number:
        continue

    user_phone = last_sms.to
    text = last_sms.body

    print(sent_phone + " sent to " + user_phone)
    print(text)
    print()

    #if database.check_user_exist(user_phone) == False:
        #database.create_user(user_phone)