#!/bin/bash

gen_cfg_file() {
	# Ask for the configuration folder
	read -p " • Enter the configuration folder [~/.clock]: " workspace
	workspace=${workspace:-~/.clock}
	mkdir -p ${workspace}
	
	# Ask for the numbers of hours required per week
	read -p " • Enter the number of hours [35]: " hours
	hours=${hours:-35}

	# Ask for the hourly rate
	read -p " • Enter the hourly rate [7,35]: " rate
	rate=${rate:-7.35}

	# Save the data into a .conf file in the configuration folder
	echo "$hours : $rate" > ~/.clock/clock.conf
}

manage_auto_start_stop() {
	# Make the autostart & autostop scripts executable
	sudo chmod +x autostart.sh autostop.sh
	
	# Copy the scripts into the good directories for automation
	sudo mv autostop.sh /etc/rc6.d/K99autostop.sh
	sudo cp autostart.sh /etc/init.d

	sudo update-rc.d autostart.sh defaults 80
}

copy_scripts() {
	# Copy the scripts into the .clock directory
	sudo cp clock.py ~/.clock/
	sudo cp check_mouse.py ~/.clock/
}

gen_cfg_file
manage_auto_start_stop
