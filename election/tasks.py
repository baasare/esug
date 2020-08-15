from celery import shared_task
from django.core import mail
from django.template.loader import render_to_string

from election.models import PassCodeEmail


@shared_task()
def send_pass_codes():
    try:
        voter_emails = PassCodeEmail.objects.all().values('id', 'full_name', 'email', 'pass_code', 'domain')[0:10]

        connection = mail.get_connection()
        connection.open()

        email_subject = "Voting Passcode"
        template_name = "election/email_pass_code.html"
        path = 'vote'

        emails = []

        for voter in list(voter_emails):
            user_id = voter["id"]
            name = voter["full_name"]
            pass_code = voter["pass_code"]
            to_email = voter["email"]
            domain = voter["domain"]

            message = render_to_string(template_name=template_name, context={
                'pass_code': pass_code,
                'name': name,
                'domain': domain,
                'path': path
            }).strip()
            email = mail.EmailMessage(subject=email_subject,
                                      body=message,
                                      to=[to_email],
                                      from_email="esugec123@gmail.com")
            email.content_subtype = "html"
            emails.append(email)
            print("sent")

            PassCodeEmail.objects.filter(id=user_id).delete()

        connection.send_messages(emails)
        connection.close()

    except PassCodeEmail.DoesNotExist:
        print("No emails to send")
        pass


@shared_task()
def create_emails(domain, queryset):
    for voter in queryset:
        pass_code_email = PassCodeEmail(full_name=voter["full_name"],
                                        pass_code=voter["pass_code"],
                                        email=voter["email"],
                                        domain=domain)
        pass_code_email.save()
