from django.shortcuts import render
from django.views import View


class RequestAnAppView(View):

    template = 'request_an_app/index.html'

    def get(self, request):
        """
        Get Request Method
        """
        return render(request, RequestAnAppView.template, {})
