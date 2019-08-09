from django.shortcuts import render

# Create your views here.
from django.views import View

class NewAppClass(View):
    def get(self, request):
        return render(request, 'wavelength_validation_tool/index.html', context={})
    def post(self, request):
        return render(request, 'wavelength_validation_tool/index.html', context={})
