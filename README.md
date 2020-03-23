# Heimdall

Heimdall is a simple USB threat evaluation framework that is designed to detect malicious behavior in USB mass storage devices.

---

## Installation:
In order to clone and use this project, you must first install the following:

* [Python 3.x.x](https://www.python.org/download/releases/3.0/);
* [PyQT5](https://pypi.org/project/PyQt5/);
* [Libusb1](https://pypi.org/project/libusb1/);
* [Clamd](https://pypi.org/project/clamd/);
* [Tkinter](https://docs.python.org/3/library/tkinter.html).

To install them run the following commands:

```
sudo apt update
```

```
sudo apt-get install python3 python3-pip python3-pyqt5 python-tk clamav-daemon clamav-freshclam clamav-unofficial-sigs
```

```
sudo pip3 install pymsgbox libusb1 clamd
```

Then you must set the following environmental variables to directories of your choice:

* DEVS_MOUNTPOINT - the location of the directory where the tested devices will be mounted temporary;
* LOGS_DIRECTORY_PATH - the location of the directory where Heimdall will store its logs.

You can set and export them with:

```
export DEVS_MOUNTPOINT=<LOCATION>
```

```
export LOGS_DIRECTORY_PATH=<LOCATION>
```

where location is the path to the directory.

Now you can clone the repository with `git@github.com:Heimdall-Framework/heimdall-framework.git` and proceed to starting Heimdall in GUI or NOGUI mode.
In order to do it you must enter in heimdall-framework/source/python and run `./main.py NOGUI` (for NOGUI mode) or `./main.py GUI` (for GUI mode).

## Possible issues:

### No access or permission exceptions
It might happen because the user you use does not have the proper access rights to use devices on the USB or to create and read files from the directories in your environmental variables.
One possible fix can be to give root privileges to your user (actually giving root privileges and not using `sudo` because it will cause conflict
during one of the tests). To do it, follow this thread in StackOverflow - [CLICK HERE](https://askubuntu.com/questions/168280/how-do-i-grant-sudo-privileges-to-an-existing-user).

### Clamav or clamd can't find or create specific files
There are multiple possible causes for this issue. One of them is that another clamav instance is already running on your system and uses those files. You can check this
by running `htop` or `top` and looking for a process that has 'clam' in his name. Terminate it and try again, if the problem still exist check these threads for possible solutions:
* [ClamAV not creating clamd.ctl file](https://askubuntu.com/questions/1170774/clamav-clamd-ctl-file-is-not-getting-created-on-ubuntu);
* [Connect to /var/run/clamav/clamd.ctl failed](https://www.howtoforge.com/community/threads/connect-to-var-run-clamav-clamd-ctl-failed.73251/);
* [Can't connect to UNIX socket /var/run/clamav/clamd.ctl](https://www.howtoforge.com/debian-ubuntu-clamav-clamd-cant-connect-to-unix-socket-var-run-clamav-clamd.ctl);
* [Clamd Will Not Start](https://www.howtoforge.com/community/threads/clamd-will-not-start.34559/).

## Creating plugins (external tests):
A plugin (or external test) is a python file that is kept in a specific directory and contains a test or multiple tests that are executed after
the hardcoded ones. You can create your own test by creating a python file with the following structure:

```python
import usb1 as usb
"""
All custom tests have to have the device and device handle as parameters.
"""
def demo_test(device, device_handle):
    print('> Demo Test was passed.')

    return True
```

Where your test function, the `demo_test` in this case, has to take a usb1 device object and usb1 device handle object as parameters.
After developing your test you have to add it to the plugins directory - /source/python/plugins, and give it a name. Then you just edit the plugin configuration 
file - /source/python/config.json, and add the config for your test inside the JSON list.
Example:
```json
[
        {"name" : "demo_test", "enabled" : true},
        {"name" : "YOUR TEST", "enabled" : true}
]
```
You can enable or disable test by setting the `enabled` parameter next to their name to `true` or `false`. Disabled tests won't be executed.