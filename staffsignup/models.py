from django.db import models

class Branch(models.Model):
    Name = models.CharField(max_length=100)
    def __str__(self):
        return self.Name
    
class Staff(models.Model):
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Branch = models.ForeignKey(Branch, on_delete=models.CASCADE)  # Add default=None here
    def __str__(self):
        return self.Username

class DisplayPreference(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    
class StudentDetails(models.Model):
    CoachingRegisteration = models.CharField(max_length=100)
    CoachingRoll = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    FatherName = models.CharField(max_length=100)
    MotherName = models.CharField(max_length=100)
    Course = models.CharField(max_length=100)
    CourseId = models.IntegerField()
    Batch = models.CharField(max_length=100)
    Medium = models.CharField(max_length=100)
    DOB = models.DateField()
    Gender = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    Address = models.CharField(max_length=500)
    Tehsil = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    PreviousRoll = models.CharField(max_length=100)
    CourseType = models.CharField(max_length=100)
    Branch = models.ForeignKey(Branch, on_delete=models.CASCADE)  # Add default=None here
    def __str__(self):
        return self.Name
    
class NEETRegistration(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete = models.CASCADE)
    NEETApplication = models.BigIntegerField(blank=True, null=True)
    Mobile = models.BigIntegerField(blank=True, null=True)
    def __str__(self):
        return self.StudentDetail.Name