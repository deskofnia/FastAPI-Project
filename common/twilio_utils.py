from twilio.rest import Client
TWILIO_ACCOUNT_SID = 'ACa1551f09880d92279f924b6127b6ccdf'
TWILIO_AUTH_TOKEN = '6530aef1b628f610d32e3aba3c3bd4a2'
TWILIO_PHONE_NUMBER = '+19179354364'

def send_message(to, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE_NUMBER,
        to=to,
        shorten_urls=True
    )
    print(message,"message")
    return message.sid
