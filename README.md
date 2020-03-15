# Heimdall

Heimdall is a simple USB threat evaluation framework that is designed to 
This project implements methods for USB mass storage devices analysis that are able to detect potential threats. The approach relies on an embedded system which executes a stack of tests, particularly designed to detect malicious behavioural characteristics in a USB mass storage device and thus to render it as dangerous.

* В /research се намира документацията.
* На https://slides.com/ivanzlatanov/heimdall/fullscreen#/ може да откриете презентацията.
* В /showcase се намират рекламните материали и графиките.

# Installation:
In order to clone and use this project, you must first install the following:

* [Python 3.x.x](https://www.python.org/download/releases/3.0/)
* [PyQT5](https://pypi.org/project/PyQt5/)
* [Libusb1](https://pypi.org/project/libusb1/)
* [Clamd](https://pypi.org/project/clamd/)
* [Tkinter](https://docs.python.org/3/library/tkinter.html)

To install them run the following commands:

`sudo apt update`

`sudo apt-get install python3 python3-pip python3-pyqt5 python3-tkinter clamav-daemon clamav-freshclam clamav-unofficial-sigs`