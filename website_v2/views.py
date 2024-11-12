from django.shortcuts import render


def home(request):
    context = {
        "page_name": "Home",
    }
    return render(request, "pages/home.html", context)


def about(request):
    context = {
        "page_name": "About",
    }
    return render(request, "pages/about.html", context)


def services(request):
    context = {
        "page_name": "Services",
    }
    return render(request, "pages/services.html", context)


def countries(request):
    context = {
        "page_name": "Countries",
    }
    return render(request, "pages/countries.html", context)


# def team(request):
#     context = {
#         "page_name": "Our Team",
#     }
#     return render(request, "pages/team.html", context)


# def gallery(request):
#     context = {
#         "page_name": "Gallery",
#     }
#     return render(request, "pages/gallery.html", context)


def career(request):
    context = {
        "page_name": "Career",
    }
    return render(request, "pages/career.html", context)


def contact(request):
    context = {
        "page_name": "Contact",
    }
    return render(request, "pages/contact.html", context)


def custom_404(request, exception):
    context = {
        "page_name": "404",
    }
    return render(request, "pages/404.html", context, status=404)


def custom_403(request, exception):
    context = {
        "page_name": "403",
    }
    return render(request, "errors/403.html", context, status=403)
