from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin, messages
from django.contrib.sites.shortcuts import get_current_site
from import_export.admin import ImportExportModelAdmin

from .models import Queries, Candidate, Position, Election, Vote, Voter, PassCodeEmail
from .resources import VoterResource
# Register your models here.
from .tasks import create_emails

admin.site.site_header = "ESUG Admin"
admin.site.site_title = "ESUG Voter Admin"
admin.site.index_title = "ESUG Voter Admin"


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
        create_emails.delay(domain=current_site.domain,
                            queryset=list(queryset.values('full_name', 'email', 'pass_code')))
        messages.success(request, "Emails scheduled for sending")

    email_pass_codes.short_description = "Send selected voters their pass code"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'voted_at', 'candidate')


@admin.register(PassCodeEmail)
class PassCodeEmailAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
