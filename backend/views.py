from django.shortcuts import render,HttpResponse
from turtle import title

# Create your views here.
def dashboard(request):
    context={
        'title':title
    }
    return render(request, 'dashboard.html', context)
