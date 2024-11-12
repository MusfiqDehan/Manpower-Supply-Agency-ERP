from django.urls import path
from visa_management_app.views import visa_manage


#App Name
app_name = 'visa_management_app'

urlpatterns = [
    path('', visa_manage.VisaManage, name='visa-manage'),
    path('create/', visa_manage.Visa_create, name='visa_create'),

    path('visa_edit/<pk>', visa_manage.visa_edit, name='visa_edit'),
    path('visa_delete/<pk>', visa_manage.visa_delete, name='visa_delete'),
]
