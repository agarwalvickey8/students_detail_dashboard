import pandas as pd
from django.core.management.base import BaseCommand
from staffsignup.models import StudentDetails

class Command(BaseCommand):
    help = 'Vacant student data'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                roll = row['STUDENT ROLL']  # Assuming 'Roll' is the column name containing roll numbers
                # Query the StudentDetails model to find the student by coaching roll number
                try:
                    student_detail = StudentDetails.objects.get(CoachingRoll=roll)
                    # Now, get the corresponding NEETAdmitCard instance
                    neet_admit_card = student_detail.neetregistration  # Assuming the related_name is 'neetadmitcard'
                    # breakpoint()
                    # Vacate the admit card values
                    neet_admit_card.DOB = None
                    neet_admit_card.NEETApplication = None
                    neet_admit_card.Category = ''
                    # Repeat this for other fields as needed
                    
                    # Save the changes
                    neet_admit_card.save()
                    
                    print(f"Admit card vacated for student with coaching roll number {roll}")
                except StudentDetails.DoesNotExist:
                    print(f"Student with coaching roll number {roll} not found")
        except FileNotFoundError:
            print(f"File {file_path} not found")
        except Exception as e:
            print(f"An error occurred: {e}")
