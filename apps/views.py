from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import Error   # db 접근
def index(request):
    num_errors = Error.objects.all().count()
    context ={
        'num_errors': num_errors,
    }
    # return HttpResponse("Hellow world!!123")
    return render(request, 'mainsite.html', context=context)