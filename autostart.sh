#!/bin/bash
picom --config ~/.config/qtile/picom.conf &
alacritty --command python ~/.config/qtile/server_client/server.py &
