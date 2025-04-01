import os
import sys
import shutil
import subprocess
import datetime

XFCE = '.config/xfce4/xfconf/xfce-perchannel-xml/'

dotfiles = [
    '.bashrc',
    '.face',
    '.fix_tap.py',
    '.gitconfig',
    '.zshrc',
    os.path.join(XFCE, 'xfce4-keyboard-shortcuts.xml'),
    os.path.join(XFCE, 'xfce4-terminal.xml'),
    os.path.join(XFCE, 'keyboard-layout.xml'),     # experimental
    os.path.join(XFCE, 'xfce4-panel.xml'),         # experimental
    os.path.join(XFCE, 'xfce4-power-manager.xml'), # experimental
    os.path.join(XFCE, 'xfce4-screensaver.xml'),   # experimental
    os.path.join(XFCE, 'xfwm4.xml'),               # experimental
    os.path.join(XFCE, 'xfce4-session.xml'),       # experimental
]

HOME = os.environ['HOME']
PREV = os.path.join(HOME, '.dotfiles_backup')
THIS = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(THIS, 'data')

def copy_all(src_dir, dst_dir):
    for path in dotfiles:
        src = os.path.join(src_dir, path)
        dst = os.path.join(dst_dir, path)
        print(f'Copying {src} to {dst}')
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        else:
            shutil.copytree(src, dst, dirs_exist_ok=True)

def install():
    print('Installing dotfiles from backup...')
    subprocess.run(['git', 'pull', 'origin', 'main'], cwd=THIS)
    copy_all(DATA, HOME)
    print('Dotfiles installation finished')

def backup():
    print('Start backup of dotfiles...')
    os.makedirs(DATA, exist_ok=True)
    copy_all(HOME, DATA)
    subprocess.run(['git', 'status'], cwd=THIS)
    subprocess.run(['git', 'add', '.'], cwd=THIS)
    subprocess.run(['git', 'commit', '-m', f'"Backup {datetime.datetime.now()}"'], cwd=THIS)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=THIS)
    print('Backup of dotfiles finished')

def backupLocally():
    print('Start backup previous dotfiles...')
    copy_all(HOME, PREV)
    print('End of previous dotfiles backup')

def installLocal():
    print('Installing dotfiles from local backup...')
    copy_all(PREV, HOME)
    print('Dotfiles installation finished')

def main():
    args = sys.argv
    if 'install' in args:
        install()
    elif 'backup' in args:
        backup()
    elif 'local-backup' in args:
        backupLocally()
    elif 'install-local' in args:
        installLocal()
    else:
        print('Unknown command')

main()
