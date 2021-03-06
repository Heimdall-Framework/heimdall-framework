#!/bin/bash

function install_dependencies () 
{
    dependencies="python3 python3-pip qt5-default pyqt5-dev pyqt5-dev-tools python3-pyqt5 python-tk clamav-daemon clamav-freshclam clamav-unofficial-sigs gconf-editor"

    apt-get update
    apt-get install $dependencies
    pip3 install -r requirements.txt
    echo "Dependencies were installed successfuly."
}

function export_env_variables () 
{
    export DEVS_MOUNTPOINT=$1
    export LOGS_DIRECTORY_PATH=$2
    export TESTING_PORTS=$3
    export NUKING_PORTS=$4

    echo "export LOGS_DIRECTORY_PATH=$1" >> /home/$SUDO_USER/.bashrc
    echo "export LOGS_DIRECTORY_PATH=$1" >> /home/$USER/.bashrc

    echo "$LOGS_DIRECTORY_PATH"
    mkdir $1
    echo "export DEVS_MOUNTPOINT=$2" >> /home/$SUDO_USER/.bashrc
    echo "export DEVS_MOUNTPOINT=$2" >> /home/$USER/.bashrc
    mkdir $2
    echo "export TESTING_PORTS=$3" >> /home/$SUDO_USER/.bashrc
    echo "export TESTING_PORTS=$3" >> /home/$USER/.bashrc

    echo "export NUKING_PORTS=$4" >> /home/$SUDO_USER/.bashrc
    echo "export NUKING_PORTS=$4" >> /home/$USER/.bashrc

    echo "$NUKING_PORTS"

    source /home/$SUDO_USER/.bashrc
    source /home/$USER/.bashrc
    echo "Environmental variables were exported successfuly."
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
    git clone https://github.com/Heimdall-Framework/heimdall-hardware-controller.git
    mv heimdall-hardware-controller/hardware_controller.py source/python/plugins/hardware_controller.py
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
    export_env_variables $2 $3 $4 $5
    echo "Disabling automounting."
    disable_automounting

    pip3 install -e .

    if [ $1 = "rpi" ];
    then
        echo "Importing hardware controller."
        import_hardware_controller
        echo "Hardware controller was imported."
    fi

    if [ $6 = "y" ];
    then
        path_to_main="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )" 
        is_ubuntu=$(cat /etc/os-release | grep NAME)
        if [ $is_ubuntu = *"Ubuntu"* ];
        then
            echo "start on runlevel [2345] >> /etc/systemd/heimdall_startup.conf"
            echo "stop on runlevel [!2345] >> /etc/systemd/heimdall_startup.conf"
            echo "exec sudo -E heimdall GUI >>" /etc/systemd/heimdall_startup.conf 
        else 
            echo "start on runlevel [2345]" >> /etc/init/heimdall_startup.conf
            echo "stop on runlevel [!2345]" >> /etc/init/heimdall_startup.conf
            echo "exec sudo -E heimdall GUI GUI" >> /etc/init/heimdall_startup.conf
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
    echo "Please enter the numbers of the ports on which tested devices will be connected to (if more than one, sepate with comma {number1,number2}):"
    read testing_ports
    echo "Please enter the numbers of the ports on which nukable devices will be connected to (if more than one, sepate with comma {number3,number4}):"
    read nuking_ports

    echo "Would you like to start the application on startup (y/n): "
    read set_on_startup

    install $device_category $logs_location $mountpoin_location $testing_ports $nuking_ports $set_on_startup
}

main