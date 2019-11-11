import psutil # Allows access to virtual memor stats
from pyspectator.computer import Computer # Python library for accessing system architecture variables
from pyspectator.processor import Cpu # Python library for accessing resource stats (CPU)
from pyspectator.network import NetworkInterface # Library for accessing resource stats (NIC) 
from pythonping import ping # Library used for the simplified running of network commands
import re # Regex for detecting patterns in strings
import RPi.GPIO as GPIO
from signal import pause
import subprocess # Library for running terminal commands through Python
from time import sleep
import tkinter as tk # Library used to create the GUI and its widgets
from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import *
        
mycolor = "#000000"
mycolor2 = "#430040"

# ToDoList
#  
# All items completed
#
#    
# Main Window (MW)
#
class MainWindow():
    def __init__(self, master):
        
        # Object Variables
        self.lastIP = ""
        self.pingLatList = []
        self.sleepTime = 500
        self.isStopped = False
        self.cpuTempCelsius = True
        self.ledBoard = False
        self.ledPins = [5,11,9,10,22,27,17,4,15,14]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledPins, GPIO.OUT)
        
        # Create Window Elements
        self.master = master
        self.master.attributes("-topmost", True)
        self.buildMasterWindow()
        self.positioningFrames()
        self.widgets()
        self.menus()
        self.master.after(self.sleepTime, self.run)
        self.master.mainloop()
    #    
    # MW.Build Master Window
    #    
    def buildMasterWindow(self):
        #self.master.tk_setPalette(background=mycolor, foreground="black", activeBackground="white", activeForeground="black")
        self.style = ttk.Style()
        self.style.theme_create("app_style", parent="alt",settings={
        ".":             {"configure": {"background"      : "midnight blue",
                                        "foreground"      : "light grey",
                                        "relief"          : "flat",
                                        "highlightcolor"  : "spring green"}},
        
        "TFrame":             {"configure": {"background"      : "midnight blue",
                                             "foreground"      : "black",
                                             "relief"          : "flat",
                                             "highlightcolor"  : "spring green"}},

        "TLabel":        {"configure": {"foreground"      : "black",
                                        "background"      : "midnight blue",
                                        "padding"         : 0,
                                        "font"            : ("Calibri", 12)}},

        "TNotebook":     {"configure": {"padding"         : 5}},
        "TNotebook.Tab": {"configure": {"padding"         : [25, 5], 
                                        "foreground"      : "white"},
                            "map"      : {"background"      : [("selected", "slate gray")],
                                        "expand"          : [("selected", [1, 1, 1, 0])]}},

        "TCombobox":     {"configure": {"selectbackground": "dim grey",
                                        "fieldbackground" : "white",
                                        "background"      : "light grey",
                                        "foreground"      : "black"}},

        "TButton":       {"configure": {"font"            :("Calibri", 13, 'bold'),
                                        "background"      : "midnight blue",
                                        "foreground"      : "red"},
                                        "relief"          : "groove",
                            "map"      : {"background"      : [("active", "spring green")],
                                        "foreground"      : [("active", 'black')]}},
            
        "TEntry":        {"configure": {"foreground"      : "black"}},
        "Horizontal.TProgressbar":{"configure": {"background": "slate gray"}}
        })
        self.style.theme_use("app_style")
        self.master.geometry("550x175")
        self.master.title("SystemStatistics")
    #    
    # MW.Positioning Frames
    #    
    def positioningFrames(self):
        self.mainContainer = ttk.Frame(self.master, style="TFrame")
        self.topFrame = ttk.Frame(self.mainContainer, style="TFrame")
        self.bottomFrame = ttk.Frame(self.mainContainer, style="TFrame")
        self.topLeft = ttk.Frame(self.topFrame, style="TFrame")
        self.topRight = ttk.Frame(self.topFrame, style="TFrame")
        self.bottomLeft = ttk.Frame(self.bottomFrame, style="TFrame")
        self.bottomRight = ttk.Frame(self.bottomFrame, style="TFrame")
        self.mainContainer.pack(side="top", fill="both", expand=True)
        self.topFrame.pack(side="top", fill="x", expand=False)
        self.bottomFrame.pack(side="bottom", fill="x", expand=False)
        self.topLeft.pack(side="left", fill="x", padx=0, pady=0, expand=False)
        self.topRight.pack(side="right", fill="x", expand=False)
        self.bottomLeft.pack(side="left", fill="x", expand=False)
        self.bottomRight.pack(side="right", fill="x", expand=True)
    #    
    # MW.Widgets
    #
    def widgets(self):
        self.cpuTemp = ttk.Label(self.topLeft, text="CPUTemp:", font="Calibri 12 bold", justify="left")
        self.cpuLoad = ttk.Label(self.topLeft, text="CPULoad:", font="Calibri 12 bold", justify="left")
        self.memoryStats = ttk.Label(self.topLeft, text="RAM:", font="Calibri 12 bold", justify="left")
        self.networkStatus = ttk.Label(self.topRight, text="NetStatus:", font="Calibri 12 bold", justify="right")
        self.cpuLoadPercBar = ttk.Label(self.topFrame, font="Calibri 10", text="")
        self.memLoadPercBar = ttk.Label(self.topFrame, font="Calibri 10 ", text="")
        self.pcInfo = ttk.Label(self.bottomFrame, font="Calibri 8 bold", text="")
    #    
    # MW.Menus
    #        
    def menus(self):
        self.menu01 = tk.Menu(self.master)
        self.submenu01 = tk.Menu(self.menu01, tearoff=False)
        self.submenu01.add_command(label="Options",command=self.loadOptionsMenu)
        self.submenu01.add_command(label="Close",command=self.destroyApplication)
        self.menu01.add_cascade(label="File", menu=self.submenu01)
        self.master.config(menu=self.menu01)
    #    
    # MW.Run
    #        
    def run(self):
        if not self.isStopped:
            self.cpuTemp.pack()
            self.cpuLoad.pack()
            self.memoryStats.pack()
            self.networkStatus.pack()
            self.cpuLoadPercBar.pack()
            self.memLoadPercBar.pack()
            self.pcInfo.pack()
            self.updateGUI()
            self.master.after(self.sleepTime, self.run)
    #    
    # MW.Load Options Menu
    #     
    def loadOptionsMenu(self):
        self.optionsMenu = tk.Toplevel(self.master)
        self.optionsMenu.title("Options")
        self.optionsMenu.geometry("300x65")
        self.optionsMenu.mainContainer = ttk.Frame(self.optionsMenu, style="TFrame")
        self.optionsMenu.mainContainer.pack(side="top", fill="both", expand=True)
        self.loadOptionsWidgets()
        self.runOptionsMenu()
    #
    # MW.Load Options Widgets
    #
    def loadOptionsWidgets(self):
        self.optionsMenu.celsiusCheckbutton = ttk.Checkbutton(self.optionsMenu.mainContainer,text="Toggle ˚F",
                                                         variable=self.cpuTempCelsius,command=self.toggleCelsius)
        self.optionsMenu.ledCheckbutton = ttk.Checkbutton(self.optionsMenu.mainContainer,text="CPU Load LEDs",
                                                          variable=self.ledBoard,command=self.toggleLEDs)
        self.optionsMenu.closeButton = ttk.Button(self.optionsMenu.mainContainer,text="Close",command=self.closeMenu,style="TButton")
    #
    # MW.Run Options Menu
    #
    def runOptionsMenu(self):
        self.optionsMenu.celsiusCheckbutton.pack()
        self.optionsMenu.ledCheckbutton.pack()
        self.optionsMenu.closeButton.pack()
    #
    # MW.Toggle Celsius
    #
    def toggleCelsius(self):
        if self.cpuTempCelsius:
            self.cpuTempCelsius = False
        else:
            self.cpuTempCelsius = True
    #
    # MW.Toggle LEDs
    #
    def toggleLEDs(self):
        if self.ledBoard:
            self.ledBoard = False
        else:
            self.ledBoard = True
    #
    # MW.Celsius Toggle
    #
    def closeMenu(self):
        self.optionsMenu.destroy()
    #    
    # MW.Update GUI
    #
    def updateGUI(self):
        
        # System Information
        systemInfo = self.pullPCInfo()
        self.pcInfo["foreground"] = "white"
        self.pcInfo["text"] = f"System Details\nHostname: {systemInfo[0]}\nOS: {systemInfo[1]}\nCPU: {systemInfo[2]}\nCores: {systemInfo[3]}\nIP: {systemInfo[4]}\nMAC: {systemInfo[5]}"
        
        # CPU Temp 
        if self.cpuTempCelsius: 
            _cpuTemp = float(self.findCPUTemp()) # CELSIUS
            if _cpuTemp < 70:
                self.cpuTemp["foreground"] = "green"
                self.cpuTemp["text"] = f"CPUTemp: {_cpuTemp}˚C"
            elif _cpuTemp >= 71 and _cpuTemp < 85:
                self.cpuTemp["foreground"] = "orange"
                self.cpuTemp["text"] = f"CPUTemp: {_cpuTemp}˚C"
            else:
                self.cpuTemp["foreground"] = "red"
                self.cpuTemp["text"] = f"CPUTemp: {_cpuTemp}˚C"
        else: 
            _cpuTemp = int(float("%.2f" % ((float(self.findCPUTemp()) * (9/5))+32))) # FARENHEIT
            if _cpuTemp < 158:
                self.cpuTemp["foreground"] = "green"
                self.cpuTemp["text"] = f"CPUTemp: {_cpuTemp}˚F"
            elif _cpuTemp >= 159 and _cpuTemp < 185:
                self.cpuTemp["foreground"] = "orange"
                self.cpuTemp["text"] = f"CPUTemp: {_cpuTemp}˚F"
            else:
                self.cpuTemp["foreground"] = "red"
                self.cpuTemp["text"] = f"CPUTemp: {_cpuTemp}˚F"
        
        # CPU Load
        _cpuLoad = self.find_cpuLoad()
        if _cpuLoad < 50:
            self.cpuLoad["foreground"] = "green"
            self.cpuLoad["text"] = f"CPULoad: {_cpuLoad}%"
        elif _cpuLoad >= 50 and _cpuLoad < 80:
            self.cpuLoad["foreground"] = "orange"
            self.cpuLoad["text"] = f"CPULoad: {_cpuLoad}%"
        else:
            self.cpuLoad["foreground"] = "red"
            self.cpuLoad["text"] = f"CPULoad: {_cpuLoad}%"
            
        # CPU Load Bar
        cpuPercOn = chr(8718)
        cpuPercOff = chr(4510)
        cpuPercOnCount = cpuPercOn * int((_cpuLoad/10) + 1)
        cpuPercOffCount = cpuPercOff * (11 - len(cpuPercOnCount))
        self.cpuLoadPercBar["foreground"] = "violet red"
        self.cpuLoadPercBar["text"] = f"CPU Load:\n[{cpuPercOnCount}{cpuPercOffCount}]"
        
        # CPU Load LEDs
        pins = int(_cpuLoad/10)
        if self.ledBoard:
            GPIO.output(self.ledPins[:pins], GPIO.HIGH)
            GPIO.output(self.ledPins[pins:], GPIO.LOW)

        # Memory
        mem = self.findMemoryStats()
        if mem.percent < 50:
            self.memoryStats["foreground"] = "green"
            self.memoryStats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"
        elif mem.percent >= 50 and mem.percent < 80:
            self.memoryStats["foreground"] = "orange"
            self.memoryStats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"
        else:
            self.memoryStats["foreground"] = "red"
            self.memoryStats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"        
        
        # Memory Bar
        memPercOn = chr(8718)
        memPercOff = chr(4510)
        memUsed = float("%.2f" % (mem.used/1000000))
        memTotal = float("%.2f" % (mem.total/1000000))
        memPerc = int(float("%.2f" % (memUsed/memTotal*100)))
        memPercOnCount = memPercOn * int(memPerc/10 + 1)
        memPercOffCount = memPercOff * (11 - len(memPercOnCount))
        self.memLoadPercBar["foreground"] = "violet red"
        self.memLoadPercBar["text"] = f"RAM Load:\n[{memPercOnCount}{memPercOffCount}]"
        
        # Network Status
        try:
            netResults = self.checkNetworkStatus()
            if netResults[1] == 4:
                self.networkStatus["foreground"] = "green"
                self.networkStatus["text"] = f"NetStatus: Good\nLatency: Avg({netResults[0]}ms)\nMax({netResults[3]}ms)\nMin({netResults[4]}ms)"
            elif netResults[1] < 4 and netResults[1] > 0:
                self.networkStatus["foreground"] = "orange"
                self.networkStatus["text"] = f"NetStatus: Poor\nLatency: Avg({netResults[0]}ms)\nMax({netResults[3]}ms)\nMin({netResults[4]}ms)"
            else:
                self.networkStatus["foreground"] = "red"
                self.networkStatus["text"] = f"NetStatus: '8.8.8.8' is unreachable."
        except OSError:
            self.networkStatus["foreground"] = "red"
            self.networkStatus["text"] = f"NetStatus: Failed"
    #
    # MW.Pull PC Info
    #
    def pullPCInfo(self):
        cpu = Cpu(monitoring_latency=1)
        comp = Computer()
        
        os = comp.os
        hostname = comp.hostname
        cpuName = cpu.name
        cpuCoreCount = cpu.count
        ip = self.findNetworkIP()
        mac = self.find_network_mac()
        
        return (hostname, os, cpuName, cpuCoreCount, ip, mac)
    #    
    # MW.Check Network Status
    #        
    def checkNetworkStatus(self):
        
        x = [str(reply) for reply in list(ping("8.8.8.8"))]
        pings = {}
        pingCount = 0
        latency = 0
        successes = 0
        failures = 0
        
        for reply in x:
        
            match = re.search("(\d+\.\d+)ms", reply)
            
            if "group" in dir(match):
                pings[pingCount] = (match.group(1), True)
            else:
                pings[pingCount] = ("Failed", False)
            
            pingCount += 1
        
        for i in range(len(pings)):
            if pings[i][1] == True:
                self.pingLatList.append(float(pings[i][0]))
                successes += 1
            else:
                failures += 1
        
        if successes > 0:
            latency = "%.2f" % (sum(self.pingLatList)/float(len(self.pingLatList)))
            if len(self.pingLatList) > 100:
                _min = min(self.pingLatList)
                _max = max(self.pingLatList)
                self.pingLatList = self.pingLatList[:49]
                self.pingLatList.append(_min)
                self.pingLatList.append(_max)
            return (float(latency),successes,failures,max(self.pingLatList),min(self.pingLatList))
        else:
            return (0,successes,failures)
    #    
    # MW.Find Network MAC
    #        
    def find_network_mac(self):
        
        net = NetworkInterface(monitoring_latency=1)
        return f"{net.hardware_address}"
    #    
    # MW.Find Network IP
    #    
    def findNetworkIP(self):
        
        net = NetworkInterface(monitoring_latency=1)
        return f"{net.ip_address}"
    #    
    # MW.Find Memory Stats
    #    
    def findMemoryStats(self):
        return psutil.virtual_memory()
    #    
    # MW.Find CPU Temp
    #    
    def findCPUTemp(self):
        
        cpuTemp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
        x = re.search("\d+\.\d+", cpuTemp)
        return x.group(0)
    #    
    # MW.Find CPU Load
    #    
    def find_cpuLoad(self):
        
        cpu = Cpu(monitoring_latency=1)
        return cpu.load
    #    
    # MW.Destroy Me
    #      
    def destroyMe(self):
        self.master.destroy()
    #    
    # MW.Destroy Application
    #    
    def destroyApplication(self,timeToSleep=0):
        if timeToSleep > 0:
            self.master.after(timeToSleep*1000, self.destroyMe)
        else:
            self.destroyMe()
    #    
    # Options Menu Class (OM)
    #
