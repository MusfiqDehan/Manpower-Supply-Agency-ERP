from django.shortcuts import render
from django.contrib.auth.decorators import login_required


app_name = 'adminstration_app'

@login_required
def admin_view(request):
    return render(request, "administration/administration.html")
