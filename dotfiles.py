import os
import sys
import shutil
import subprocess
import datetime

dotfiles = [
    '.bashrc',
    '.bash_history',
    '.face',
    '.gitconfig',
    '.zshrc',
    '.config/xfce4/xfconf/xfce-perchannel-xml/',
]

HOME = os.environ['HOME']
THIS = os.path.dirname(os.path.realpath(__file__))

def install():
    pass

def backup():
    print('Start backup of dotfiles...')
    # todo add remove
    for path in dotfiles:
        src = os.path.join(HOME, path)
        print(f'\tCopying {src}')
        if os.path.isfile(src):
            shutil.copy2(src, THIS)
        else:
            target = os.path.join(THIS, path)
            shutil.copytree(src, target, dirs_exist_ok=True)
    subprocess.run(['git', 'add', '.'], cwd=THIS)
    subprocess.run(['git', 'commit', '-m', f'"Backup {datetime.datetime.now()}"'], cwd=THIS)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=THIS)
    print('Finish backup of dotfiles')

def main():
    args = sys.argv
    if 'install' in args:
        print('kek')
    elif 'backup' in args:
        backup()
    else:
        print('Unknown command')

main()
