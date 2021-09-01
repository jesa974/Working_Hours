#!/bin/bash

gen_cfg_file() {
    
	read -p " • Enter the configuration folder [~/.clock]: " workspace
	workspace=${workspace:-~/.clock}
	mkdir -p ${workspace}

	read -p " • Enter the number of hours [35]: " hours
	hours=${hours:-35}

	read -p " • Enter the taux horaire [7,35]: " rate
	rate=${rate:-7.35}

	# Save the data into a .conf file in the configuration folder
	echo "$hours : $rate" > ~/.clock/clock.conf

}

gen_cfg_file