from django import forms

from election.models import Queries


class QueryForm(forms.ModelForm):
    class Meta:
        model = Queries
        fields = ("name", "email", "subject", "message")
