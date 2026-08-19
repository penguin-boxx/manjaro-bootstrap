#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Setup swap
# https://wiki.archlinux.org/title/Swap
if [ ! -f /swapfile ]; then
    sudo mkswap -U clear --size 20G --file /swapfile
    sudo swapon /swapfile
fi
grep -q '^/swapfile' /etc/fstab \
    || sudo sh -c 'echo "/swapfile none swap defaults 0 0" >> /etc/fstab'

sudo pacman-mirrors -f3
sudo pacman -Syyu # update system

# Enable AUR
# https://forum.manjaro.org/t/enable-aur-using-command-line/79107
sudo sed -Ei '/EnableAUR/s/^#//' /etc/pamac.conf

sudo pacman -S --needed \
    xf86-input-wacom linux-headers-meta xorg-xinput \
    htop mc tree wget links lynx cmatrix sl cowsay elinks gparted gnome-system-monitor baobab nautilus gnome-calculator gedit cheese gcolor3 screenfetch keepassxc \
    zsh zsh-autosuggestions zsh-completions zsh-doc zsh-history-substring-search zsh-lovers zsh-syntax-highlighting zshdb \
    firefox chromium discord telegram-desktop qbittorrent \
    code obsidian vim dbeaver \
    git git-lfs cloc nix cmake boost gtest doxygen stack hlint ocaml opam rust rustup mypy flake8 ipython python-pip autopep8 kotlin maven gradle junit sbt npm nvm \
    virtualbox docker valgrind postgresql \
    libreoffice xournalpp shotwell krita inkscape openshot vlc blender fbreader evince gimp coolreader obs-studio \
    texstudio texlive texlive-lang texlive-bibtexextra biber \
    steam

pamac install zen-browser zoom code-marketplace code-features nekoray-bin koka-bin swift-bin etcher-bin python-pympress ghcup-hs-bin normcap

# post-install setup for services
sudo systemctl enable docker.service
sudo usermod -aG docker "$USER"
sudo test -f /var/lib/postgres/data/PG_VERSION \
    || sudo -u postgres initdb -D /var/lib/postgres/data
sudo modprobe vboxdrv || echo 'WARNING: vboxdrv module not loaded, reboot may be needed'

# make zen default browser
xdg-settings set default-web-browser zen-browser.desktop
xdg-mime default zen-browser.desktop x-scheme-handler/http
xdg-mime default zen-browser.desktop x-scheme-handler/https
xdg-mime default zen-browser.desktop text/html

# install oh my zsh (RUNZSH/CHSH keep the installer from prompting
# and exec'ing zsh, which would halt this script)
[ -d ~/.oh-my-zsh ] \
    || RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# install coq proof assistent
opam init -y
opam repo add coq-released https://coq.inria.fr/opam/released
opam remote add coq-weakmemory-local -k git https://github.com/weakmemory/local-coq-opam-archive
opam install -y coq coq-hahn vscoq-language-server

# install JetBrains mono font
if ! fc-list | grep -qi 'JetBrains Mono'; then
    wget -O ~/Downloads/jbfont.zip 'https://download.jetbrains.com/fonts/JetBrainsMono-2.304.zip'
    unzip ~/Downloads/jbfont.zip -d ~/.local/share/
    rm ~/Downloads/jbfont.zip
    fc-cache -f
fi

# install japaneese input
sudo pacman -S --needed fcitx5 fcitx5-mozc fcitx5-configtool fcitx5-gtk fcitx5-qt fcitx5-im
mkdir -p ~/.config/autostart
cp /etc/xdg/autostart/org.fcitx.Fcitx5.desktop ~/.config/autostart/
setxkbmap -layout us -option # make hotkeys work

python "$SCRIPT_DIR/dotfiles.py" local-backup
python "$SCRIPT_DIR/dotfiles.py" install

# enable weekly automatic dotfiles backup
mkdir -p ~/.config/systemd/user
cp "$SCRIPT_DIR"/systemd/dotfiles-backup.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now dotfiles-backup.timer

# interactive steps last, so a prompt cannot stall the unattended part
chsh -s "$(which zsh)"       # asks for password
fcitx5-configtool            # add mozc input manually

echo 'Now reboot!'
