
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.urls import reverse

from django.contrib.auth.forms import SetPasswordForm
from django.http import JsonResponse



# =========================== SuperUser view ==================
@login_required
def all_superusers(request):
    User = get_user_model()
    all_superusers = User.objects.filter(is_superuser=True)

    context = {
        "all_superusers": all_superusers,
        "user": request.user,
    }
    return render(request, "superusers/superusers.html", context)




# ===================== SuperUser Create =========Not used=================
@login_required
def create_superuser(request):
    return render(request, 'Authentication/create_superuser.html')



# ====================== Password Change ==========Not Used====================
def change_password(request):
    data = dict()

    if request.method == 'POST':
        email = request.POST.get('user_email')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if new_password == confirm_new_password:
            user = get_user_model().objects.get(email=email)

            # Create a password change form with the new password
            form = SetPasswordForm(user, {'new_password1': new_password, 'new_password2': confirm_new_password})
         
            if form.is_valid():
                # Save the new password
                user.set_password(new_password)
                user.save()
                # Log in the user with the new password
             
                login(request, user)
                data['password_change_form_is_valid'] = True
            else:
                data['form_errors'] = form.errors.as_json()
        else:
            data['password_mismatch'] = True

    return JsonResponse(data)

    
    



