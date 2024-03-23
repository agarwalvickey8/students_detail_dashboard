from django.db import models
import random
import string
class Branch(models.Model):
    Name = models.CharField(max_length = 100)
    def __str__(self):
        return self.Name
    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
    
class Staff(models.Model):
    Name = models.CharField(max_length=100)
    Username = models.CharField(max_length=100, blank=True, unique=True)
    Password = models.CharField(max_length=100, blank=True)
    Branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Username

    def generate_random_password(self):
        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=3))
        return f"{random_chars}"

    def save(self, *args, **kwargs):
        if not self.id:
            base_username = f"{self.Branch.Name.lower().replace(' ', '_')}_{self.Name.lower().replace(' ', '_')}"
            existing_usernames = Staff.objects.filter(Username__startswith=base_username).values_list('Username', flat=True)
            if existing_usernames:
                suffix = 1
                new_username = f"{base_username}_{suffix}"
                while new_username in existing_usernames:
                    suffix += 1
                    new_username = f"{base_username}_{suffix}"
                self.Username = new_username
            else:
                self.Username = base_username
            self.Password = self.__str__() + '@' + self.generate_random_password()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
        
class DisplayPreference(models.Model):
    staff = models.ForeignKey('Staff', on_delete = models.CASCADE)
    model_name = models.CharField(max_length = 100)
    
    class Meta:
        verbose_name = "Display Preference"
        verbose_name_plural = "Display Preferences"
        
class StudentDetails(models.Model):
    CoachingRegisteration = models.CharField(max_length = 100)
    CoachingRoll = models.CharField(max_length = 100)
    Name = models.CharField(max_length = 100)
    FatherName = models.CharField(max_length = 100)
    MotherName = models.CharField(max_length = 100)
    Course = models.CharField(max_length = 100)
    CourseId = models.IntegerField()
    Batch = models.CharField(max_length = 100)
    Medium = models.CharField(max_length = 100)
    DOB = models.DateField()
    Gender = models.CharField(max_length = 100)
    Category = models.CharField(max_length = 100)
    Address = models.CharField(max_length = 500)
    Tehsil = models.CharField(max_length = 100)
    District = models.CharField(max_length = 100)
    State = models.CharField(max_length = 100)
    PreviousRoll = models.CharField(max_length = 100)
    CourseType = models.CharField(max_length = 100)
    Branch = models.ForeignKey(Branch, on_delete = models.CASCADE)  # Add default=None here
    
    def __str__(self):
        return self.Name
    
    class Meta:
        verbose_name = "Student Details"
        verbose_name_plural = "Student Details"
        
class NEETRegistration(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete = models.CASCADE)
    NEETApplication = models.BigIntegerField(blank = True, null = True)
    Mobile = models.BigIntegerField(blank = True, null = True)
    
    def __str__(self):
        return self.StudentDetail.Name
    
    class Meta:
        verbose_name = "NEET Registrations"
        verbose_name_plural = "NEET Registrations"
        
class JEEMAIN1Registration(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete = models.CASCADE)
    JEEMAIN1Application = models.BigIntegerField(blank = True, null = True)
    Mobile = models.BigIntegerField(blank = True, null = True)
    
    def __str__(self):
        return self.StudentDetail.Name
    
    class Meta:
        verbose_name = "JEE Main 1 Registrations"
        verbose_name_plural = "JEE Main 1 Registrations"