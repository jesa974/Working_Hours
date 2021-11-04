from pynput.mouse import Button, Controller
import time
import os

i = 0
cpt = 0

while True:
    # Wait for 20 seconds
    time.sleep(2)
    # Create a mouse controller
    mouse = Controller()
    # Get the current position of the mouse
    current_mouse_position = mouse.position
    # Print the current position of the mouse
    print(current_mouse_position)
    # If it is not the first time, compare the current position with the previous one
    if i != 0:
        # If the current position is different from the previous one, reset the counter
        if current_mouse_position != old_mouse_position:
            if cpt >= 9:
                # Send a notification to the user if the mouse moved
                os.system("notify-send 'Break Time stops'")
                os.system("python3 clock.py lunch_end")
            cpt = 0
        # If the current position is the same as the previous one, increment the counter
        else:
            
            cpt = cpt + 1
            # If the counter reaches 9 (3 min), consider that the user is absent
            if cpt == 9:
                # Send a notification to the user if the mouse is not moved
                os.system("notify-send 'Break Time starts'")
                os.system("python3 clock.py lunch")

    # Get the last mouse position        
    old_mouse_position = current_mouse_position
    i = i + 1