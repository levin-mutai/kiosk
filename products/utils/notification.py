from __future__ import print_function

import africastalking

class SMS:
    def __init__(self):
        # Set your app credentials
        self.username = "sandbox"
        self.api_key = "f66fc49eaf0fe5110775e3899b032ce79ba649eae61b4212ffbf9b9244d588ea"

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self,recepient,message):
        # Set the numbers you want to send to in international format
        recipients = [recepient]

        # Set your message
        message = message

        # Set your shortCode or senderId
        sender = "Kiosk"
        try:
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, recipients, sender)
            print (response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))
       