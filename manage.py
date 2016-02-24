#!/usr/bin/env python
import os
import sys
import getpass
import shutil


def create_default_settings_filed(flavor):
    print('creating local settings file for flavor: {flavor} '.format(flavor=flavor))
    src_path = "./config/settings/base_user.py"
    dst_path = "./config/settings/{flavor}.py".format(flavor=flavor)
    shutil.copyfile(src_path, dst_path)

if __name__ == "__main__":

    flavor = os.environ.get('FLAVOR', 'dev')
    settings_module = "config.settings.{flavor}".format(flavor=flavor)

    settings_path = './' + settings_module.replace('.', '/') + '.py'

    if not os.path.exists(settings_path):
        create_default_settings_filed(flavor)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

