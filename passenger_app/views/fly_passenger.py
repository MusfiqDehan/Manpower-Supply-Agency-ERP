from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError

from passenger_app.models import Passenger


@login_required
def fly_passengers(request):
    user_group = request.user.Group_Users.all().first()
    if request.user.is_superuser:
        try:
            fly_passenger_list = Passenger.objects.filter(fly_status=True).order_by(
                "-id"
            )
        except DatabaseError as e:
            # Handle the database error here,
            pass

        context = {
            "page_name": "Successful Passengers",
            "successful_passenger_nav_link_status": "active",
            "fly_passenger_list": fly_passenger_list,
            "user": request.user,
        }

        return render(
            request,
            "fly_passenger_management/fly_passengers.html",
            context,
        )
    else:
        if user_group is None:
            return render(request, "errors/403.html")
        else:
            group_permissions = user_group.permissions.all()
            for perm in group_permissions:
                if perm.codename == "successful_passenger_view":
                    try:
                        fly_passenger_list = Passenger.objects.filter(
                            fly_status=True
                        ).order_by("-id")
                    except DatabaseError as e:
                        # Handle the database error here,
                        pass

                    context = {
                        "page_name": "Successful Passengers",
                        "successful_passenger_nav_link_status": "active",
                        "fly_passenger_list": fly_passenger_list,
                        "user": request.user,
                    }

                    return render(
                        request,
                        "fly_passenger_management/fly_passengers.html",
                        context,
                    )
            return render(request, "errors/403.html")
