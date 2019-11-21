# -*- coding: utf-8 -*-

import json
from django.apps import AppConfig
from katana.utils.directory_traversal_utils import get_abs_path, join_path
from katana.utils.json_utils import read_json_data
from katana.utils.navigator_util import Navigator
from katana.wui.core.core_utils.app_info_class import AppInformation
from katana.wui.core.core_utils.apps_class import Apps
from katana.wui.core.core_utils.core_index_class_utils import CoreIndex
from katana.wui.core.core_utils.core_utils import validate_config_json
import os
import shutil

class CoreConfig(AppConfig):
    name = 'katana.wui.core'
    verbose_name = "Core Katana"

    def copy(self, src):
        dir_lis=[x[0] for x in os.walk(src)]
        for fol in dir_lis:
            path= 'Warriorspace'+fol.split('Warriorspace')[1]
            if not os.path.exists(path):
                os.mkdir(path)
            lis_dir = os.listdir(fol)
            for fileordir in lis_dir:
                if os.path.isfile(fol+'/'+fileordir) and not os.path.exists(path+'/'+fileordir):
                    shutil.copyfile(fol+'/'+fileordir, path+'/'+fileordir)

    def ready(self):
        """
        The ready function is trigger only on events like server start up and server reload
        """
        # print "***************You are in Core Katana App Config Class***************"
        nav_obj = Navigator()
        env_path = "/".join(os.environ['_'].split("/")[:-2])
        source_warriorspace = env_path + '/lib/python3.6/site-packages/warrior/Warriorspace'
        self.copy(source_warriorspace)
        base_directory = nav_obj.get_katana_dir()
        warrior_dir = nav_obj.get_warrior_dir()
        config_file_name = "wf_config.json"
        config_json_file = join_path(base_directory, "config.json")
        settings_file_path = get_abs_path(join_path("wui", "settings.py"), base_directory)
        core_index_obj = CoreIndex(base_directory, settings_file_path=settings_file_path)

        available_apps = core_index_obj.get_available_apps()
        settings_apps = core_index_obj.get_apps_from_settings_file()

        AppInformation.information = Apps()

        AppInformation.information.set_apps({'base_directory': base_directory,
                                             'config_file_name': config_file_name,
                                             'available_apps': available_apps,
                                             'settings_apps': settings_apps})

        ordered_json = validate_config_json(read_json_data(config_json_file), warrior_dir)
        with open(config_json_file, "w") as f:
            f.write(json.dumps(ordered_json, indent=4))

        # print "***************You are in Core Katana App Config Class***************"
