sudo pacman-mirrors -f3
sudo pacman -Syyu # update system

sudo pacman -S \
    wget links lynx cmatrix sl cowsay elinks gparted gnome-system-monitor nautilus htop mc tree gnome-calculator gnome-search-tool gedit xf86-input-wacom　linux-headers xinput cheese gcolor3 screenfetch keepassxc \
    zsh zsh-autosuggestions zsh-completions zsh-doc zsh-history-substring-search zsh-lovers zsh-syntax-highlighting zshdb \
    firefox chromium discord telegram-desktop zoom qbittorrent \
    code code-marketplace dbeaver vim \
    git gitk cmake boost gtest doxygen stack ocaml opam rust rust-docs rustup mypy flake8 ipython python-pip autopep8 kotlin maven gradle junit \
    virtualbox docker valgrind postgresql \
    libreoffice xournalpp shotwell krita inkscape openshot vlc blender fbreader evince gimp coolreader obs-studio \
    texstudio texlive-most texlive-lang texlive-bibtexextra biber

# change bash to zsh
chsh -s $(which zsh)

# install oh my zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# install JetBrains mono font
wget -O ~/Downloads/jbfont.zip 'https://download.jetbrains.com/fonts/JetBrainsMono-2.304.zip'
unzip ~/Downloads/jbfont.zip -d ~/.local/share/
