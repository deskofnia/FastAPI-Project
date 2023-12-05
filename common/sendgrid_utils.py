import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, To
from config import env_variables

sg = sendgrid.SendGridAPIClient(api_key=env_variables.SENDGRID_API_KEY)


def send_email(from_email, to_email, subject, content):
    from_email = Email(from_email)
    to_email = To(to_email)
    subject = subject
    content = Content("text/html", content)
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    response = sg.client.mail.send.post(request_body=mail_json)

    return response.status_code
