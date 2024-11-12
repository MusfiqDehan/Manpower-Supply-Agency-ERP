from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from ..models import Passenger


@login_required
def all_passport(request):
    user_group = request.user.Group_Users.all().first()

    if request.user.is_superuser:
        passenger_list = Passenger.objects.all()
        context = {
            "passport_nav_link_status": "active",
            "passenger_list": passenger_list,
        }
        return render(request, "all_passport/passport.html", context)
    else:
        if user_group is None:
            return render(request, "errors/403.html")
        else:
            group_permissions = user_group.permissions.all()
            for perm in group_permissions:
                if perm.codename == "view_passport":
                    passenger_list = Passenger.objects.all()
                    context = {"passenger_list": passenger_list}
                    return render(request, "all_passport/passport.html", context)
            return render(request, "errors/403.html")


@login_required
def search_passport(request):
    data = {}
    user_group = request.user.Group_Users.all().first()

    if request.user.is_superuser:
        search_value = request.GET.get("search_value")
        passport_search_list = Passenger.objects.filter(
            passport__icontains=search_value
        )
        context = {"passenger_list": passport_search_list}
        data["search_list"] = render_to_string(
            "all_passport/passport_list.html", context
        )
        return JsonResponse(data)
    else:
        if user_group is None:
            return render(request, "errors/403.html")
        else:
            group_permissions = user_group.permissions.all()
            for perm in group_permissions:
                if perm.codename == "search_passport":
                    search_value = request.GET.get("search_value")
                    passport_search_list = Passenger.objects.filter(
                        passport__icontains=search_value
                    )
                    context = {"passenger_list": passport_search_list}
                    data["search_list"] = render_to_string(
                        "all_passport/passport_list.html", context
                    )
                    return JsonResponse(data)
            return render(request, "errors/403.html")
