from django.contrib import admin
from passenger_app.models import (
    Passenger,
    PassengerTransaction,
    PassengerPassport,
    PassengerDocument,
    PassengerGeneralDocument,
)


admin.site.register(Passenger)
admin.site.register(PassengerPassport)
admin.site.register(PassengerTransaction)
admin.site.register(PassengerDocument)
admin.site.register(PassengerGeneralDocument)
