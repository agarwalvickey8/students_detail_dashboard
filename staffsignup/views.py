from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import DisplayPreference, FieldHistory, NEETAdmitCard, NEETCityIn, RemarkStudents, Staff, StaffDetailTracking, StudentDetails
from .forms import LoginForm
from django.contrib.auth import logout as django_logout
from django.apps import apps
from django.utils import timezone
from pytz import timezone as pytz_timezone
def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = Staff.objects.get(Username=username)
                if password == user.Password:
                    request.session['user_id'] = user.id
                    if DisplayPreference.objects.get(staff=user).model_name == 'RemarkStudents':
                        return redirect('review_page')
                    else:
                        return redirect('student_list')
                else:
                    error_message = 'Invalid username or password'
            except Staff.DoesNotExist:
                error_message = 'Invalid username or password'
        else:
            error_message = 'Invalid form submission'
    else:
        form = LoginForm()
    return render(request, 'staffsignup/login.html', {'form': form, 'error_message': error_message})

def logout(request):
    django_logout(request)
    return redirect('/')

def review_page(request):
    if 'user_id' in request.session:
        next_student = RemarkStudents.objects.filter(remarks='').first()
        if next_student:
            neet_city_in_instance = NEETAdmitCard.objects.get(StudentDetail=next_student.StudentDetail)
            student_details_instance = next_student.StudentDetail
            # breakpoint()
            if request.method == 'POST':
                review_option = request.POST.get('review_option')
                if review_option in ['correct', 'incorrect', 'review_later']:
                    next_student.remarks = review_option
                    next_student.save()
                    # breakpoint()
                return redirect('review_page')
            context = {
                'neet_city_in_instance': neet_city_in_instance,
                'student_details_instance': student_details_instance,
            }
            # breakpoint()
            return render(request, 'staffsignup/review_page.html', context)
        else:
            return render(request, 'staffsignup/no_student_left.html',next_student)
    else:
        return redirect('/')
    
