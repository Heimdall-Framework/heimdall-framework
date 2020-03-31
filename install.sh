#!/bin/bash

function install_dependencies () 
{
    dependencies="python3 python3-pip python3-pyqt5 python-tk clamav-daemon clamav-freshclam clamav-unofficial-sigs"
    python_modules="pymsgbox libusb1 clamd"

    apt-get update
    apt-get install $dependencies
    pip3 install $python_modules
    echo "Dependencies were installed successfuly."
}

function export_env_variables () 
{
    export DEVS_MOUNTPOINT=$1
    export LOGS_DIRECTORY_PATH=$2
    echo "export DEVS_MOUNTPOINT=$1 >> ~/.bashrc "
    mkdir $1
    echo "export LOGS_DIRECTORY_PATH=$2 >> ~/.bashrc "
    mkdir $2
    echo "Environmental variables were imported successfuly."
}

function disable_automounting (){
    gconftool-2 --direct \
    --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory \
    --type bool \
    --set /desktop/gnome/volume_manager/automount_drives false

    echo "Automounting was disabled."
}

function import_hardware_controller()
{
    git clone git@github.com:Heimdall-Framework/heimdall-hardware-controller.git
    mv heimdall-hardware-controller/heimdall_hardware_controller.py source/python/plugins/hardware_controller.py
    rm -rf heimdall-hardware-controller
    echo "Hardware controller was imported successfuly"
}

function increase_rpi_swap() 
{

    echo "Swap size was increased."
}

function install () 
{
    echo "Installing dependencies."
    install_dependencies
    echo "Setting environmental variables."
    export_env_variables $2 $3 
    echo "Disabling automounting."
    disable_automounting

    if [ $1 == "rpi" ]
    then
        echo "Importing hardware controller."
        import_hardware_controller
        echo "Increasing swap."
        
    fi

    if [ $4 == "y" ]
    then
        path_to_main = "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" 
        is_ubuntu = $(cat /etc/os-release | grep NAME)
        if [[$is_ubuntu == *"Ubuntu"*]]
        then
            echo "start on runlevel [2345] >> /etc/systemd/heimdall_startup.conf"
            echo "stop on runlevel [!2345] >> /etc/systemd/heimdall_startup.conf"
            echo "exec $path_to_main/source/python/main.py GUI >> /etc/systemd/heimdall_startup.conf" 
        else 
            echo "start on runlevel [2345] >> /etc/init/heimdall_startup.conf"
            echo "stop on runlevel [!2345] >> /etc/init/heimdall_startup.conf"
            echo "exec $path_to_main/source/python/main.py GUI >> /etc/init/heimdall_startup.conf" 
       fi
    fi

    echo "Installation was successful."
}

function main ()
{
    echo "Welcome to the installation script."
    echo "Enter the device category (desktop/rpi): "
    read device_category
    echo "Please enter the location of the logs folder: "
    read logs_location
    echo "Please enter the location of the mounting folder, where device will be temporarely mounted during the testing process: "
    read mountpoin_location
    echo "Would you like to start the application on startup (y/n): "
    read set_on_startup

    install $device_category $logs_location $mountpoin_location $set_on_startup
}

main