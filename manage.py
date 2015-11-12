#!/usr/bin/env python3
import os
import sys
import getpass
import shutil

DEFAULT_SETTINGS_MODULE = 'config.settings.local'


def create_default_settings_file(filename):
    print('creating local settings file for user: {username} '.format(username=username))
    src_path = "./config/settings/base_user.py"
    dst_path = "./config/settings/{filename}.py".format(username=username)
    shutil.copyfile(src_path, dst_path)

if __name__ == "__main__":

    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        settings_module = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_path = './' + settings_module.replace('.', '/') + '.py'

        if not os.path.exists(settings_path):
            create_default_settings_file(settings_path.split('/')[-2])
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

