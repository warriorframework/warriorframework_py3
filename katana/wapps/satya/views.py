from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.template import loader, RequestContext

def index(request):
    print("Satya App Index here!!!!")
    template = loader.get_template("satya/satyaApp.html")
    context = {
        'title' : 'Satya App'
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello, World!!!")