def student_list_view(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            staff = Staff.objects.get(id=user_id)
            student_details_data = None
            selected_model_name = None
            selected_model_class = None
            registration_number = request.GET.get('registration_number')
            roll_number = request.GET.get('roll_number')
            course = request.GET.get('course')
            batch = request.GET.get('batch')
            registration_number = registration_number or ''
            roll_number = roll_number or ''
            batch = batch or ''
            course = course or ''
            try:
                preference = DisplayPreference.objects.get(staff=staff)
                selected_model_name = preference.model_name
            except DisplayPreference.DoesNotExist:
                return render(request, 'staffsignup/login.html', {'error_message': 'Sorry, No Display Preference is assigned to you! Please conatact Gurukripa admin.'})
            selected_model_class = apps.get_model(app_label='staffsignup', model_name=selected_model_name)
            fields = []
            if registration_number or roll_number or course or batch:    
                if selected_model_name == 'StudentDetails':
                    student_details_data = StudentDetails.objects.filter(Branch=staff.Branch)
                else:
                    field_objects = [field for field in selected_model_class._meta.get_fields() if field.name not in ['id', 'StudentDetail'] ]
                    fields = [field.verbose_name for field in field_objects]
                    selected_model_class = selected_model_class.objects.filter(StudentDetail__Branch=staff.Branch)
                if registration_number:
                    if selected_model_name == 'StudentDetails':
                        student_details_data = student_details_data.filter(CoachingRegisteration=registration_number)
                    else:
                        selected_model_class = selected_model_class.filter(StudentDetail__CoachingRegisteration=registration_number)
                if roll_number:
                    if selected_model_name == 'StudentDetails':
                        student_details_data = student_details_data.filter(CoachingRoll=roll_number)
                    else:
                        selected_model_class = selected_model_class.filter(StudentDetail__CoachingRoll=roll_number)                    
                if course:
                    if selected_model_name == 'StudentDetails':
                        student_details_data = student_details_data.filter(Course=course)
                    else:
                        selected_model_class = selected_model_class.filter(StudentDetail__Course=course)
                if batch:
                    if selected_model_name == 'StudentDetails':
                        student_details_data = student_details_data.filter(Batch=batch)
                    else:
                        selected_model_class = selected_model_class.filter(StudentDetail__Batch=batch)                   
            else:
                selected_model_class = selected_model_class.objects.none() if selected_model_class else None
            all_courses = StudentDetails.objects.values_list('Course', flat=True).distinct()
            batch_options = {}
            for course in all_courses:
                batches = StudentDetails.objects.filter(Course=course).values_list('Batch', flat=True).distinct()
                batch_options[course] = list(batches)
            request.session['filter_params'] = {
                'course': course,
                'batch': batch,
                'registration_number': registration_number,
                'roll_number': roll_number,
            }
            staff_name = staff.Name
            return render(request, 'staffsignup/student_list.html', {
                'student_details_data': student_details_data,
                'selected_model_class': selected_model_class,
                'selected_model_name': selected_model_name,
                'registration_number':registration_number,
                'roll_number':roll_number,
                'course': course,
                'batch': batch,
                'batch_options': batch_options,
                'all_courses': all_courses,
                'fields': fields if selected_model_name != 'StudentDetails' else [],
                'staff_name': staff_name  
            })
        except Staff.DoesNotExist:
            return redirect('/')
    else:
        return redirect('/')
    
def get_batch_options(request):
    course = request.GET.get('course')
    if course:
        user_id = request.session.get('user_id')
        try:
            staff = Staff.objects.get(id=user_id)
            staff_branch = staff.Branch
            student_details = StudentDetails.objects.filter(Course=course, Branch=staff_branch)
            batches = student_details.values_list('Batch', flat=True).distinct()
            batch_options = list(batches)
            return JsonResponse(batch_options, safe=False)
        except Staff.DoesNotExist:
            return JsonResponse([], safe=False)
    else:
        return JsonResponse([], safe=False)

def update_field(request):
    if request.method == 'POST' and request.headers.get('X_REQUESTED_WITH') == 'XMLHttpRequest':
        registration_id = request.POST.get('registration_id')
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')
        selected_model_name = request.POST.get('selected_model_name')
        model_class = apps.get_model(app_label='staffsignup', model_name=selected_model_name)
        try:
            obj = model_class.objects.get(id=registration_id)
            all_fields_filled_before_update = all([getattr(obj, field.name) for field in model_class._meta.get_fields() if field.name not in ['id', 'StudentDetail']])
            old_value = getattr(obj, field_name)
            if field_value.strip():
                    setattr(obj, field_name, field_value)
            else:
                    setattr(obj, field_name, None)
            obj.save()
            student_detail = obj.StudentDetail
            coaching_roll = student_detail.CoachingRoll
            indian_timezone = pytz_timezone('Asia/Kolkata')
            indian_time = timezone.now().astimezone(indian_timezone)
            all_fields_filled_after_update = all([getattr(obj, field.name) for field in model_class._meta.get_fields() if field.name not in ['id', 'StudentDetail']])
            if all_fields_filled_after_update and not all_fields_filled_before_update:
                user_id = request.session.get('user_id')
                if user_id:
                    staff = Staff.objects.get(id=user_id)
                    tracking, created = StaffDetailTracking.objects.get_or_create(staff=staff)
                    tracking.details_added += 1
                    tracking.save()
            if not old_value and field_value.strip():
                user_id = request.session.get('user_id')
                if user_id:
                    staff = Staff.objects.get(id=user_id)
                    FieldHistory.objects.create(
                        staff=staff,
                        model_name=selected_model_name,
                        field_name=field_name,
                        old_value = None,
                        new_value=field_value,
                        action='add',
                        timestamp=indian_time,
                        coaching_roll=coaching_roll,
                    )
            elif old_value != field_value:
                user_id = request.session.get('user_id')
                if user_id:
                    staff = Staff.objects.get(id=user_id)
                    FieldHistory.objects.create(
                        staff=staff,
                        model_name=selected_model_name,
                        field_name=field_name,
                        old_value=old_value,
                        new_value=field_value,
                        action='edit',
                        timestamp=indian_time,
                        coaching_roll=coaching_roll,
                    )
            return JsonResponse({'success': True})
        except model_class.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'{selected_model_name} not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or not AJAX'})