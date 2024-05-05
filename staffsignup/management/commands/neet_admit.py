# script to add neet students data in NEET city intimation model from excel
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from staffsignup.models import NEETAdmitCard, StudentDetails
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
                    neet_city_intimation, created = NEETAdmitCard.objects.get_or_create(StudentDetail=student)
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
                    dob = row['dob']
                    if not isinstance(dob, str):
                        dob = dob.strftime('%Y-%m-%d')
                    else:
                        # Convert DOB to yyyy-mm-dd format
                        dob = datetime.strptime(dob, '%d-%m-%Y').strftime('%Y-%m-%d')
                    neet_city_intimation.DOB = dob
                    neet_city_intimation.NEETRoll = row['rollno']
                    neet_city_intimation.Category = category
                    neet_city_intimation.CentreNo = int(row['centreno'])
                    neet_city_intimation.CentreName = row['centrename']
                    neet_city_intimation.PWD = row['pwd']
                    neet_city_intimation.CentreAddress = row['centreaddress']
                    neet_city_intimation.Stateofele = row['stateofel']
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