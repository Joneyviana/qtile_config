# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, puish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, hook, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger
from libqtile.widget.pulse_volume import PulseVolume
from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupSlider


from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration,   BorderDecoration
from qtile_extras.popup.templates.mpris2 import COMPACT_LAYOUT, DEFAULT_LAYOUT
from qtile_extras.widget.brightnesscontrol import BRIGHTNESS_NOTIFICATION

import os
import subprocess
import random
import re

mod = "mod1"
terminal = guess_terminal()

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

def get_brightness():
    return subprocess.run("xrandr --verbose --current | grep ^'HDMI-A-0' -A5 | tail -n1", shell=True, capture_output=True).stdout
    
def adjust_brightness(value):
    brightness_text = get_brightness()
    brightness = float(re.findall("\d+\.\d+", str(brightness_text))[0]) + value
    os.system("xrandr --output 'HDMI-A-0' --brightness {0}".format(brightness))
    return brightness
    
def label_brightness(value):
    percentage = int(value * 100)
    return f"Brightness {percentage}%"
    
def show_brightness_menu(qtile, output):
    if BRIGHTNESS_NOTIFICATION.configured and not BRIGHTNESS_NOTIFICATION.finalized:
       BRIGHTNESS_NOTIFICATION.popup.clear()
       BRIGHTNESS_NOTIFICATION.update_controls(brightness=output,text=label_brightness(output))
    else :
       BRIGHTNESS_NOTIFICATION.finalized = False
       BRIGHTNESS_NOTIFICATION._configure(qtile)
       BRIGHTNESS_NOTIFICATION.show(hide_on_timeout=0.5, centered=True)
       BRIGHTNESS_NOTIFICATION.update_controls(brightness=output,text=label_brightness(output))
    
    
def increase1_brightness(qtile):
    show_brightness_menu(qtile,adjust_brightness(0.01))
      
def increase10_brightness(qtile): 
    
    show_brightness_menu(qtile, adjust_brightness(0.10))

def decrease1_brightness(qtile):
     show_brightness_menu(qtile, adjust_brightness(-0.01))
      
def decrease10_brightness(qtile):
    show_brightness_menu(qtile, adjust_brightness(-0.10))


def execute_client(command):
    os.system("python ~/.config/qtile/server_client/client.py "+ command)

def next_music(qtile):
    execute_client("pause")
    execute_client("move down")
    execute_client("play")

def previous_music(qtile):
    execute_client("pause")
    execute_client("move up")
    execute_client("play")

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "Up", lazy.function(increase10_brightness)),
    Key([mod, "shift"], "Up", lazy.function(increase1_brightness)),
    Key([mod], "Down", lazy.function(decrease10_brightness)),
    Key([mod, "shift"], "Down", lazy.function(decrease1_brightness)),
    Key([mod, "control"], "Down", lazy.function(next_music)),
    Key([mod, "control"], "Up", lazy.function(previous_music)),
]

groups = []


groups.append(Group("Spotify"))
groups.append(Group("Web", spawn='google-chrome-stable'))
groups.append(Group("Terminal", spawn="alacritty"))
groups.append(Group("Others"))


keys.append(Key([mod],"1",lazy.group["Spotify"].toscreen()))
keys.append(Key([mod],"2",lazy.group["Web"].toscreen()))
keys.append(Key([mod],"3",lazy.group["Terminal"].toscreen()))
keys.append(Key([mod],"4",lazy.group["Others"].toscreen()))


appearence = [("~/.config/qtile/archblue.png","0c16d7","ffffff")
,("~/.config/qtile/archGreen.jpg", "588365", "000000"),
("~/.config/qtile/archPurple.jpg", "62026F", "eb97ee"),
("~/.config/qtile/archRed.jpg", "670000", "eb97ee")]


random_appearance = random.choice(appearence)
wallpaper = random_appearance[0]
cor = random_appearance[1]

layouts = [
           layout.Columns(border_normal=cor, ratio=5,margin=[2,2,4,2], border_focus=random_appearance[2], border_width=3),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

forward = {
"decorations": [
        PowerLineDecoration(path="forward_slash"),
    ]
}

back = {
"decorations": [
        PowerLineDecoration(path="back_slash"),
    ]
}

arrow_left = {
"decorations":[
    PowerLineDecoration(path="rounded_left")
    ]
}

arrow_right = {
"decorations":[
    PowerLineDecoration(path="rounded_right")
    ]
}

widget_defaults = dict(
    font= "Consolas",
    fontsize=14,
    foreground = random_appearance[2]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.ThermalSensor(format="CPU: {temp:.0f}{unit}", background=cor, **arrow_left),
                widget.Spacer(**arrow_right),
                widget.GroupBox(**arrow_left, background="#00000075"),
                widget.Prompt(**arrow_left, background=cor),
                widget.Mpris2(scroll=True,max_chars=45,**arrow_left, background=cor),
                widget.Spacer(**arrow_right),
                widget.Clock(format="%d %a %I:%M %p", background="#00000075",**arrow_left),
                widget.PulseVolume(background=cor),
            ],
            18,
            background = "#00000000",
            margin=[2,4,0,4],
           # border_width=[2, 8, 0, 8],  # Draw top and bottom borders
            border_color=["#00000000", "#00000000", "ff00ff", "#00000000"]  # Borders are magenta
        ),
        wallpaper_mode = "strech",
        wallpaper = wallpaper,
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
