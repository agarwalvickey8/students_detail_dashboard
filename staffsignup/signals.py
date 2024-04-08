from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JEEMAIN1Registration, StudentDetails, NEETRegistration  # Import other related models

@receiver(post_save, sender=StudentDetails)
def create_related_records(sender, instance, created, **kwargs):
    """
    Signal handler to create related records when a new StudentDetails instance is created.
    """
    if created:
        if instance.Exam == 'NEET':
            NEETRegistration.objects.create(StudentDetail=instance, NEETApplication=None, DOB=None, Category = None)
        elif instance.Exam == 'JEE':
            JEEMAIN1Registration.objects.create(StudentDetail = instance, JEEMAIN1Application = None, Mobile = None)