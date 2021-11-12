# Working_Hours

![GitHub contributors](https://img.shields.io/github/contributors/jesa974/Working_Hours?color=green&style=flat-square)
![GitHub top language](https://img.shields.io/github/languages/top/jesa974/Working_Hours?color=orange&label=Python&style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/jesa974/Working_Hours?label=Project%20size&style=flat-square&color=lightgrey)
[![Visits Badge](https://badges.pufler.dev/visits/jesa974/Working_Hours)](https://badges.pufler.dev?style=for-the-badge)

Working_Hours is a program that helps you determine if you are in agreement with the number of hours you should work per week.

---
## Setup

Make the install script executable

```
sudo chmod +x clock_install.sh
```

Launch the install script
```
sudo ./clock_install.sh
```

You will have some parameters to define :

  * configuration folder   --> predifined to ~/.clock
  * number of hours        --> predifined to 35 hours
  * hourly rate            --> predifined to 7,35€ per hour


---
## Usage

Get all the commands
```
python3 clock.py help
```

Available arguments :

  * enter        ---> when you start working
  * break        ---> when you start a break
  * break_end    ---> when you finish a break
  * lunch        ---> when you go to lunch
  * lunch_end    ---> when you finish your lunch
  * go           ---> when you finish working

---
## Automation

Scripts ***start*** when the *PC starts up* and ***end*** when the *PC is shut down*

Must :

  * **Start** your computer when you **start working**
  * **Shut down** your computer when you **finish working**    

Activity is check using the mouse
 
  * If the user stop his mouse activity during **3min**, **break** is automatically declared
  * If the user restart his mouse activity after **3min or more** of inactivty, **end of break** is automatically declared

---
## Features in coming

* SQLite
* Background activity checking ***OR*** Linux extension
* Break time can be modified via the installation script
* Windows & Mac Version
