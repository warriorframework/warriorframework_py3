from django.http import JsonResponse
from django.shortcuts import render
from katana.native.file_manager.file_manager_utils import backend
from katana.native.file_manager.file_manager_utils import ftp_utils
from katana.native.file_manager.file_manager_utils import scp_utils
from katana.native.file_manager.file_manager_utils.backend import getpath
import katana.utils.navigator_util
import os

def index(request):
    return render(request, "file_manager/file_manager.html", {})

def list_files(request):
    navigator = katana.utils.navigator_util.Navigator()
    return JsonResponse({"data": navigator.get_dir_tree_json(start_dir_path = getpath())})

def delete_files(request):
    file_path = request.GET.getlist('path[]')
    for paths in file_path:
        backend.delete(paths)
    return list_files(request)

def ftp_files(request):
    files_path = request.GET.getlist('path[]')
    all_files_path = request.GET.getlist('all_path[]')
    files_name = request.GET.getlist('file_name[]')
    username = request.GET.get('username')
    passwd = request.GET.get('password')
    host = request.GET.get('host')
    port = request.GET.get('port')
    port = int(port)
    destdir = request.GET.get('destdir')
    result = ftp_utils.ftpfile(host, port, username, passwd, destdir, files_path, files_name, all_files_path)
    return JsonResponse({"result": result})

def scp_files(request):
    files_path = request.GET.getlist('path[]')
    # all_files_path = request.GET.getlist('all_path[]')
    files_name = request.GET.getlist('file_name[]')
    username = request.GET.get('username')
    passwd = request.GET.get('password')
    host = request.GET.get('host')
    port = request.GET.get('port')
    port = int(port)
    destdir = request.GET.get('destdir')
    result = scp_utils.scpfile(host, port, username, passwd, destdir, files_path, files_name)
    return JsonResponse({"result": result})

def rename_files(request):
    file_path = request.GET.get('path')
    old_name = request.GET.get('file_name')
    new_name = request.GET.get('new_name')
    rename_result = backend.rename(file_path, old_name, new_name)
    return JsonResponse({"data": katana.utils.navigator_util.Navigator().get_dir_tree_json(start_dir_path = getpath()), "result": rename_result})

def save(request):
    username = request.GET.get('username')
    host = request.GET.get('host')
    port = request.GET.get('port')
    port = int(port)
    destdir = request.GET.get('destdir')
    transfer_proto = request.GET.get('transfer_protocol')
    file_name = request.GET.get('file_name')
    result = backend.save(file_name, username, host, port, destdir, transfer_proto)
    return JsonResponse({"result": result})

def cache_list(request):
    # This path will change to the cache directory
    path = os.path.join(getpath(),"File Manager/.data")
    try:
        return JsonResponse({"cache_list": os.listdir(path)})
    except:
        return JsonResponse({"cache_list": "error"})

def read_cache(request):
    cache_name = request.GET.get('cache_name')
    result = backend.read_cache(cache_name)
    return JsonResponse({"result": result})