class OptionsMenu():
    def __init__(self, master):
        
        # Object Variables
        self.lastIP = ""
        self.pingLatList = []
        self.sleepTime = 1000
        self.isStopped = False
        
        # Create Window Elements
        self.master = master
        self.buildMasterWindow()
        self.positioningFrames()
        self.widgets()
        self.menus()
        self.master.after(self.sleepTime, self.run)
        self.master.mainloop()
    #    
    # OM.Build Master Window
    #
    def buildMasterWindow(self):
        self.style.theme_use("app_style")
        self.master.geometry("150x150")
        self.master.title("SystemStatistics")
    #    
    # OM.Positioning Frames
    #       
    def positioningFrames(self):
        self.mainContainer = ttk.Frame(self.master, style="TFrame")
        self.topFrame = ttk.Frame(self.mainContainer, style="TFrame")
        self.bottomFrame = ttk.Frame(self.mainContainer, style="TFrame")
        self.topLeft = ttk.Frame(self.topFrame, style="TFrame")
        self.topRight = ttk.Frame(self.topFrame, style="TFrame")
        self.bottomLeft = ttk.Frame(self.bottomFrame, style="TFrame")
        self.bottomRight = ttk.Frame(self.bottomFrame, style="TFrame")
        self.mainContainer.pack(side="top", fill="both", expand=True)
        self.topFrame.pack(side="top", fill="x", expand=False)
        self.bottomFrame.pack(side="bottom", fill="both", expand=False)
        self.topLeft.pack(side="left", fill="x", padx=0, pady=0, expand=False)
        self.topRight.pack(side="right", fill="x", expand=False)
        self.bottomLeft.pack(side="left", fill="x", expand=True)
        self.bottomRight.pack(side="right", fill="x", expand=True)
    #    
    # OM.Widgets
    #
    def widgets(self):
        self.closeButton = ttk.Button(self.bottomFrame, command=self.master.destroy, text="Close",style="TButton")
    #    
    # OM.Run
    #      
    def run(self):
        if not self.isStopped:
            self.closeButton.pack(bottomFrame, style="TButton")
            self.updateGUI()
            self.master.after(self.sleepTime, self.run)
    #    
    # OM.Destroy Me
    #      
    def destroyMe(self):
        self.master.destroy()
    #    
    # OM.Destroy Application
    #    
    def destroyApplication(self,timeToSleep=0):
        if timeToSleep > 0:
            self.master.after(timeToSleep*1000, self.destroyMe)
    #    
    # OM.Update GUI
    #     
    def updateGUI(self):
        print("updating gui")
 