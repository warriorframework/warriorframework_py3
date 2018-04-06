from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

class KwSequencerIndex(TemplateView):
    template_name = 'kw_sequencer/kw_sequencer.html'

class KwSequencerCreate(View):

    def get(self, request):
        return render(request, 'kw_sequencer/create_kw.html')
