from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.template.loader import render_to_string

from election.models import Voter


class Command(BaseCommand):
    help = 'Create random users'

    def token_email(self, name, pass_code, email_subject, template_name, to_email, ):
        message = render_to_string(template_name=template_name, context={
            'pass_code': pass_code,
            'name': name,
        }).strip()

        email = EmailMessage(subject=email_subject, body=message, to=[to_email], from_email="ugneuronet@gmail.com", )
        email.content_subtype = "html"
        email.send(fail_silently=False)

    def handle(self, *args, **options):
        voters = Voter.objects.all()

        for voter in voters:
            email = voter.email
            name = voter.full_name
            pass_code = voter.pass_code
            self.token_email(name=name, pass_code=pass_code, email_subject="Voting passcode",
                             template_name="election/email_passcode.html",
                             to_email=email)
