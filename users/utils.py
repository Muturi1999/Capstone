from django.core.mail import EmailMessage


class EmailGen:
    @staticmethod
    def send_Email(data):
        email = EmailMessage(
            subject= data["subject"], 
            to= [data['To']],
             body=data['email_body'])
        email.send(fail_silently=True)
    