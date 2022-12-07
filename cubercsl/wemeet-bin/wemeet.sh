#!/bin/sh
export XDG_SESSION_TYPE=x11
export QT_QPA_PLATFORM=xcb
export QT_AUTO_SCREEN_SCALE_FACTOR=1
export QT_STYLE_OVERRIDE=fusion # 解决使用自带qt情况下，字体颜色全白看不到的问题
export IBUS_USE_PORTAL=1        # fix ibus
unset WAYLAND_DISPLAY
USER_RUN_DIR="/run/user/$(id -u)"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}"
FONTCONFIG_DIR="$CONFIG_DIR/fontconfig"
KDE_ICON_CACHE_FILE="${XDG_CACHE_HOME:-$HOME/.cache}/icon-cache.kcache"
WEMEET_APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/wemeetapp"

# if pipewire-pulse installed
if [ -f /usr/bin/pipewire-pulse ]; then
    export PULSE_LATENCY_MSEC=20
fi

if [ -f /usr/bin/bwrap ]; then
    mkdir -p "$WEMEET_APP_DIR"
    bwrap --new-session --die-with-parent --cap-drop ALL --unshare-user-try \
     --unshare-pid --unshare-cgroup-try --ro-bind / / --dev-bind /dev /dev \
     --bind "$USER_RUN_DIR" "$USER_RUN_DIR" --tmpfs "$CONFIG_DIR" \
     --ro-bind-try "$FONTCONFIG_DIR" "$FONTCONFIG_DIR" \
     --bind-try "$KDE_ICON_CACHE_FILE" "$KDE_ICON_CACHE_FILE" \
     --bind "$WEMEET_APP_DIR" "$WEMEET_APP_DIR" \
     /opt/wemeet/bin/wemeetapp "$@"
else
    exec /opt/wemeet/bin/wemeetapp "$@"
fi
