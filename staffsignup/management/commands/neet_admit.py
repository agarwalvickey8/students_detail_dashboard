# script to add neet students data in NEET Admit model from excel
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from staffsignup.models import NEETAdmitCard, StudentDetails
class Command(BaseCommand):
    help = 'Import NEET Admit data from Excel file'
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
                    neet_admit, created = NEETAdmitCard.objects.get_or_create(StudentDetail=student)
                    if pd.isna(row['Appno']):
                        self.stdout.write(self.style.ERROR(f'Student with coaching roll {coaching_roll} has a NaN NEET Application number. Skipping.'))
                        continue
                    category_mapping = {
                        'OBC-(NCL) AS PER CENTRAL LIST': 'OBC',
                        'GEN-EWS': 'EWS'
                    }
                    category = category_mapping.get(row['category'], row['category'])
                    neet_admit.NEETApplication = int(row['Appno'])
                    neet_admit.Name = row['name']
                    neet_admit.FatherName = row['father']
                    dob = row['dob']
                    if not isinstance(dob, str):
                        dob = dob.strftime('%Y-%m-%d')
                    else:
                        # Convert DOB to yyyy-mm-dd format
                        dob = datetime.strptime(dob, '%d-%m-%Y').strftime('%Y-%m-%d')
                    neet_admit.DOB = dob
                    neet_admit.NEETRoll = row['rollno']
                    neet_admit.Category = category
                    neet_admit.CentreNo = int(row['centreno'])
                    neet_admit.CentreName = row['centrename']
                    neet_admit.PWD = row['pwd']
                    neet_admit.CentreAddress = row['centreaddress']
                    neet_admit.Stateofele = row['stateofel']
                    neet_admit.save()
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'NEET Admit data added for {student}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'NEET Admit data updated for {student}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Student with coaching roll {coaching_roll} not found.'))
            self.stdout.write(self.style.SUCCESS('NEET Admit data imported successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))