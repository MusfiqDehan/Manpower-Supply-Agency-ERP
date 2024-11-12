from django.shortcuts import render
from passenger_app.forms import TrackingForm, PassportEditForm
from passenger_app.models import PassengerPassport , Passenger
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse




#create passenger document
def save_tracking_form(request, form, passenger_id,passport, template_name):
    
    data = dict()
    
    if request.method == 'POST':
        
        if form.is_valid():
         
            form.save()
            
            data['form_is_valid'] = True
            
            data['html_tracking_steps'] = render_to_string('passenger_app_templates/passenger_details/passport/tracking_steps.html', {
                'passenger_passport': passport,
                'user': request.user,
                })
            data['html_steps_script'] = render_to_string('passenger_app_templates/passenger_details/passport/steps_script.html')
            
            return JsonResponse(data)
            
        else:
           
            data['form_is_valid'] = False
            return JsonResponse(data)

    context = {
        'form': form,
        'passenger_id': passenger_id,
        'passport': passport,
        'user': request.user,
     
        }
    
    data['html_form'] = render_to_string(template_name, context, request= request)
    return JsonResponse(data)

@login_required
def passport_tracking_update(request, passenger_id):
    passenger = Passenger.objects.get(id=passenger_id)
  
    passport = passenger.passport_info_passenger.all().first()
   

    if request.method == 'POST':  
        form = TrackingForm(request.POST, instance=passport)
        
    else:
        passenger_id = passenger_id
        form = TrackingForm()
    
    return save_tracking_form(request, form,  passenger_id, passport, 'passenger_app_templates/passenger_details/passport/track_update.html')

# passport edit
def save_passport_edit_form(request, form, passenger_id,passport, template_name):
    
    data = dict()
    
    if request.method == 'POST':
        
        if form.is_valid():
          
            instance = form.save(commit=False)
            
            instance.save()

            # this is to update the passenger model passport info according to passenegrpassport model
            passenger_id = request.POST.get('passenger_passport')
            passenger = Passenger.objects.get(id=passenger_id)
            
            passenger.passport=instance.passport_number
            passenger.passport_date_of_expairy=instance.date_of_expairy
            passenger.save()
            
           
            data['form_is_valid'] = True
            data['html_header'] = render_to_string('passenger_app_templates/passenger_details/passport/header.html', {
                'passenger_passport': passport,
                'user': request.user,
                
           })
            data['html_passport_info'] = render_to_string('passenger_app_templates/passenger_details/passport/passport_info_div.html', {
                'passenger_passport': passport,
                'user': request.user,
                
           })
            
            return JsonResponse(data)
            
        else:
           
            data['form_is_valid'] = False
            return JsonResponse(data)

    context = {
        'form': form,
        'passenger_id': passenger_id,
        'passport': passport,
        'user': request.user,
     
        }
    
    data['html_form'] = render_to_string(template_name, context, request= request)
    return JsonResponse(data)


@login_required
def passport_edit(request, passenger_id):
    passenger = Passenger.objects.get(id=passenger_id)
    passport = passenger.passport_info_passenger.all().first()
    
    if request.method == 'POST':  
        form = PassportEditForm(request.POST, instance=passport)
        
    else:
        passenger_id = passenger_id
        form = PassportEditForm()
    
    return save_passport_edit_form(request, form,  passenger_id, passport, 'passenger_app_templates/passenger_details/passport/edit_passport.html')
