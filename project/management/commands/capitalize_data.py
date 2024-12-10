from django.core.management.base import BaseCommand
from project.models import Pokemon, Move

class Command(BaseCommand):
    help = 'Capitalize the first letter of all text fields in Pokemon and Move models'

    def handle(self, *args, **kwargs):
        self.capitalize_pokemon()
        self.capitalize_moves()

    def capitalize_pokemon(self):
        pokemons = Pokemon.objects.all()
        for pokemon in pokemons:
            pokemon.name = pokemon.name.capitalize()
            pokemon.type1 = pokemon.type1.capitalize()
            if pokemon.type2:
                pokemon.type2 = pokemon.type2.capitalize()
            pokemon.ability = pokemon.ability.capitalize()
            if pokemon.item:
                pokemon.item = pokemon.item.capitalize()
            pokemon.save()
            self.stdout.write(self.style.SUCCESS(f'Updated Pokémon: {pokemon.name}'))

    def capitalize_moves(self):
        moves = Move.objects.all()
        for move in moves:
            move.name = move.name.capitalize()
            move.save()
            self.stdout.write(self.style.SUCCESS(f'Updated Move: {move.name}'))

if __name__ == '__main__':
    Command().handle()