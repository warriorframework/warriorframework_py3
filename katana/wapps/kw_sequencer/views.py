from django.shortcuts import render
from django.views.generic import TemplateView


class KwSequencerIndex(TemplateView):
    template_name = 'kw_sequencer/kw_sequencer.html'
