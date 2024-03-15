from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import DisplayPreference, Staff, StudentDetails, NEETRegistration
from .forms import LoginForm, NEETRegistrationForm
from django.contrib.auth import logout as django_logout
from urllib.parse import urlencode
from django.urls import reverse

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

def student_list_view(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            staff = Staff.objects.get(id=user_id)
            student_details_data = None
            neet_registeration_data = None
            selected_model_name = None
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
                pass
            if selected_model_name == 'NEETRegistration':
                neet_registeration_data = NEETRegistration.objects.filter(StudentDetail__Branch=staff.Branch)
            else:
                student_details_data = StudentDetails.objects.filter(Branch=staff.Branch)
            if registration_number:
                if selected_model_name == 'NEETRegistration':
                    neet_registeration_data = neet_registeration_data.filter(StudentDetail__CoachingRegisteration=registration_number)
                else:
                    student_details_data = student_details_data.filter(CoachingRegisteration=registration_number)
            if roll_number:
                if selected_model_name == 'NEETRegistration':
                    neet_registeration_data = neet_registeration_data.filter(StudentDetail__CoachingRoll=roll_number)
                else:
                    student_details_data = student_details_data.filter(CoachingRoll=roll_number)
            if course:
                if selected_model_name == 'NEETRegistration':
                    neet_registeration_data = neet_registeration_data.filter(StudentDetail__Course=course)
                else:
                    student_details_data = student_details_data.filter(Course=course)
            if batch:
                if selected_model_name == 'NEETRegistration':
                    neet_registeration_data = neet_registeration_data.filter(StudentDetail__Batch=batch)
                else:
                    student_details_data = student_details_data.filter(Batch=batch)
            batch_options = []
            if course:
                if course == "Spartan Batch":
                    batch_options = ["FE4", "Batch2", "Batch3"]
                elif course == "Course2":
                    batch_options = ["Batch4", "Batch5", "Batch6"]
                elif course == "Course3":
                    batch_options = ["Batch7", "Batch8", "Batch9"]
            request.session['filter_params'] = {
                'course': course,
                'batch': batch,
                'registration_number': registration_number,
                'roll_number': roll_number,
            }
            return render(request, 'staffsignup/student_list.html', {
                'student_details_data': student_details_data,
                'neet_registeration_data': neet_registeration_data,
                'selected_model_name': selected_model_name,
                'registration_number':registration_number,
                'roll_number':roll_number,
                'course': course,
                'batch': batch,
                'batch_options': batch_options,
            })
        except Staff.DoesNotExist:
            return redirect('/')
    else:
        return redirect('/')

def edit_neet_registration(request, neet_registration_id):
    neet_registration = get_object_or_404(NEETRegistration, pk=neet_registration_id)
    if request.method == 'POST':
        form = NEETRegistrationForm(request.POST, instance=neet_registration)
        if form.is_valid():
            form.save()
            filter_params = request.session.get('filter_params', {})
            redirect_url = reverse('student_list') + '?' + urlencode(filter_params)
            return redirect(redirect_url)
    else:
        form = NEETRegistrationForm(instance=neet_registration)
    return render(request, 'edit_neet_registration.html', {'form': form})

def logout(request):
    django_logout(request)
    return redirect('/')

def update_neet_application(request):
    if request.method == 'POST' and request.headers.get('X_REQUESTED_WITH') == 'XMLHttpRequest':
        registration_id = request.POST.get('registration_id')
        neet_application = request.POST.get('neet_application')

        try:
            neet_registration = NEETRegistration.objects.get(id=registration_id)
            if neet_application.strip():
                neet_registration.NEETApplication = neet_application
            else:
                neet_registration.NEETApplication = None 
            neet_registration.save()
            return JsonResponse({'success': True})
        except NEETRegistration.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'NEETRegistration not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or not AJAX'})

def update_mobile(request):
    if request.method == 'POST' and request.headers.get('X_REQUESTED_WITH') == 'XMLHttpRequest':
        registration_id = request.POST.get('registration_id')
        mobile = request.POST.get('mobile')
        
        try:
            neet_registration = NEETRegistration.objects.get(id=registration_id)
            if mobile.strip():
                neet_registration.Mobile = mobile
            else:
                neet_registration.Mobile = None
            neet_registration.save()
            return JsonResponse({'success': True})
        except NEETRegistration.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'NEETRegistration not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or not AJAX'})