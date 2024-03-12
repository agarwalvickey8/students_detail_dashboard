# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentDetails, NEETRegistration  # Import other related models

# Define signal handlers
@receiver(post_save, sender=StudentDetails)
def create_related_records(sender, instance, created, **kwargs):
    """
    Signal handler to create related records when a new StudentDetails instance is created.
    """
    if created:
        if instance.CourseType == 'NEET':
        # Example: Create a NEETRegistration instance associated with the new StudentDetails instance
            NEETRegistration.objects.create(StudentDetail=instance, NEETApplication=None, Mobile=None)
        # Add similar code for other related models