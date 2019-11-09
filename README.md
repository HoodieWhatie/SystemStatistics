# SystemStatistics

<b>Disclaimer:</b>
1) This script was developed on a RPi 4 running Rasbpian using Python3. 
There is always a chance that some of the underlying evironment on your device is different and that can cause certain commands to vary and potentialy throw exceptions. 
2) You will need to confirm that you have python3.x installed on your device. 
This can be accomplished by typing `python3 -V` into your terminal and pressing `Enter` inside your bash terminal. 
Else you will need to install Python3 by running `sudo apt-get install python<latest version, ie. 3.8>`

<b>Prepping your environment:</b>
One of the libraries used, `pythonping`, controls the socket layer of the OS and can only be modified by the root user. This also means that `$ sudo pip3` and `$ sudo python3` have to be used when installing the Python libraries and when executing the script.

1) Download and save the SystemStatistics.py file to your device in the directory of your choosing.  
I use `home/pi/Documents/Python`

2) Run the following commands in your bash terminal:  
`$ sudo pip3 install pyspectator`  
`$ sudo pip3 install pythonping`


<b>Running the script:</b>
Now, `cd` to the directory that you placed the python script and run:  
`$ sudo python3 SystemStatistics.py` 

You should now see a window appear with statistics updating every 2 seconds by default.

<b>Notes:</b>
As this program needs to be run as sudo I find it the easiest to run the code in your IDE of choice (im using Thonny) by executing a terminal command like `$ sudo thonny SystemStatistics.py`

If you want to modify the frequency of the GUI updating the system statistics, navigate to the `__init__()` method in the `MainWindow` class and change the value of the `self.sleepTime()`.
