import requests
from django.core.management.base import BaseCommand
from project.models import Pokemon, Move

class Command(BaseCommand):
    help = 'Fetch Pokémon data from PokeAPI and save to database'

    def handle(self, *args, **kwargs):
        for dexnum in range(1, 1026):  # Example: Fetch first 151 Pokémon
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{dexnum}/')
            if response.status_code == 200:
                data = response.json()
                self.save_pokemon(data)
            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch data for Pokémon {dexnum}'))

    def save_pokemon(self, data):
        # Extract stats
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        
        # Extract types
        types = [t['type']['name'] for t in data['types']]
        type1 = types[0]
        type2 = types[1] if len(types) > 1 else None

        # Extract moves
        moves = []
        for move in data['moves']:
            move_name = move['move']['name']
            move_obj, created = Move.objects.get_or_create(name=move_name)
            moves.append(move_obj)

        # Extract sprite
        sprite = data['sprites']['front_default']

        # Create or update Pokémon
        pokemon, created = Pokemon.objects.update_or_create(
            dexnum=data['id'],
            defaults={
                'name': data['name'],
                'type1': type1,
                'type2': type2,
                'ability': data['abilities'][0]['ability']['name'],
                'item': None,  # Assuming no item data from this endpoint
                'health': stats['hp'],
                'attack': stats['attack'],
                'special_attack': stats['special-attack'],
                'defense': stats['defense'],
                'special_defense': stats['special-defense'],
                'speed': stats['speed'],
                'sprite': sprite,  # Save sprite URL
            }
        )
        pokemon.learnset.set(moves)
        pokemon.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully saved Pokémon {pokemon.name}'))

if __name__ == '__main__':
    Command().handle()