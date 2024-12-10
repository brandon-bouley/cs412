from django.shortcuts import redirect, get_object_or_404, render
from .models import *
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponse

class ShowAllPokemonView(ListView):
    """
    View to display a list of all Pokémon.
    Allows filtering by generation using a query parameter.
    """
    model = Pokemon
    template_name = 'project/pokemon_list.html'
    context_object_name = 'pokemon_list'

    def get_queryset(self):
        generation = self.request.GET.get('generation', 'all')
        generation_ranges = {
            '1': (1, 151),
            '2': (152, 251),
            '3': (252, 386),
            '4': (387, 493),
            '5': (494, 649),
            '6': (650, 721),
            '7': (722, 809),
            '8': (810, 905),
            '9': (906, 1025),
        }
        if generation == 'all':
            return Pokemon.objects.all()
        start, end = generation_ranges.get(generation, (1, 151))
        return Pokemon.objects.filter(dexnum__gte=start, dexnum__lte=end)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['generation'] = self.request.GET.get('generation', 'all')
        return context

class TrainerListView(ListView):
    """
    View to display a list of all trainers.
    """
    model = Trainer
    template_name = 'project/trainer_list.html'
    context_object_name = 'trainers'

class TrainerCreateView(CreateView):
    """
    View to create a new trainer.
    """
    model = Trainer
    form_class = TrainerForm
    template_name = 'project/trainer_form.html'

    def get_success_url(self):
        return reverse_lazy('trainer_list')

class TrainerDetailView(DetailView):
    """
    View to display the details of a specific trainer.
    """
    model = Trainer
    template_name = 'project/trainer_detail.html'
    context_object_name = 'trainer'

class ShowPokemonPageView(DetailView):
    """
    View to display the details of a specific Pokémon.
    """
    model = Pokemon
    template_name = 'project/pokemon_detail.html'
    context_object_name = 'pokemon'
    pk_url_kwarg = 'dexnum' 

class CreateTeamView(CreateView):
    """
    View to create a new team.
    """
    model = Team
    form_class = CreateTeamForm
    template_name = 'project/create_team_form.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect('team_detail', pk=self.object.pk)

class TeamDetailView(DetailView):
    """
    View to display the details of a specific team.
    """
    model = Team
    template_name = 'project/team_detail.html'
    context_object_name = 'team'

class PokemonSearchView(FormView):
    """
    View to search for a Pokémon by name.
    """
    template_name = 'project/pokemon_search.html'
    form_class = PokemonSearchForm

    def form_valid(self, form):
        pokemons = form.search()
        if pokemons.exists():
            pokemon = pokemons.first()  # Assuming you want to select the first match
            return redirect('add_team_pokemon', pk=self.kwargs['pk'], dexnum=pokemon.dexnum)
        else:
            form.add_error('name', 'No Pokémon found with this name')
            return self.form_invalid(form)

class CreateTeamPokemonView(CreateView):
    """
    View to add a Pokémon to a team.
    """
    model = TeamPokemon
    form_class = TeamPokemonForm
    template_name = 'project/add_team_pokemon.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        pokemon = get_object_or_404(Pokemon, dexnum=self.kwargs['dexnum'])
        kwargs['pokemon'] = pokemon
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pokemon'] = get_object_or_404(Pokemon, dexnum=self.kwargs['dexnum'])
        return context

    def form_valid(self, form):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        if team.teampokemon_set.count() >= 6:
            form.add_error(None, 'A team cannot have more than 6 Pokémon.')
            return self.form_invalid(form)
        pokemon = get_object_or_404(Pokemon, dexnum=self.kwargs['dexnum'])
        team_pokemon = form.save(commit=False)
        team_pokemon.team = team
        team_pokemon.pokemon = pokemon
        team_pokemon.save()
        form.save_m2m()
        return redirect('team_detail', pk=team.pk)
    
class EditTeamPokemonView(UpdateView):
    """
    View to edit the details of a Pokémon in a team.
    """
    model = TeamPokemon
    form_class = TeamPokemonForm
    template_name = 'project/edit_team_pokemon.html'

    def get_object(self):
        return get_object_or_404(TeamPokemon, pk=self.kwargs['team_pokemon_pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pokemon'] = self.object.pokemon
        return kwargs

    def form_valid(self, form):
        team_pokemon = form.save(commit=False)
        team = team_pokemon.team
        if team.teampokemon_set.count() > 6:
            form.add_error(None, 'A team cannot have more than 6 Pokémon.')
            return self.form_invalid(form)
        team_pokemon.save()
        form.save_m2m()
        return redirect('team_detail', pk=self.kwargs['pk'])
    
class DeleteTeamPokemonView(DeleteView):
    """
    View to delete a Pokémon from a team.
    """
    model = TeamPokemon
    template_name = 'project/delete_team_pokemon.html'

    def get_object(self):
        return get_object_or_404(TeamPokemon, pk=self.kwargs['team_pokemon_pk'])

    def get_success_url(self):
        return reverse_lazy('team_detail', kwargs={'pk': self.kwargs['pk']})

class TeamListView(ListView):
    """
    View to display a list of all teams.
    """
    model = Team
    template_name = 'project/team_list.html'
    context_object_name = 'teams'

class TeamDeleteView(DeleteView):
    """
    View to delete a team.
    """
    model = Team
    template_name = 'project/team_confirm_delete.html'
    context_object_name = 'team'
    success_url = reverse_lazy('team_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        TeamPokemon.objects.filter(team=self.object).delete()
        self.object.delete()
        return redirect(self.success_url)

def export_team(request, pk):
    """
    View to export a team in a text format suitable for Pokémon Showdown.
    """
    team = get_object_or_404(Team, pk=pk)
    export_text = ""

    for team_pokemon in team.teampokemon_set.all():
        export_text += f"{team_pokemon.nickname or team_pokemon.pokemon.name}\n"
        export_text += f"Ability: {team_pokemon.pokemon.ability}\n"
        
        evs = []
        if team_pokemon.ev_health:
            evs.append(f"{team_pokemon.ev_health} HP")
        if team_pokemon.ev_attack:
            evs.append(f"{team_pokemon.ev_attack} Atk")
        if team_pokemon.ev_defense:
            evs.append(f"{team_pokemon.ev_defense} Def")
        if team_pokemon.ev_special_attack:
            evs.append(f"{team_pokemon.ev_special_attack} SpA")
        if team_pokemon.ev_special_defense:
            evs.append(f"{team_pokemon.ev_special_defense} SpD")
        if team_pokemon.ev_speed:
            evs.append(f"{team_pokemon.ev_speed} Spe")
        if evs:
            export_text += f"EVs: {' / '.join(evs)}\n"
        
        export_text += f"{team_pokemon.nature} Nature\n"
        
        for move in team_pokemon.moveset.all():
            export_text += f"- {move.name}\n"
        
        export_text += "\n"

    return render(request, 'project/export_team.html', {'export_text': export_text})