# manjaro-bootstrap

Personal Manjaro machine setup: system provisioning plus dotfiles backup/restore.

## New machine

```sh
git clone git@github.com:penguin-boxx/manjaro-bootstrap.git ~/manjaro-bootstrap
cd ~/manjaro-bootstrap
./init.sh
```

`init.sh` sets up swap, installs packages (repos + AUR), configures services
(docker, postgres), installs oh-my-zsh / opam / fonts / fcitx5, then backs up
the machine's current dotfiles to `~/.dotfiles_backup` and installs the ones
from this repo. The last two steps are interactive (`chsh` asks for a password,
`fcitx5-configtool` needs mozc added by hand). Reboot when it finishes.

## Day to day

```sh
./dotfiles.py backup         # copy dotfiles from $HOME into data/, commit and push
./dotfiles.py install        # pull and copy dotfiles from data/ into $HOME
./dotfiles.py local-backup   # snapshot current $HOME dotfiles to ~/.dotfiles_backup
./dotfiles.py install-local  # restore that snapshot
```

The list of managed files lives at the top of `dotfiles.py`. Backups abort if a
file in `data/` matches a known secret pattern (private keys, API tokens).

A systemd user timer (`systemd/dotfiles-backup.timer`, installed by `init.sh`)
runs `backup` weekly. Check it with:

```sh
systemctl --user list-timers dotfiles-backup.timer
journalctl --user -u dotfiles-backup.service
```
