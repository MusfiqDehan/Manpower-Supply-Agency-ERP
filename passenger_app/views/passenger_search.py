
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from passenger_app.models import Passenger

@login_required
def passenger_search(request):
    data=dict()
    search_value=request.GET.get('search_value')

    passenger_search_list=(Passenger.objects.filter(passport__icontains=search_value) | 
                    Passenger.objects.filter(full_name__icontains=search_value) |
                    Passenger.objects.filter(phone_number__icontains=search_value))
    context={'passenger_list':passenger_search_list, 'user': request.user,}
    data['passenger_search_list']=render_to_string('passenger_app_templates/passenger_management/passenger_list.html',context)
    return JsonResponse(data)