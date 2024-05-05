from django.db import models
import random
import string
class Branch(models.Model):
    Name = models.CharField(max_length=100)
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
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    model_name = models.CharField(max_length = 255)
    
    class Meta:
        verbose_name = "Display Preference"
        verbose_name_plural = "Display Preferences"
        
class StudentDetails(models.Model):
    CoachingRegisteration = models.BigIntegerField()
    CoachingRoll = models.BigIntegerField()
    Name = models.CharField(max_length=100)
    FatherName = models.CharField(max_length=100, blank=True)
    MotherName = models.CharField(max_length=100)
    PrimaryNumber = models.CharField(max_length=10, blank=True, null=True)
    SecondaryNumber = models.CharField(max_length=10, blank=True, null=True)
    AdditionalNumber = models.CharField(max_length=10, blank=True, null=True)
    WhatsappNumber = models.CharField(max_length=10, blank=True, null=True)
    Course = models.CharField(max_length=100)
    CourseId = models.IntegerField()
    Batch = models.CharField(max_length=100)
    Medium = models.CharField(max_length=100)
    DOB = models.DateField(blank=True, null=True)
    Gender = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    Address = models.CharField(max_length=500)
    Tehsil = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Pincode = models.CharField(max_length=10, blank=True, null=True)
    PreviousRoll = models.CharField(max_length=100, blank=True, null=True)
    Exam = models.CharField(max_length=100)
    Branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Name
    
    class Meta:
        verbose_name = "Student Details"
        verbose_name_plural = "Student Details"
        
class NEETRegistration(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete=models.CASCADE)
    NEETApplication = models.BigIntegerField(blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)
    Category = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.StudentDetail.Name
    
    class Meta:
        verbose_name = "NEET Registrations"
        verbose_name_plural = "NEET Registrations"
        
class JEEMAIN1Registration(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete=models.CASCADE)
    JEEMAIN1Application = models.BigIntegerField(blank=True, null=True)
    Mobile = models.BigIntegerField(blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.StudentDetail.Name
    
    class Meta:
        verbose_name = "JEE Main 1 Registrations"
        verbose_name_plural = "JEE Main 1 Registrations"
        
class StaffDetailTracking(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    details_added = models.PositiveIntegerField(default=0)
    details_added_flag = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.staff} - {self.details_added} details added"
    
class FieldHistory(models.Model):
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255, null=True, blank=True)
    new_value = models.CharField(max_length=255)
    action = models.CharField(max_length=10, choices=(('add', 'Add'), ('edit', 'Edit')))
    model_name=models.CharField(max_length=20)
    coaching_roll = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.staff.Username} - {self.field_name} - {self.action} - {self.timestamp}"

class JeeAdvReg(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete=models.CASCADE)
    AdvanceRegNo = models.CharField(max_length = 252, blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)
    Mobile = models.BigIntegerField(blank=True, null=True)
    def __str__(self):
        return self.StudentDetail.Name
    
    class Meta:
        verbose_name = "JEE Advanced Registrations"
        verbose_name_plural = "JEE Advanced Registrations"
class NEETCityIn(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete=models.CASCADE)
    NEETApplication = models.CharField(max_length=252, blank=True, null=True)
    Name = models.CharField(max_length=252, blank=True, null=True)
    FatherName = models.CharField(max_length=252, blank=True, null=True)
    Category = models.CharField(max_length=252, blank=True, null=True)
    Pwd = models.CharField(max_length=3, blank=True, null=True)
    City = models.CharField(max_length=252, blank=True, null=True)
    State = models.CharField(max_length=252, blank=True, null=True)
    
    def __str__(self):
        return self.StudentDetail.Name
    
    class Meta:
        verbose_name = "NEET City Intimation"
        verbose_name_plural = "NEET City Intimation"
        
class RemarkStudents(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete=models.CASCADE)
    CoachingRoll = models.BigIntegerField(blank=True,null=True)
    remarks = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.StudentDetail.Name
    class Meta:
        verbose_name = "Student Review"
        verbose_name_plural = "Student Reviews"

class NEETAdmitCard(models.Model):
    StudentDetail = models.OneToOneField(StudentDetails, on_delete=models.CASCADE)
    Name = models.CharField(max_length=252, blank=True, null=True)
    FatherName = models.CharField(max_length=252, blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)
    NEETRoll = models.CharField(max_length=252, blank=True, null=True)
    NEETApplication = models.CharField(max_length=252, blank=True, null=True)
    Category = models.CharField(max_length=252, blank=True, null=True)
    CentreNo = models.CharField(max_length=252, blank=True, null=True)
    CentreName = models.TextField(blank=True, null=True)
    CentreAddress = models.TextField(blank=True, null=True)
    PWD = models.CharField(max_length=252, blank=True, null=True)
    Stateofele = models.CharField(max_length=252, blank=True, null=True)
    def __str__(self):
        return self.StudentDetail.Name
    class Meta:
        verbose_name = "NEET Admit Card Details"
        verbose_name_plural = "NEET Admit Card Details"
        
# class JEEMainResult(models.Model):
#     StudentDetail = models.OneToOneField(StudentDetails, on_delete=models.CASCADE)
#     JEEApplication = models.BigIntegerField(blank=True, null=True)
#     DOB = models.DateField(blank=True, null=True)
#     Name = models.CharField(max_length=252, blank=True, null=True)
#     FathersName = models.CharField(max_length=252, blank=True, null=True)
#     Category = models.CharField(max_length=252,blank=True,null=True)
#     Maths1Score = models.CharField(max_length=252, blank=True, null=True)
#     Maths2Score = models.CharField(max_length=252, blank=True, null=True)
#     MathsfinalScore = models.CharField(max_length=252, blank=True, null=True)
#     Physics1Score = models.CharField(max_length=252, blank=True, null=True)
#     Physics2Score = models.CharField(max_length=252, blank=True, null=True)
#     PhysicsfinalScore = models.CharField(max_length=252, blank=True, null=True)
#     Chemistry1Score = models.CharField(max_length=252, blank=True, null=True)
#     Chemistry2Score = models.CharField(max_length=252, blank=True, null=True)
#     ChemistryfinalScore = models.CharField(max_length=252, blank=True,null=True)
#     Jeemain1Score = models.CharField(max_length=252, blank=True, null=True)
#     Jeemain2Score = models.CharField(max_length=252, blank=True, null=True)
#     JeemainFinalScore = models.CharField(max_length=252, blank=True, null=True)
#     AIR = models.BigIntegerField(blank=True, null=True)
#     CategoryRank = models.BigIntegerField(blank=True, null=True)
#     def __str__(self):
#         return self.StudentDetail.Name
#     class Meta:
#         verbose_name = "Jee Mains Final Result"
#         verbose_name_plural = "Jee Mains Final Result"