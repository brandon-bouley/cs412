from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_dob']:
                queryset = queryset.filter(dob__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data['max_dob']:
                queryset = queryset.filter(dob__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['v20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['v21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['v23town']:
                queryset = queryset.filter(v23town=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_dob']:
                queryset = queryset.filter(dob__gte=form.cleaned_data['min_dob'])
            if form.cleaned_data['max_dob']:
                queryset = queryset.filter(dob__lte=form.cleaned_data['max_dob'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['v20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['v21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['v23town']:
                queryset = queryset.filter(v23town=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Histogram of Voters by Year of Birth
        birth_years = [voter.dob.year for voter in queryset]
        birth_year_hist = px.histogram(x=birth_years, nbins=30, title='Distribution of Voters by Year of Birth')
        birth_year_hist_div = plot(birth_year_hist, output_type='div')

        # Pie Chart of Voters by Party Affiliation
        party_affiliations = [voter.affiliation for voter in queryset]
        party_affiliation_pie = px.pie(names=party_affiliations, title='Distribution of Voters by Party Affiliation')
        party_affiliation_pie_div = plot(party_affiliation_pie, output_type='div')

        # Histogram of Voters by Election Participation
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [sum(getattr(voter, election) for voter in queryset) for election in elections]
        election_hist = go.Figure(data=[go.Bar(x=elections, y=election_counts)])
        election_hist.update_layout(title='Distribution of Voters by Election Participation')
        election_hist_div = plot(election_hist, output_type='div')

        context['birth_year_hist_div'] = birth_year_hist_div
        context['party_affiliation_pie_div'] = party_affiliation_pie_div
        context['election_hist_div'] = election_hist_div
        context['form'] = VoterFilterForm(self.request.GET)
        return context