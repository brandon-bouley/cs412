from django import forms
from .models import *

class PokemonSearchForm(forms.Form):
    """
    Form for searching Pokémon by name.
    """
    name = forms.CharField(max_length=100, required=False, label='Search Pokémon')

    def search(self):
        """
        Method to perform the search based on the cleaned data.
        Returns a queryset of Pokémon whose names contain the search term.
        """
        name = self.cleaned_data['name']
        return Pokemon.objects.filter(name__icontains=name)

class CreateTeamForm(forms.ModelForm):
    """
    Form for creating a new team.
    """
    class Meta:
        model = Team
        fields = ['name', 'trainer']

class TeamPokemonForm(forms.ModelForm):
    """
    Form for adding or editing a Pokémon in a team.
    """
    class Meta:
        model = TeamPokemon
        fields = ['nickname', 'nature', 'ev_health', 'ev_attack', 'ev_special_attack', 'ev_defense', 'ev_special_defense', 'ev_speed', 'moveset']
        widgets = {
            'moveset': forms.CheckboxSelectMultiple,
            'ev_health': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 252, 'class': 'slider'}),
            'ev_attack': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 252, 'class': 'slider'}),
            'ev_special_attack': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 252, 'class': 'slider'}),
            'ev_defense': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 252, 'class': 'slider'}),
            'ev_special_defense': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 252, 'class': 'slider'}),
            'ev_speed': forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 252, 'class': 'slider'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with an optional Pokémon instance to set the moveset queryset.
        """
        pokemon = kwargs.pop('pokemon', None)
        super().__init__(*args, **kwargs)
        if pokemon:
            self.fields['moveset'].queryset = pokemon.learnset.all()
        self.fields['moveset'].help_text = "Select up to 4 moves"
        self.fields['moveset'].required = False

    def clean(self):
        """
        Custom validation to ensure the total EVs do not exceed 510.
        """
        cleaned_data = super().clean()
        total_evs = (
            cleaned_data.get('ev_health', 0) +
            cleaned_data.get('ev_attack', 0) +
            cleaned_data.get('ev_special_attack', 0) +
            cleaned_data.get('ev_defense', 0) +
            cleaned_data.get('ev_special_defense', 0) +
            cleaned_data.get('ev_speed', 0)
        )
        if total_evs > 510:
            raise forms.ValidationError("The total EVs cannot exceed 510.")
        return cleaned_data

    def clean_moveset(self):
        """
        Custom validation to ensure no more than 4 moves are selected.
        """
        moveset = self.cleaned_data.get('moveset')
        if len(moveset) > 4:
            raise forms.ValidationError("You can select up to 4 moves only.")
        return moveset

class TrainerForm(forms.ModelForm):
    """
    Form for creating or editing a trainer.
    """
    class Meta:
        model = Trainer
        fields = ['username', 'email']