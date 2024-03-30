import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
email_id = os.getenv('email_id')
email_password = os.getenv('email_password')


def send_mail():
    # to_addrs and msg have to be changed as required
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=email_id, password=email_password)
            connection.sendmail(
                from_addr=email_id,
                to_addrs="alangeorge3603@gmail.com",
                msg="ninja")
            print("Sent successfully!")
    except:
        print("An error occurred, please try again")
