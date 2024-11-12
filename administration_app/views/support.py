from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse

def support(request):
    return render(request,'support/support.html')