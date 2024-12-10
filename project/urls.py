from django.urls import path
from .views import (
    ShowAllPokemonView, ShowPokemonPageView, TrainerListView, TrainerCreateView, 
    TrainerDetailView, CreateTeamView, PokemonSearchView, CreateTeamPokemonView, 
    TeamDetailView, EditTeamPokemonView, DeleteTeamPokemonView, TeamListView, 
    TeamDeleteView, export_team
)

urlpatterns = [
    # Pokédex URLs
    path('', ShowAllPokemonView.as_view(), name='pokemon_list'),
    path('pokemon/<int:dexnum>/', ShowPokemonPageView.as_view(), name='pokemon_detail'),

    # Trainer URLs
    path('trainer_list/', TrainerListView.as_view(), name='trainer_list'),
    path('trainer/create/', TrainerCreateView.as_view(), name='trainer_create'),
    path('trainer/<int:pk>/', TrainerDetailView.as_view(), name='trainer_detail'),

    # Team URLs
    path('create_team/', CreateTeamView.as_view(), name='create_team'),
    path('teams/', TeamListView.as_view(), name='team_list'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('team/<int:pk>/delete/', TeamDeleteView.as_view(), name='delete_team'),
    path('team/<int:pk>/export/', export_team, name='export_team'),

    # Team Pokémon URLs
    path('team/<int:pk>/search_pokemon/', PokemonSearchView.as_view(), name='search_pokemon'),
    path('team/<int:pk>/add_pokemon/<int:dexnum>/', CreateTeamPokemonView.as_view(), name='add_team_pokemon'),
    path('team/<int:pk>/edit_pokemon/<int:team_pokemon_pk>/', EditTeamPokemonView.as_view(), name='edit_team_pokemon'),
    path('team/<int:pk>/delete_pokemon/<int:team_pokemon_pk>/', DeleteTeamPokemonView.as_view(), name='delete_team_pokemon'),
]