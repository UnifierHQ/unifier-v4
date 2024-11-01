"""
Unifier - A sophisticated Discord bot uniting servers and platforms
Copyright (C) 2024  Green, ItsAsheer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import os
import sys
from pathlib import Path

install_option = sys.argv[1] if len(sys.argv) > 1 else None

if install_option == 'autodetect':
    try:
        with open('.install.json') as file:
            install_data = json.load(file)

        install_option = install_data['option']
    except:
        print(f'\x1b[31;1mNo Unifier installation was detected.\x1b[0m')

        # check if running in docker
        cgroup = Path('/proc/self/cgroup')
        if Path('/.dockerenv').is_file() or cgroup.is_file() and 'docker' in cgroup.read_text():
            # don't exit w/ error code 1 just in case
            sys.exit(0)
        else:
            sys.exit(1)

with open('boot/internal.json') as file:
    internal = json.load(file)

install_options = internal['options']

skip_plugins = '--skip-plugins' in sys.argv

prefix = None

if not install_option:
    for option in install_options:
        if option['default']:
            install_option = option['id']
            break
else:
    for option in install_options:
        if option['id'] == install_option:
            prefix = option['prefix']
            if prefix == '':
                prefix = None
            break

boot_config = {}
try:
    with open('boot_config.json') as file:
        boot_config = json.load(file)
except:
    pass

binary = boot_config['bootloader'].get('binary', 'py -3' if sys.platform == 'win32' else 'python3')

print('\x1b[36;1mInstalling dependencies, this may take a while...\x1b[0m')

user_arg = ' --user' if not boot_config['bootloader'].get('global_dep_install',False) else ''

if prefix:
    code = os.system(f'{binary} -m pip install{user_arg} -U -r requirements_{prefix}.txt')
else:
    code = os.system(f'{binary} -m pip install{user_arg} -U -r requirements.txt')

if not code == 0:
    print('\x1b[31;1mCould not install dependencies.\x1b[0m')
    print('\x1b[31;1mIf you\'re using a virtualenv, you might want to set global_dep_install to true in bootloader configuration to fix this.\x1b[0m')
    sys.exit(code)

if not skip_plugins:
    print('\x1b[36;1mInstalling Modifier dependencies, this may take a while...\x1b[0m')
    for plugin in os.listdir('plugins'):
        if not os.path.isdir(f'plugins/{plugin}'):
            continue

        with open(f'plugins/{plugin}/plugin.json') as file:
            plugin_data = json.load(file)

        if not plugin_data.get('requirements', None):
            continue

        code = os.system(f'{binary} -m pip install{user_arg} -U {" ".join(plugin_data["requirements"])}')
        if not code == 0:
            print(f'\x1b[36;1mCould not install dependencies for {plugin_data["id"]}, this Modifier may not work.\x1b[0m')

print('\x1b[36;1mDependencies successfully installed.\x1b[0m')
sys.exit(0)
