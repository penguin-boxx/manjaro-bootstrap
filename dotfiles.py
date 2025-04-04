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
    '.config/Code - OSS/User/settings.json',
    '.code_extensions.txt',
    os.path.join(XFCE, 'xfce4-keyboard-shortcuts.xml'),
    os.path.join(XFCE, 'xfce4-terminal.xml'),
    os.path.join(XFCE, 'keyboard-layout.xml'),
    os.path.join(XFCE, 'xfce4-panel.xml'),
    os.path.join(XFCE, 'xfce4-power-manager.xml'),
    os.path.join(XFCE, 'xfce4-screensaver.xml'),
    os.path.join(XFCE, 'xfwm4.xml'),
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
        try:
            if os.path.isfile(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
            else:
                shutil.copytree(src, dst, dirs_exist_ok=True)
        except FileNotFoundError as e:
            print(e)

def install():
    print('Installing dotfiles from backup...')
    if subprocess.run(['git', 'pull', 'origin', 'main', '--no-ff', '--no-edit'], cwd=THIS).returncode != 0:
        raise Exception("Git pull failed")
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
    with open(os.path.join(PREV, 'timestamp.txt'), 'w') as file:
        file.write(str(datetime.datetime.now()))
    print('End of previous dotfiles backup')

def installLocal():
    print('Installing dotfiles from local backup...')
    copy_all(PREV, HOME)
    print('Dotfiles installation finished')

# https://superuser.com/questions/1080682/how-do-i-back-up-my-vs-code-settings-and-list-of-installed-extensions
def extractVsCodeExtensions():
    with open(os.path.join(HOME, '.code_extensions.txt'), 'w') as file:
        subprocess.run(['code', '--list-extensions'], stdout=file)

def installVsCodeExtensions():
    with open(os.path.join(HOME, '.code_extensions.txt'), 'r') as file:
        subprocess.run(['xargs', '-n', '1', 'code', '--install-extension'], stdin=file)

def main():
    args = sys.argv
    if 'install' in args:
        install()
        installVsCodeExtensions()
    elif 'backup' in args:
        extractVsCodeExtensions()
        backup()
    elif 'local-backup' in args:
        extractVsCodeExtensions()
        backupLocally()
    elif 'install-local' in args:
        installLocal()
    else:
        print('Unknown command, use "install" or "backup" or "local-backup" or "install-local"')

main()
