import requests
from django.core.management.base import BaseCommand
from project.models import Move

class Command(BaseCommand):
    help = 'Fetch move data from PokeAPI and save to database'

    def handle(self, *args, **kwargs):
        move_id = 1
        while True:
            response = requests.get(f'https://pokeapi.co/api/v2/move/{move_id}/')
            if response.status_code == 200:
                data = response.json()
                self.save_move(data)
                move_id += 1
            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch data for move {move_id}'))
                break

    def save_move(self, data):
        # Extract flavor text
        flavor_text = None
        for entry in data['flavor_text_entries']:
            if entry['language']['name'] == 'en' and entry['version_group']['name'] == 'sword-shield':
                flavor_text = entry['flavor_text']
                break

        move, created = Move.objects.update_or_create(
            name=data['name'],
            defaults={
                'type': data['type']['name'],
                'power': data.get('power'),
                'pp': data['pp'],
                'accuracy': data.get('accuracy'),
                'category': data['damage_class']['name'],
                'flavor_text': flavor_text,  # Save flavor text
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created move {move.name}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated move {move.name}'))

if __name__ == '__main__':
    Command().handle()