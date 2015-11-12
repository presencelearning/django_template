#!/usr/bin/env python
import os
import sys
import getpass
import shutil


def create_default_settings_filed(username):
    print('creating local settings file for user: {username} '.format(username=username))
    src_path = "./config/settings/base_user.py"
    dst_path = "./config/settings/{username}.py".format(username=username)
    shutil.copyfile(src_path, dst_path)

if __name__ == "__main__":

    username = getpass.getuser()
    settings_module = "config.settings.{username}".format(username=username)

    settings_path = './' + settings_module.replace('.', '/') + '.py'

    if not os.path.exists(settings_path):
        create_default_settings_filed(username)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

