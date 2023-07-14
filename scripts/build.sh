#!/bin/sh

CWD=$(pwd)
echo $CWD
echo $HOME

flatpak build-init $CWD/.flatpak/repo com.misterlobo.pyzza org.gnome.Sdk org.gnome.Platform 44

flatpak-builder --ccache --force-clean --disable-updates --download-only --state-dir=$CWD/.flatpak/flatpak-builder --stop-at=pyzza $CWD/.flatpak/repo $CWD/com.misterlobo.pyzza.json

flatpak-builder --ccache --force-clean --disable-updates --disable-download --build-only --keep-build-dirs --state-dir=$CWD/.flatpak/flatpak-builder --stop-at=pyzza $CWD/.flatpak/repo $CWD/com.misterlobo.pyzza.json

flatpak build --share=network --nofilesystem=host --filesystem=$CWD --filesystem=$CWD/.flatpak/repo --env=RUST_BACKTRACE=1 --env=RUST_LOG=pyzza=debug --env=LD_LIBRARY_PATH=/app/lib --env=PKG_CONFIG_PATH=/app/lib/pkgconfig:/app/share/pkgconfig:/usr/lib/pkgconfig:/usr/share/pkgconfig --filesystem=$CWD/_build $CWD/.flatpak/repo meson --prefix /app _build

flatpak build --share=network --nofilesystem=host --filesystem=$CWD --filesystem=$CWD/.flatpak/repo --env=RUST_BACKTRACE=1 --env=RUST_LOG=pyzza=debug --env=PATH=$PATH:/usr/bin:/usr/lib/sdk/rust-stable/bin --env=LD_LIBRARY_PATH=/app/lib --env=PKG_CONFIG_PATH=/app/lib/pkgconfig:/app/share/pkgconfig:/usr/lib/pkgconfig:/usr/share/pkgconfig --filesystem=$CWD/_build $CWD/.flatpak/repo meson install -C _build

flatpak build --with-appdir --allow=devel --bind-mount=/run/user/1000/doc=/run/user/1000/doc/by-app/com.misterlobo.pyzza --share=network --share=ipc --socket=fallback-x11 --device=dri --socket=wayland --talk-name=org.freedesktop.portal.* --talk-name=org.a11y.Bus --bind-mount=/run/flatpak/at-spi-bus=/run/user/1000/at-spi/bus_0 --env=AT_SPI_BUS_ADDRESS=unix:path=/run/flatpak/at-spi-busguid=e606147a86daee8549d7ecd96499f6df --env=DESKTOP_SESSION=plasma --env=LANG=en_PH.UTF-8 --env=XDG_CURRENT_DESKTOP=KDE --env=XDG_SEAT=seat0 --env=XDG_SESSION_DESKTOP=KDE --env=XDG_SESSION_ID=1 --env=XDG_SESSION_TYPE=x11 --env=XDG_VTNR=1 --bind-mount=/run/host/fonts=/usr/share/fonts --bind-mount=/run/host/fonts-cache=/var/cache/fontconfig --filesystem=$HOME/.fonts:ro --filesystem=$HOME/.cache/fontconfig:ro --bind-mount=/run/host/user-fonts-cache=$HOME/.cache/fontconfig --bind-mount=/run/host/font-dirs.xml=$HOME/.cache/font-dirs.xml $CWD/.flatpak/repo pyzza