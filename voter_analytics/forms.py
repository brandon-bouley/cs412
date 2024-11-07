from django import forms
from .models import Voter
from datetime import datetime
class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(choices=[('', 'Any')] + [(pa, pa) for pa in Voter.objects.values_list('affiliation', flat=True).distinct()], required=False)
    min_dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, datetime.now().year + 1)), required=False)
    max_dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, datetime.now().year + 1)), required=False)
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + [(vs, vs) for vs in Voter.objects.values_list('voter_score', flat=True).distinct()], required=False)
    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)