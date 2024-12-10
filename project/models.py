from django.db import models
from django.core.exceptions import ValidationError

class Trainer(models.Model):
    """
    Model representing a trainer.
    """
    username = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username

class Move(models.Model):
    """
    Model representing a move that a Pokémon can learn.
    """
    CATEGORY_CHOICES = [
        ('physical', 'Physical'),
        ('special', 'Special'),
        ('status', 'Status'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    power = models.IntegerField(null=True, blank=True)
    pp = models.IntegerField(null=True, blank=True)
    accuracy = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    flavor_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Choices for Pokémon natures
NATURE_CHOICES = [
    ('Adamant', 'Adamant'),
    ('Bashful', 'Bashful'),
    ('Bold', 'Bold'),
    ('Brave', 'Brave'),
    ('Calm', 'Calm'),
    ('Careful', 'Careful'),
    ('Docile', 'Docile'),
    ('Gentle', 'Gentle'),
    ('Hardy', 'Hardy'),
    ('Hasty', 'Hasty'),
    ('Impish', 'Impish'),
    ('Jolly', 'Jolly'),
    ('Lax', 'Lax'),
    ('Lonely', 'Lonely'),
    ('Mild', 'Mild'),
    ('Modest', 'Modest'),
    ('Naive', 'Naive'),
    ('Naughty', 'Naughty'),
    ('Quiet', 'Quiet'),
    ('Quirky', 'Quirky'),
    ('Rash', 'Rash'),
    ('Relaxed', 'Relaxed'),
    ('Sassy', 'Sassy'),
    ('Serious', 'Serious'),
    ('Timid', 'Timid'),
]

class Pokemon(models.Model):
    """
    Model representing a Pokémon.
    """
    dexnum = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=50)
    type2 = models.CharField(max_length=50, null=True, blank=True)
    ability = models.CharField(max_length=100)
    item = models.CharField(max_length=100, null=True, blank=True)
    sprite = models.URLField(max_length=200, null=True, blank=True) 
    
    # Base stats
    health = models.IntegerField()
    attack = models.IntegerField()
    special_attack = models.IntegerField()
    defense = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()
    
    # IVs
    iv_health = models.IntegerField(default=31)
    iv_attack = models.IntegerField(default=31)
    iv_special_attack = models.IntegerField(default=31)
    iv_defense = models.IntegerField(default=31)
    iv_special_defense = models.IntegerField(default=31)
    iv_speed = models.IntegerField(default=31)
    
    # EVs
    ev_attack = models.IntegerField(default=0)
    ev_special_attack = models.IntegerField(default=0)
    ev_defense = models.IntegerField(default=0)
    ev_special_defense = models.IntegerField(default=0)
    ev_speed = models.IntegerField(default=0)
    
    # Nature
    nature = models.CharField(max_length=10, choices=NATURE_CHOICES, default='Hardy')
    
    learnset = models.ManyToManyField(Move, related_name='learnable_by')
    moveset = models.ManyToManyField(Move, related_name='used_by')

    def __str__(self):
        return self.name

class Team(models.Model):
    """
    Model representing a team of Pokémon.
    """
    name = models.CharField(max_length=100)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    pokemon = models.ManyToManyField('Pokemon', through='TeamPokemon')

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure a team cannot have more than 6 Pokémon.
        """
        super().save(*args, **kwargs)
        if self.teampokemon_set.count() > 6:
            raise ValidationError('A team cannot have more than 6 Pokémon.')

class TeamPokemon(models.Model):
    """
    Model representing the relationship between a team and a Pokémon.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    nature = models.CharField(max_length=10, choices=NATURE_CHOICES, default='Hardy')
    ev_health = models.IntegerField(default=0)
    ev_attack = models.IntegerField(default=0)
    ev_special_attack = models.IntegerField(default=0)
    ev_defense = models.IntegerField(default=0)
    ev_special_defense = models.IntegerField(default=0)
    ev_speed = models.IntegerField(default=0)
    moveset = models.ManyToManyField(Move, related_name='team_pokemon_moveset')

    def __str__(self):
        return f"{self.nickname or self.pokemon.name} in {self.team.name}"