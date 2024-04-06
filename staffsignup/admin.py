from django.contrib import admin, messages
from staffsignup.models import Branch, DisplayPreference, NEETRegistration, Staff, StudentDetails, JEEMAIN1Registration
from django import forms
from django.http import HttpResponseRedirect
import pandas as pd
from django.urls import path
from django.contrib import admin
import re
admin.site.site_header = 'Gurukripa  Administration'

class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')  # Show the Branch ID and Name in the list
    search_fields = ('id', 'Name')  # Enable searching by Branch ID and Name


class DisplayPreferenceForm(forms.ModelForm):
    model_name = forms.ChoiceField(choices=[], label='Model Name')
    def __init__(self, *args, **kwargs):
        super(DisplayPreferenceForm, self).__init__(*args, **kwargs)
        self.fields['model_name'].choices = self.get_model_choices()

    def get_model_choices(self):
        model_choices = [('StudentDetails', 'StudentDetails')]
        related_models = [
            field.related_model._meta.object_name for field in StudentDetails._meta.get_fields()
            if field.one_to_many or field.one_to_one
        ]
        for model_name in related_models:
            model_choices.append((model_name, model_name))
        return model_choices


class DisplayPreferenceAdmin(admin.ModelAdmin):
    form = DisplayPreferenceForm

    def staff_username(self, obj):
        return obj.staff.Username  # Assuming the username field is named 'Username' in the Staff model

    staff_username.short_description = 'Staff Username'  # Optional: Customize the column header

    list_display = ('staff_username', 'model_name')
    
class StudentDetailsAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.upload_excel, name='upload_excel'),
        ]
        return custom_urls + urls

class StudentDetailsAdmin(admin.ModelAdmin):
    def extract_phone_number(self, raw_number):
        if pd.notnull(raw_number):
            raw_number_str = str(raw_number)
            if '.' in raw_number_str:
                # If raw number is a floating-point number, remove the decimal part
                raw_number_str = raw_number_str.split('.')[0]
            digits_only = re.sub(r'\D', '', raw_number_str)
            if len(digits_only) >= 10:
                last_10_digits = digits_only[-10:]
                return last_10_digits
        return None


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.upload_excel, name='upload_excel'),
        ]
        return custom_urls + urls
    mandatory_fields = ["Registration Number", "Roll number","Primary Mobile Number", "Student's Name", "Primary Mobile Number", "Course", "Course ID", "Batch", "Exam", "Branch_id"]
    def upload_excel(self, request):
        if request.method == 'POST' and request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)
                success_count = 0
                error_count = 0
                for index, row in df.iterrows():
                    pincode = row["PIN Code"]
                    if pd.notnull(pincode):
                        pincode = int(pincode) if isinstance(pincode, float) else pincode
                    dob = row["Date Of Birth"]
                    if pd.notnull(dob) and not pd.isna(dob):
                        dob = row["Date Of Birth"]
                    else:
                        dob = None
                    branch_name = row["Branch_id"]
                    try:
                        branch = Branch.objects.get(Name = branch_name)
                        branch_id = branch.id
                    except Branch.DoesNotExist:
                        branch_id = None
                    missing_fields = [field for field in self.mandatory_fields if pd.isnull(row[field])]
                    if missing_fields:
                        error_count += 1
                        error_message = f"Error processing row {index + 1}: Missing mandatory fields: {', '.join(missing_fields)}"
                        messages.error(request, error_message)
                        continue
                    try:
                        student = StudentDetails.objects.create(
                            CoachingRegisteration = row["Registration Number"],
                            CoachingRoll = row["Roll number"],
                            Name = row["Student's Name"],
                            FatherName = row["Father's Name"],
                            MotherName = row["Mother's Name"],
                            PrimaryNumber=self.extract_phone_number(row["Primary Mobile Number"]),
                            SecondaryNumber=self.extract_phone_number(row["Secondary Mobile Number"]),
                            AdditionalNumber=self.extract_phone_number(row["Addition Mobile Number"]),
                            WhatsappNumber=self.extract_phone_number(row["WhatsApp Number"]),
                            Course = row["Course"],
                            CourseId = row["Course ID"],
                            Batch = row["Batch"],
                            Medium = row["Medium"],
                            DOB = dob,
                            Gender = row["Gender"],
                            Category = row["Category"],
                            Address = row["Permanent Address"],
                            Tehsil = row["Tehsil"],
                            District = row["District"],
                            State = row["State"],
                            Pincode = pincode,
                            PreviousRoll = row["Previous GCI Roll Number"],
                            Exam = row["Exam"],
                            Branch_id = branch_id,
                        )
                        success_count += 1
                    except Exception as e:
                        error_count += 1
                        messages.error(request, f"Error processing row {index + 1}: {str(e)}")
                if success_count > 0:
                    messages.success(request, f"{success_count} student(s) added successfully.")
                if error_count > 0:
                    messages.warning(request, f"{error_count} student(s) encountered errors.")
            except Exception as e:
                messages.error(request, f"Error reading Excel file: {str(e)}")
        return HttpResponseRedirect('../')

class NEETRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'NEETApplication', 'Mobile')

    def student_name(self, obj):
        return obj.StudentDetail.Name
    
class JEEMAIN1RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'JEEMAIN1Application', 'Mobile')
    def student_name(self, obj):
        return obj.StudentDetail.Name
class StaffAddForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['Username', 'Password']

class StaffEditForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

class StaffAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Branch', 'Username', 'Password']
    readonly_fields = ['Username']

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['form'] = StaffEditForm
        else:
            kwargs['form'] = StaffAddForm
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return super().get_fieldsets(request, obj)
        else:
            return [(None, {'fields': ['Name', 'Branch']})]

admin.site.register(Staff, StaffAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(StudentDetails, StudentDetailsAdmin)
admin.site.register(DisplayPreference, DisplayPreferenceAdmin)
admin.site.register(NEETRegistration, NEETRegistrationAdmin)
admin.site.register(JEEMAIN1Registration, JEEMAIN1RegistrationAdmin)
# admin.site.unregister(Group)