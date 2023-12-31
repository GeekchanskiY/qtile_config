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
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
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

# import os
import subprocess

from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

from libqtile.utils import send_notification

from qtile_extras.popup.toolkit import (
    PopupRelativeLayout,
    PopupImage,
    PopupText
)

from qtile_extras import widget

from modules.docker_widget import DockerWidget

import logging


logging.basicConfig(filename='/home/dmitry/.config/qtile/qtile.log', level=logging.NOTSET)

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["sh", "/home/dmitry/.config/qtile/autostart.sh"])

@hook.subscribe.startup
def run_every_startup():
    send_notification("qtile", "refresh")

def notify_me():
    send_notification("qtile", f"{'asd'} has been managed by qtile")


def get_current_brightness(*args, **kwargs):
    command = "xrandr --verbose | grep -i brightness"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    output = str(process.stdout)
    brightness = float(output.strip().split(' ')[1])
    return brightness


def increase_brightness(*args, **kwargs):
    brightness: float = get_current_brightness()
    subprocess.run(f"xrandr --output eDP-1 --brightness {round(brightness + 0.1, 2)}", shell=True, stdout=subprocess.PIPE, text=True)
    send_notification('Increased brightness', str(round(brightness + 0.1, 2)))

def decrease_brightness(*args, **kwargs):
    brightness: float = get_current_brightness()
    subprocess.run(f"xrandr --output eDP-1 --brightness {round(brightness - 0.1, 2)}", shell=True, stdout=subprocess.PIPE, text=True)
    send_notification('Decreased brightness', str(round(brightness - 0.1, 2)))



def show_power_menu(qtile):
    controls = [
        PopupText(
            text="Lock",
            pos_x=0.1,
            pos_y=0.5,
            width=0.2,
            height=0.2,
            h_align="center"
        ),
        PopupText(
            text="Sleep",
            pos_x=0.4,
            pos_y=0.5,
            width=0.2,
            height=0.2,
            h_align="center"
        ),
        PopupText(
            text="Shutdown",
            pos_x=0.7,
            pos_y=0.5,
            width=0.2,
            height=0.2,
            h_align="center",
            mouse_callbacks={
                "Button1": lazy.shutdown()
            }
        ),
    ]

    layout = PopupRelativeLayout(
        qtile,
        width=500,
        height=100,
        controls=controls,
        background="00000060",
        initial_focus=True,
    )

    layout.show(centered=True)


mod = "mod4"
terminal = 'kitty'
keyboard = widget.KeyboardLayout(
    configured_keyboards=['us', 'ru'],
    padding=5
)

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

    # Other
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn('rofi -show drun'), desc="Spawn a command using a rofi"),

    Key([mod,], "space", lazy.widget["keyboardlayout"].next_keyboard(),   desc="Next keyboard layout"),

    Key([mod, "shift"], "q", lazy.function(show_power_menu)),
    Key([mod, 'control'], 'y', lazy.function(increase_brightness)),
    Key([mod, 'control'], 'u', lazy.function(decrease_brightness)),

]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
        layout.Columns( # type: ignore
        border_focus="#808080",
        border_width=2,
        fair=True,
        grow_amount=4,
        margin=5,
        margin_on_single=5,
    ),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper='/home/dmitry/Pictures/wallpaper_delorian.jpg',
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.GroupBox(
			    highlight_method='block',
			    rounded=True,
			    block_highlight_text_color='#FFFFFF',
			    this_current_screen_border='#2a2a2a',	
		        ),
                # widget.WindowName(),
                # widget.Chord(
                #     chords_colors={
                #         "launch": ("#ff0000", "#ffffff"),
                #     },
                #     name_transform=lambda name: name.upper(),
                # ),
                widget.Spacer(),
                widget.Clock(format="%H:%M"),
                widget.Spacer(),
                widget.Notify(),
                DockerWidget(),
                widget.Net(),
                keyboard,
                widget.Volume(
                    padding=5
                ),
                widget.Battery(
                    format=" {percent:2.0%} ",
                    padding=5
                ),
                widget.QuickExit(
                    countdown_start=3,
                    default_text=' ⏻ ',
                    countdown_format='[{}]',
                    padding=5
                ),
            ],
            30,
            background='#00000099',
            margin=[5, 5, 0, 5]
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
    Screen(
        wallpaper='/home/dmitry/Pictures/wallpaper_delorian.jpg',
        wallpaper_mode='fill',
        top=bar.Bar([
            widget.GroupBox(
			highlight_method='block',
			rounded=False,
			block_highlight_text_color='#FFFFFF',
			this_current_screen_border='#2a2a2a',	
		    ),
            widget.Spacer(),
            widget.Clock(format='%H:%M'),
            widget.Spacer()
            ], 
            30,
            background='#00000099',
            margin=[5, 5, 0, 5]
        ),
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
cursor_warp = False
floating_layout = layout.Floating( # type: ignore
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules, # type: ignore
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



