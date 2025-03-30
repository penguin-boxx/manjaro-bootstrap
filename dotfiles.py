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

def copy_all(src_dir, dst_dir):
    for path in dotfiles:
        src = os.path.join(src_dir, path)
        dst = os.path.join(dst_dir, path)
        print(f'Copying {src} to {dst}')
        if os.path.isfile(src):
            shutil.copy2(src, dst)
        else:
            shutil.copytree(src, dst, dirs_exist_ok=True)

def install():
    print('Installing dotfiles from backup...')
    subprocess.run(['git', 'pull', 'origin', 'main'], cwd=THIS)
    copy_all(THIS, HOME)
    print('Dotfiles installation finished')

def backup():
    print('Start backup of dotfiles...')
    copy_all(HOME, THIS)
    subprocess.run(['git', 'add', '.'], cwd=THIS)
    subprocess.run(['git', 'commit', '-m', f'"Backup {datetime.datetime.now()}"'], cwd=THIS)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=THIS)
    print('Backup of dotfiles finished')

def main():
    args = sys.argv
    if 'install' in args:
        install()
    elif 'backup' in args:
        backup()
    else:
        print('Unknown command')

main()
