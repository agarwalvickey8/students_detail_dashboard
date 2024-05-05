# update neet registration model with dob and neetapplication number
import pandas as pd
from django.core.management.base import BaseCommand
from staffsignup.models import NEETRegistration, StudentDetails

class Command(BaseCommand):
    help = 'Update NEETRegistration data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        updated_count = 0
        not_found_count = 0
        error_count = 0
        error_students = []

        try:
            # Read the Excel file into a Pandas DataFrame
            df = pd.read_excel(file_path)

            # Iterate over each row in the DataFrame
            for index, row in df.iterrows():
                coaching_roll = row['COACHING ROLL']

                # Query the NEETRegistration model to find the corresponding student by coaching roll
                neet_registration = NEETRegistration.objects.filter(StudentDetail__CoachingRoll=coaching_roll).first()

                if neet_registration:
                    try:
                        # Update NEETRegistration data with the values from the Excel file
                        neet_registration.NEETApplication = row['NEETAPPLICATION']
                        neet_registration.DOB = row.get('DOB2')  # Use .get() to handle missing keys gracefully
                        neet_registration.save()
                        updated_count += 1
                    except Exception as e:
                        error_count += 1
                        error_students.append(coaching_roll)
                        self.stdout.write(self.style.ERROR(f'Error updating data for coaching roll {coaching_roll}: {str(e)}'))
                else:
                    not_found_count += 1

            self.stdout.write(self.style.SUCCESS(f'NEETRegistration data updated for {updated_count} students.'))
            self.stdout.write(self.style.ERROR(f'NEETRegistration data not found for {not_found_count} students.'))
            self.stdout.write(self.style.ERROR(f'Encountered errors while updating data for {error_count} students.'))
            if error_students:
                self.stdout.write(self.style.ERROR(f'Students with errors: {", ".join(str(coaching_roll) for coaching_roll in error_students)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
