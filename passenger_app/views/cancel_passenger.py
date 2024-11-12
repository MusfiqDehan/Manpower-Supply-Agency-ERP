from django.shortcuts import render
from passenger_app.models import Passenger
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError


@login_required
def cancel_passengers(request):
    user_group = request.user.Group_Users.all().first()
    if request.user.is_superuser:
        try:
            cancel_passenger_list = Passenger.objects.filter(
                cancel_status=True
            ).order_by("-id")
        except DatabaseError as e:
            # Handle the database error here,
            pass

        context = {
            "page_name": "Rejected Passengers",
            "cancel_passenger_nav_link_status": "active",
            "cancel_passenger_list": cancel_passenger_list,
            "user": request.user,
        }

        return render(
            request,
            "cancel_passenger_management/cancel_passengers.html",
            context,
        )
    else:
        if user_group is None:
            return render(request, "errors/403.html")
        else:
            group_permissions = user_group.permissions.all()
            for perm in group_permissions:
                if perm.codename == "rejected_passenger_view":
                    try:
                        cancel_passenger_list = Passenger.objects.filter(
                            cancel_status=True
                        ).order_by("-id")
                    except DatabaseError as e:
                        # Handle the database error here,
                        pass

                    context = {
                        "page_name": "Rejected Passengers",
                        "cancel_passenger_nav_link_status": "active",
                        "cancel_passenger_list": cancel_passenger_list,
                        "user": request.user,
                    }

                    return render(
                        request,
                        "cancel_passenger_management/cancel_passengers.html",
                        context,
                    )
            return render(request, "errors/403.html")
