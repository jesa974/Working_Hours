#!/bin/bash

# This script is executed on boot

# Declare that the user start working
python3 ~/.clock/clock.py enter

# Launch the background process which checks the mouse
python3 ~/.clock/check_mouse.py &