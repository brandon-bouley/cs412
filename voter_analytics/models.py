from django.db import models
import csv
from datetime import datetime

class Voter(models.Model):
    # Identification
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.IntegerField(null=True, blank=True)
    zip_code = models.IntegerField()
    dob = models.DateField()
    dor = models.DateField()
    affiliation = models.TextField()
    precinct = models.CharField(max_length=10)
    # Election participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()


    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct}"
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    # Delete existing records to prevent duplicates
    Voter.objects.all().delete()
    
    filename = '/Users/brandonbouley/Desktop/django/newton_voters.csv'
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Handle missing apartment number
                apartment_number = int(row['Residential Address - Apartment Number']) if row['Residential Address - Apartment Number'] else None
                
                # Convert boolean fields
                v20state = row['v20state'].strip().upper() == 'TRUE'
                v21town = row['v21town'].strip().upper() == 'TRUE'
                v21primary = row['v21primary'].strip().upper() == 'TRUE'
                v22general = row['v22general'].strip().upper() == 'TRUE'
                v23town = row['v23town'].strip().upper() == 'TRUE'
                
                # Create a new instance of Voter object with this record from CSV
                voter = Voter(
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    street_number=int(row['Residential Address - Street Number']),
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=apartment_number,
                    zip_code=int(row['Residential Address - Zip Code']),
                    dob=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    dor=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    affiliation=row['Party Affiliation'].strip(),
                    precinct=row['Precinct Number'],
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    voter_score=int(row['voter_score'])
                )
                
                voter.save()  # Commit to database
                print(f"Created voter: {voter}")
            except Exception as e:
                print(f"Skipped: {row}")
                print(f"Error: {e}")