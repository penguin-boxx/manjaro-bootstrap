set -e

sudo pacman-mirrors -f3
sudo pacman -Syyu # update system

sudo pacman -S \
    xf86-input-wacom linux-headers-meta xorg-xinput \
    htop mc tree wget links lynx cmatrix sl cowsay elinks gparted gnome-system-monitor baobab nautilus gnome-calculator gedit cheese gcolor3 screenfetch keepassxc \
    zsh zsh-autosuggestions zsh-completions zsh-doc zsh-history-substring-search zsh-lovers zsh-syntax-highlighting zshdb \
    firefox chromium discord telegram-desktop qbittorrent \
    code obsidian vim intellij-idea-community-edition dbeaver \
    git cmake boost gtest doxygen stack ocaml opam rust rustup mypy flake8 ipython python-pip autopep8 kotlin maven gradle junit sbt npm nvm \
    virtualbox docker valgrind postgresql \
    libreoffice xournalpp shotwell krita inkscape openshot vlc blender fbreader evince gimp coolreader obs-studio \
    texstudio texlive texlive-lang texlive-bibtexextra biber \
    steam

# change bash to zsh
chsh -s $(which zsh)

# install oh my zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# install JetBrains mono font
wget -O ~/Downloads/jbfont.zip 'https://download.jetbrains.com/fonts/JetBrainsMono-2.304.zip'
unzip ~/Downloads/jbfont.zip -d ~/.local/share/
