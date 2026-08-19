#!/usr/bin/env python

import os
import re
import sys
import shutil
import platform
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
    '.config/Code/User/settings.json',
    '.code_extensions.txt',
    os.path.join(XFCE, 'xfce4-keyboard-shortcuts.xml'),
    os.path.join(XFCE, 'xfce4-terminal.xml'),
    os.path.join(XFCE, 'keyboard-layout.xml'),
    os.path.join(XFCE, 'xfce4-panel.xml'),
    os.path.join(XFCE, 'xfce4-power-manager.xml'),
    os.path.join(XFCE, 'xfce4-screensaver.xml'),
    os.path.join(XFCE, 'xfwm4.xml'),
    '.config/environment.d/fcitx5.conf',
    '.xprofile',
    '.config/fcitx5/config',
    '.config/fcitx5/profile',
    '.config/fcitx5/conf/xcb.conf',
]

# High-confidence secret patterns only, to avoid false positives on
# config option names like "AllowInputMethodForPassword".
SECRET_PATTERNS = [
    r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    r'ghp_[A-Za-z0-9]{36}',
    r'github_pat_[A-Za-z0-9_]{22,}',
    r'glpat-[A-Za-z0-9_-]{20,}',
    r'xox[baprs]-[A-Za-z0-9-]{10,}',
    r'AKIA[0-9A-Z]{16}',
    r'sk-[A-Za-z0-9_-]{20,}',
    r'AIza[0-9A-Za-z_-]{35}',
]

HOME = os.environ['HOME']
PREV = os.path.join(HOME, '.dotfiles_backup')
THIS = os.path.dirname(os.path.realpath(__file__))
DATA = os.path.join(THIS, 'data')

def git(*args):
    subprocess.run(['git', *args], cwd=THIS, check=True)

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

def scanForSecrets():
    hits = []
    for root, _, files in os.walk(DATA):
        for name in files:
            path = os.path.join(root, name)
            with open(path, errors='ignore') as file:
                for lineno, line in enumerate(file, 1):
                    for pattern in SECRET_PATTERNS:
                        if re.search(pattern, line):
                            hits.append(f'{path}:{lineno}')
    if hits:
        raise Exception('Possible secrets found, backup aborted:\n' + '\n'.join(hits))

def install():
    print('Installing dotfiles from backup...')
    git('pull', '--ff-only', 'origin', 'main')
    copy_all(DATA, HOME)
    print('Dotfiles installation finished')

def backup():
    print('Start backup of dotfiles...')
    os.makedirs(DATA, exist_ok=True)
    copy_all(HOME, DATA)
    scanForSecrets()
    git('add', '.')
    git('status')
    changes = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=THIS, check=True, capture_output=True, text=True,
    ).stdout.strip()
    if changes:
        git('commit', '-m', f'Backup {platform.node()} {datetime.datetime.now()}')
    else:
        print('No changes since last backup')
    git('push', 'origin', 'main')
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
        subprocess.run(['code', '--list-extensions'], stdout=file, check=True)

def installVsCodeExtensions():
    with open(os.path.join(HOME, '.code_extensions.txt')) as file:
        for extension in file.read().split():
            subprocess.run(['code', '--install-extension', extension], check=True)

COMMANDS = {
    'install': lambda: (install(), installVsCodeExtensions()),
    'backup': lambda: (extractVsCodeExtensions(), backup()),
    'local-backup': lambda: (extractVsCodeExtensions(), backupLocally()),
    'install-local': installLocal,
}

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        print(f'Usage: {sys.argv[0]} {{{" | ".join(COMMANDS)}}}')
        sys.exit(1)
    COMMANDS[sys.argv[1]]()

if __name__ == '__main__':
    main()
