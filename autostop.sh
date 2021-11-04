#!/bin/bash

# This script is executed at the extinction of the computer

# Stop the background process which checks the mouse
kill $(ps aux | grep '[p]ython3 check_mouse.py' | awk '{print $2}')

# Declare that the user stop working
python3 clock.py go