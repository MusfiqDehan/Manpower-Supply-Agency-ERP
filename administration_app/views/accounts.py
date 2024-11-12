from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.urls import reverse

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse





# =================================== Employee Authentication ==========================================

# User Login 
def user_login(request):
    data = dict()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():            
            email = form.cleaned_data.get('username')           
            password = form.cleaned_data.get('password')

            login_user = authenticate(request, email=email, password=password)
            if login_user is not None:
                login(request, login_user)
                data['form_is_valid'] = True 
                next_value = request.POST.get('post_next_value')
                data['ajax_next_value'] = next_value

                # Add role-based redirection logic here( or user.has_perm('some_permission'))
                if login_user.is_superuser:
                    data['redirect_url'] = '/erp/home/'  # Replace with the URL for the Root dashboard view.
                
                else:
                    data['redirect_url'] = '/erp/home/' 
                 
                    # data['redirect_url'] = f"/employee/employee-details/{id}/view/" # Replace with the URL for the employee profile view.
                
                return JsonResponse(data)
        else:
           
            data['login_error'] = render_to_string('Authentication/user_login_error.html', {})
            
            return JsonResponse(data)
    else:
        next_value = request.GET.get('next')
        
        if next_value:
            return render(request, 'Authentication/login.html', {"next_value": next_value})
        else:
            return render(request, 'Authentication/login.html')




# User Logout
@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('administration_app:user_login')
    else:
        return redirect(request.path_info)







    



