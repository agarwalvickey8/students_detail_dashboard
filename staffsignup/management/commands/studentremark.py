# Inside clear_remarks.py

from django.core.management.base import BaseCommand
from staffsignup.models import RemarkStudents

class Command(BaseCommand):
    help = 'Clear remarks of all students'

    def handle(self, *args, **options):
        # Get all instances of RemarkStudents
        students = RemarkStudents.objects.all()

        # Iterate over instances and clear remarks
        for student in students:
            student.remarks = ''
            student.save()
        self.stdout.write(self.style.SUCCESS('Successfully cleared remarks for all students.'))