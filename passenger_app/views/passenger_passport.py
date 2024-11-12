from django.shortcuts import render, redirect
from passenger_app.forms import PassportSubmitForm, PassportImageForm
from passenger_app.models import PassengerPassport, Passenger
from django.contrib.auth.decorators import login_required
import json
from django.template.loader import render_to_string
from django.http import JsonResponse


# def save_image(request, form, passenger_id, passport, template_name):
#     data = dict()
#     if request.method == 'POST':
#         print("post called")
#         if form.is_valid():
#             print("data validation successful")
#             form.save()
#             print("data saved successfully")
#             data['form_is_valid'] = True
#             data['html_image_div'] = render_to_string('passenger_app_templates/passenger_details/passport/image_card.html', {
#                'passenger_passport': passport,
#                'user': request.user,
#             }

#             )
#             data['html_images']=render_to_string('passenger_app_templates/passenger_details/passport_image.html',{
#                'passenger_passport': passport,
#                'user': request.user,
#             })
#             data['html_modal_images']=render_to_string('passenger_app_templates/passenger_details/passport_ajax_image.html',{
#                'passenger_passport': passport,
#                'user': request.user,
#             })
#             return JsonResponse(data)

#         else:
#             form.errors()
#             data['form_is_valid'] = False
#             return JsonResponse(data)
#     context = {
#         'form': form,
#         'passenger_id': passenger_id,
#         'passport': passport,
#         'user': request.user,

#         }

#     data['html_form'] = render_to_string(template_name, context, request= request)
#     return JsonResponse(data)


# @login_required
# def passport_image_add(request, passenger_id):
#     print("passenger:", passenger_id)

#     passenger = Passenger.objects.get(id=passenger_id)
#     print("passenger is ", passenger)


#     passport = passenger.passport_info_passenger.all().first()


#     if request.method == 'POST':
#         form = PassportImageForm(request.POST, request.FILES, instance=passport)

#     else:
#         passenger_id = passenger_id
#         form = PassportImageForm()

#     return save_image(request, form, passenger_id, passport,'passenger_app_templates/passenger_details/passport/no_image.html')


@login_required
def passport_image_add(request, passenger_id):
    data = dict()
    passenger = Passenger.objects.get(id=passenger_id)
    passport = passenger.passport_info_passenger.all().first()

    if request.method == "POST":
        form = PassportImageForm(request.POST, request.FILES, instance=passport)
        if form.is_valid():
            form.save()

            data["form_is_valid"] = True
            data["html_image_div"] = render_to_string(
                "passenger_app_templates/passenger_details/passport/image_card.html",
                {
                    "passenger_passport": passport,
                    "user": request.user,
                },
            )

            data["html_images"] = render_to_string(
                "passenger_app_templates/passenger_details/passport_image.html",
                {
                    "passenger_passport": passport,
                    "user": request.user,
                },
            )
            data["html_modal_images"] = render_to_string(
                "passenger_app_templates/passenger_details/passport_ajax_image.html",
                {
                    "passenger_passport": passport,
                    "user": request.user,
                },
            )
            return JsonResponse(data)
        else:
            data["form_is_valid"] = False
            return JsonResponse(data)
    else:
        form = PassportImageForm()

    context = {
        "form": form,
        "passenger_id": passenger_id,
        "passport": passport,
        "user": request.user,
    }

    data["html_form"] = render_to_string(
        "passenger_app_templates/passenger_details/passport/no_image.html",
        context,
        request=request,
    )
    return JsonResponse(data)
