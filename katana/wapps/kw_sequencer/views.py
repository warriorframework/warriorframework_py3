import json

from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View

from utils.navigator_util import Navigator
from wapps.kw_sequencer.kw_sequencer_utils.get_drivers import GetDriversActions
from wapps.kw_sequencer.kw_sequencer_utils.write_wrapper_kw import CreateWrappeKwActions

navigator = Navigator()
WARRIOR_DIR = navigator.get_warrior_dir()[:-1]

class KwSequencerIndex(View):

    def get(self, request):
        """ Get Method """
        return render(request, 'kw_sequencer/kw_sequencer.html')

class KwSequencerCreate(View):

    def get(self, request):
        """ Get Method """
        return render(request, 'kw_sequencer/create_kw.html')

def create_new_subkw(request):
    """ Creates new sub keyword """
    output = {}
    da_obj = GetDriversActions(WARRIOR_DIR)
    output["drivers"] = da_obj.get_all_actions()
    output["html_data"] = render_to_string('kw_sequencer/create_subkw.html', output)
    return JsonResponse(output)

def save_wrapper_kw(request):
    """ Saves wrapper keyword in the respective Warrior Action file """
    output = {}
    action_file = request.POST.get("@actionFile")
    wrapper_kw_name = request.POST.get("@wrapperKwName")
    w_desc = request.POST.get("@wDescription")
    sub_keywords = request.POST.get("@subKeywords")
    sub_keywords = json.loads(sub_keywords)
    wka_obj = CreateWrappeKwActions(WARRIOR_DIR)
    output['status'], output['message'] = wka_obj.write_wrapper_kw(action_file, wrapper_kw_name,
                                                                   w_desc, sub_keywords)
    return JsonResponse(output)
