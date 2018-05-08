from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views import View

from utils.navigator_util import Navigator
from wapps.kw_sequencer.kw_sequencer_utils.get_drivers import GetDriversActions

navigator = Navigator()

class KwSequencerIndex(TemplateView):
    template_name = 'kw_sequencer/kw_sequencer.html'

class KwSequencerCreate(View):

    def get(self, request):
        return render(request, 'kw_sequencer/create_kw.html')

def create_new_subkw(request):
    """ Creates new sub keyword """
    output = {}
    da_obj = GetDriversActions(navigator.get_warrior_dir()[:-1])
    output["drivers"] = da_obj.get_all_actions()
    output["html_data"] = render_to_string('kw_sequencer/create_subkw.html', output)
    return JsonResponse(output)
