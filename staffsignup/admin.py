from django.contrib import admin, messages
from staffsignup.models import Branch, DisplayPreference, NEETRegistration, Staff, StudentDetails, JEEMAIN1Registration
from django import forms
from django.http import HttpResponseRedirect
import pandas as pd
from django.urls import path

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
    list_display = ('staff', 'model_name')

class StudentDetailsAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.upload_excel, name='upload_excel'),
        ]
        return custom_urls + urls

class StudentDetailsAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.upload_excel, name='upload_excel'),
        ]
        return custom_urls + urls

    def upload_excel(self, request):
        if request.method == 'POST' and request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)
                success_count = 0
                error_count = 0
                for index, row in df.iterrows():
                    try:
                        student = StudentDetails.objects.create(
                            CoachingRegisteration=row['Registration Number'],
                            CoachingRoll=row['Roll number'],
                            Name=row["Student's Name"],
                            FatherName=row["Father's Name"],
                            MotherName=row["Mother's Name"],
                            Course=row['Course'],
                            CourseId=row['Course ID'],
                            Batch=row['Batch'],
                            Medium=row['Medium'],
                            DOB=row['Date Of Birth'],
                            Gender=row['Gender'],
                            Category=row['Category'],
                            Address=row['Permanent Address'],
                            Tehsil=row['Tehsil'],
                            District=row['District'],
                            State=row['State'],
                            PreviousRoll=row["Previous GCI Roll No"],
                            CourseType=row['CourseType'],
                            Branch_id=row['Branch_id'],
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

admin.site.register(Branch)
admin.site.register(StudentDetails, StudentDetailsAdmin)
admin.site.register(Staff)
admin.site.register(DisplayPreference, DisplayPreferenceAdmin)
admin.site.register(NEETRegistration, NEETRegistrationAdmin)
admin.site.register(JEEMAIN1Registration, JEEMAIN1RegistrationAdmin)