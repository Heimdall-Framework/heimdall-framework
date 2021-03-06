# Heimdall
Heimdall is a Python USB threat evaluation framework for Linux that is designed to detect malicious behavior in USB mass storage devices.

## Installation:
You can install manually or automatically, using the script.

### Automatic installation
In order to install the project automatically, you must start the script, named `install.sh`, located inside the root folder of the project, and provide the proper arguments (desktop or RPI installation, logs folder path, and mounting folder path)
when asked. The script will update the system, install the required dependencies, set the appropriate environment variables, and, if the installation is on RPI, download the hardware controller. 

### Manual installation
In order to clone and use this project, you must first install the following:

* [Python 3.6+](https://www.python.org/download/releases/3.0/);
* [PyQT5](https://pypi.org/project/PyQt5/);
* [Libusb1](https://pypi.org/project/libusb1/);
* [Clamd](https://pypi.org/project/clamd/);
* [Tkinter](https://docs.python.org/3/library/tkinter.html);
* [PlugyPy](https://pypi.org/project/PlugyPy/).


To install them run the following commands:

```
sudo apt-get update
```

```
sudo apt-get install python3 python3-pip python3-pyqt5 python-tk clamav-daemon clamav-freshclam clamav-unofficial-sigs
```

```
sudo pip3 install pymsgbox libusb1 clamd objectpath
```

Then you must set the following environment variables to directories of your choice:

* DEVS_MOUNTPOINT - the location of the directory where the tested devices will be mounted temporarily;
* LOGS_DIRECTORY_PATH - the location of the directory where Heimdall will store its logs;
* TESTING_PORTS - the port or ports that will be used to test USB mass storage devices;
* NUKING_PORTS - the port or ports that will be used to nuke a mass storage device.

You can set and export them with:

```
export DEVS_MOUNTPOINT=<LOCATION>
```

```
export LOGS_DIRECTORY_PATH=<LOCATION>
```

```
export TESTING_PORTS=<PORT>
```

```
export NUKING_PORTS=<PORT>
```

where `<LOCATION>` is the path to the directory on your system and `<PORT>` is the port or ports that will be used for either testing or nuking.

Now you can clone the repository with `git@github.com:Heimdall-Framework/heimdall-frame work.git` and proceed to start Heimdall in GUI or NOGUI mode.

## Execution
In order to run the program, you must enter in the heimdall-framework/source/python directory and run `./main.py NOGUI` (for NOGUI mode) or `./main.py GUI` (for GUI mode).


## Possible issues:

### No access or permission exceptions
It might happen because the user you use does not have the proper access rights to use devices on the USB or to create and read files from the directories in your environment variables.
The proper way to fix it is to start the `./main.py` file with `sudo -E` which will grant it the proper access rights and keep the environment variables.

### Clamav or clamd can't find or create specific files
There are multiple possible causes for this issue. One of them is that another clamav instance is already running on your system and uses those files. You can check this
by running `htop` or `top` and looking for a process that has 'clam' in his name. Terminate it and try again, if the problem still exist check these threads for possible solutions:
* [ClamAV not creating clamd.ctl file](https://askubuntu.com/questions/1170774/clamav-clamd-ctl-file-is-not-getting-created-on-ubuntu);
* [Connect to /var/run/clamav/clamd.ctl failed](https://www.howtoforge.com/community/threads/connect-to-var-run-clamav-clamd-ctl-failed.73251/);
* [Can't connect to UNIX socket /var/run/clamav/clamd.ctl](https://www.howtoforge.com/debian-ubuntu-clamav-clamd-cant-connect-to-unix-socket-var-run-clamav-clamd.ctl);
* [Clamd Will Not Start](https://www.howtoforge.com/community/threads/clamd-will-not-start.34559/).

## Creating plugins (external tests):
A plugin (or external test) is a Python file that is kept in a specific directory and contains a test or multiple tests that are executed after
the hardcoded ones. You can create your own test by creating a Python file with the following structure:

```python
import usb1 as usb
"""
All custom tests must to have the device and device handle as parameters.
"""
def demo_test(device, device_handle):
    print('> Demo Test was passed.')

    return True
```

Where your test function, the `demo_test` in this case, has to take a usb1 device object (named as `device`) 
and usb1 device handle object (named as `device_handle`) as parameters.

After developing your test you have to add it to the plugins directory - `/source/python/plugins`. Then you must edit the plugin configuration file - `/source/python/plugins/config.json`, and add the config for your test inside the JSON list. Put the name of the test in the `name` field and the 
function that will be called when executed in the `main_function` field.
Example:
```json
[
        {
                "name" : "demo_test",
                "main_function" : "execute_demo_test",
                "enabled" : true
        },
        {
                "name" : "YOUR_TEST",
                "main_function" : "YOUR_TEST_MAIN_FUNCTION",
                "enabled" : true
        }
]
```
Enabling or disabling tests can be done by setting the `enabled` parameter to `true` or `false`. Disabled tests won't be executed.

You find out more about the plugin management system that is used in this project [HERE](https://github.com/not-so-cool-anymore/plugypy).