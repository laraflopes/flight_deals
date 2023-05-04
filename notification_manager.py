from twilio.rest import Client
import smtplib

ACCOUNT_SID = "secret account"
AUTH_TOKEN = "secret token"
TWILIO_NUMBER = "phone number"
MY_NUMBER = "phone number"

MY_EMAIL = "email"
PASSWORD = "password"


class NotificationManager:
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_message(self, message):
        message = self.client.messages \
            .create(
                body=message,
                from_=TWILIO_NUMBER,
                to=MY_NUMBER
            )

        print(message.status)

    def send_email(self, message, emails, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )
