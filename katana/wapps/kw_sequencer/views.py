from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views import View
import os

from utils.navigator_util import Navigator
from wapps.kw_sequencer.kw_sequencer_utils.get_drivers import GetDriversActions
from wapps.kw_sequencer.kw_sequencer_utils.write_wrapper_kw import CreateWrappeKwActions

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

def save_wrapper_kw(request):
    " Saves wrapper keyword in the respective Warrior Action file "
    output = {'status': True}
    action_file = os.path.join(navigator.get_warrior_dir()[:-1], request.POST.get("@actionFile"))
    wrapper_kw_name = request.POST.get("@wrapperKwName")
    w_desc = request.POST.get("@wDescription")
    sub_keywords = request.POST.get("@subKeywords")

    cwk_obj = CreateWrappeKwActions(action_file, wrapper_kw_name, w_desc, sub_keywords)
    cwk_obj.write_wrapper_kw()

    return JsonResponse(output)
