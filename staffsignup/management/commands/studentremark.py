from django.core.management.base import BaseCommand
from staffsignup.models import NEETAdmitCard, StudentDetails, RemarkStudents

class Command(BaseCommand):
    help = 'Check for discrepancies between NEETCityIn and StudentDetails models and create RemarkStudents instances'

    def handle(self, *args, **options):
        for neet_city_in_instance in NEETAdmitCard.objects.all():
            if neet_city_in_instance.Name:  # Check if Name is not None
                coaching_roll = neet_city_in_instance.StudentDetail.CoachingRoll
                neet_name = neet_city_in_instance.Name.strip().upper()  # Remove leading and trailing spaces, convert to uppercase for case-insensitive comparison
                try:
                    student_details_instance = StudentDetails.objects.get(CoachingRoll=coaching_roll)
                    student_details_name = student_details_instance.Name.strip().upper()  # Remove leading and trailing spaces, convert to uppercase for case-insensitive comparison
                    if student_details_name != neet_name:
                        # Check if RemarkStudents instance already exists for this StudentDetail
                        if not RemarkStudents.objects.filter(StudentDetail=student_details_instance).exists():
                            # Create RemarkStudents instance with CoachingRoll and StudentDetail
                            RemarkStudents.objects.create(
                                CoachingRoll=coaching_roll,
                                StudentDetail=student_details_instance
                            )
                            self.stdout.write(self.style.SUCCESS(f"Student '{neet_name}' added"))
                        else:
                            self.stdout.write(self.style.WARNING(f"Student '{neet_name}' already exists in RemarkStudents"))
                    else:
                        self.stdout.write(self.style.WARNING(f"No discrepancies found for student '{neet_name}'"))
                except StudentDetails.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Student with coaching roll '{coaching_roll}' not found"))
