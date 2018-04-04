from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, "index.html")

def selected(request):
    return render(request, "selected.html")

def schedule(request):
    return render(request, "schedule.html")

def toolbox(request):
    return render(request, "toolbox.html")