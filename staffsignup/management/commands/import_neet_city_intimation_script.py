# script to add neet students data in NEET city intimation model from excel
import pandas as pd
from django.core.management.base import BaseCommand
from staffsignup.models import StudentDetails, NEETCityIn
class Command(BaseCommand):
    help = 'Import NEET City Intimation data from Excel file'
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')
    def handle(self, *args, **options):
        file_path = options['file_path']
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                coaching_roll = row['COACHING ROLL']
                student = StudentDetails.objects.filter(CoachingRoll=coaching_roll).first()
                if student:
                    neet_city_intimation, created = NEETCityIn.objects.get_or_create(StudentDetail=student)
                    if pd.isna(row['Appno']):
                        self.stdout.write(self.style.ERROR(f'Student with coaching roll {coaching_roll} has a NaN NEET Application number. Skipping.'))
                        continue
                    category_mapping = {
                        'OBC-(NCL) AS PER CENTRAL LIST': 'OBC',
                        'GEN-EWS': 'EWS'
                    }
                    category = category_mapping.get(row['category'], row['category'])
                    neet_city_intimation.NEETApplication = int(row['Appno'])
                    neet_city_intimation.Name = row['name']
                    neet_city_intimation.FatherName = row['father']
                    neet_city_intimation.Category = category
                    neet_city_intimation.Pwd = row['pwd']
                    neet_city_intimation.City = row['city']
                    neet_city_intimation.State = row['state']
                    neet_city_intimation.save()
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'NEET City Intimation data added for {student}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'NEET City Intimation data updated for {student}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Student with coaching roll {coaching_roll} not found.'))
            self.stdout.write(self.style.SUCCESS('NEET City Intimation data imported successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))