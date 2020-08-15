from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.template.loader import render_to_string
from import_export.admin import ImportExportModelAdmin

from .models import Queries, Candidate, Position, Election, Vote, Voter
from .resources import VoterResource

# Register your models here.


admin.site.site_header = "ESUG Admin"
admin.site.site_title = "ESUG Voter Admin"
admin.site.index_title = "ESUG Voter Admin"


def pass_code_email(connection, name, pass_code, email_subject, template_name, to_email, current_site, path):
    message = render_to_string(template_name=template_name, context={
        'pass_code': pass_code,
        'name': name,
        'domain': current_site.domain,
        'path': path
    }).strip()

    email = mail.EmailMessage(subject=email_subject, body=message, to=[to_email],
                              from_email="ec.esug.legon@gmail.com", connection=connection)
    email.content_subtype = "html"
    return email


@admin.register(Queries)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at')


@admin.register(Candidate)
class CandidateAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('full_name', 'position', 'level', 'course_offering', 'year', 'total_votes')
    list_filter = ('level', 'course_offering', 'year')
    search_fields = ('full_name', 'level', 'course_offering')


class CandidateInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Candidate


@admin.register(Position)
class PositionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'description', 'contestable')
    inlines = (CandidateInline,)


class PositionInline(admin.TabularInline):
    model = Position


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    inlines = (PositionInline,)


@admin.register(Voter)
class VoterAdmin(ImportExportModelAdmin):
    exclude = ('pass_code',)
    list_display = ('full_name', 'email')
    resource_class = VoterResource
    actions = ['email_pass_codes', ]

    def email_pass_codes(self, request, queryset):
        current_site = get_current_site(request)
        connection = mail.get_connection()
        connection.open()
        emails = []
        for voter in queryset:
            email = pass_code_email(connection=connection, name=voter.full_name, pass_code=voter.pass_code,
                                    email_subject="Voting passcode",
                                    template_name="election/email_pass_code.html",
                                    to_email=voter.email, current_site=current_site, path='vote')
            # emails.append(email)
            email.send(fail_silently=False)
            print(voter.email)

        # connection.send_messages(emails)
        connection.close()

    email_pass_codes.short_description = "Send selected voters their pass code"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'voted_at', 'candidate')
