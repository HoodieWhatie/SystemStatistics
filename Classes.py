from gpiozero import LED
import psutil # Allows access to virtual memor stats
from pyspectator.processor import Cpu # Python library for access resource stats (CPU)
from pyspectator.network import NetworkInterface # Library for access resource stats (NIC) 
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
# 1) Switch between C and F for CPU temp with radio button
# 2) Create "percentage bars" for CPU Load, RAM Utilization
# 3) Add Menu system with options
#
#    
# Main Window (MW)
#
class MainWindow():
    def __init__(self, master):
        
        # Object Variables
        self.last_ip = ""
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
        self.build_master_window()
        self.positioning_frames()
        self.widgets()
        self.menus()
        self.master.after(self.sleepTime, self.run)
        self.master.mainloop()
    #    
    # MW.Build Master Window
    #    
    def build_master_window(self):
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
        self.master.geometry("600x150")
        self.master.title("SystemStatistics")
    #    
    # MW.Positioning Frames
    #    
    def positioning_frames(self):
        self.main_container = ttk.Frame(self.master, style="TFrame")
        self.top_frame = ttk.Frame(self.main_container, style="TFrame")
        self.bottom_frame = ttk.Frame(self.main_container, style="TFrame")
        self.top_left = ttk.Frame(self.top_frame, style="TFrame")
        self.top_right = ttk.Frame(self.top_frame, style="TFrame")
        self.bottom_left = ttk.Frame(self.bottom_frame, style="TFrame")
        self.bottom_right = ttk.Frame(self.bottom_frame, style="TFrame")
        self.main_container.pack(side="top", fill="both", expand=True)
        self.top_frame.pack(side="top", fill="x", expand=False)
        self.bottom_frame.pack(side="bottom", fill="both", expand=False)
        self.top_left.pack(side="left", fill="x", padx=0, pady=0, expand=False)
        self.top_right.pack(side="right", fill="x", expand=False)
        self.bottom_left.pack(side="left", fill="x", expand=True)
        self.bottom_right.pack(side="right", fill="x", expand=True)
    #    
    # MW.Widgets
    #
    def widgets(self):
        self.cpu_temp = ttk.Label(self.top_left, text="CPUTemp:", font="Calibri 12 bold", justify="left")
        self.cpu_load = ttk.Label(self.top_left, text="CPULoad:", font="Calibri 12 bold", justify="left")
        self.memory_stats = ttk.Label(self.top_left, text="RAM:", font="Calibri 12 bold", justify="left")
        self.network_status = ttk.Label(self.top_right, text="NetStatus:", font="Calibri 12 bold", justify="right")
        self.ip = ttk.Label(self.bottom_frame, text="IP:")
        self.mac = ttk.Label(self.bottom_frame, text="MAC:")
        self.cpu_load_perc_bar = ttk.Label(self.top_frame, font="Calibri 8 bold", text="")
        self.mem_load_perc_bar = ttk.Label(self.top_frame, font="Calibri 8 bold", text="")
        self.close_button = ttk.Button(self.bottom_frame, command=self.master.destroy, text="Close",style="TButton")
    #    
    # MW.Menus
    #        
    def menus(self):
        self.menu01 = tk.Menu(self.master)
        self.submenu01 = tk.Menu(self.menu01, tearoff=False)
        self.submenu01.add_command(label="Options",command=self.loadOptionsMenu)
        self.menu01.add_cascade(label="File", menu=self.submenu01)
        self.master.config(menu=self.menu01)
    #    
    # MW.Run
    #        
    def run(self):
        if not self.isStopped:
            self.cpu_temp.pack()
            self.cpu_load.pack()
            self.memory_stats.pack()
            self.network_status.pack()
            self.cpu_load_perc_bar.pack()
            self.mem_load_perc_bar.pack()
            self.ip.pack()
            self.mac.pack()
            self.close_button.pack()
            self.updateGUI()
            self.master.after(self.sleepTime, self.run)
    #    
    # MW.Load Options Menu
    #     
    def loadOptionsMenu(self):
        self.optionsMenu = tk.Toplevel(self.master)
        self.optionsMenu.title("Options")
        self.optionsMenu.geometry("300x65")
        self.optionsMenu.main_container = ttk.Frame(self.optionsMenu, style="TFrame")
        self.optionsMenu.main_container.pack(side="top", fill="both", expand=True)
        self.loadOptionsWidgets()
        self.runOptionsMenu()
    #
    # MW.Load Options Widgets
    #
    def loadOptionsWidgets(self):
        self.optionsMenu.celsiusCheckbutton = ttk.Checkbutton(self.optionsMenu.main_container,text="Toggle ˚F",
                                                         variable=self.cpuTempCelsius,command=self.toggleCelsius)
        self.optionsMenu.ledCheckbutton = ttk.Checkbutton(self.optionsMenu.main_container,text="CPU Load LEDs",
                                                          variable=self.ledBoard,command=self.toggleLEDs)
        self.optionsMenu.closeButton = ttk.Button(self.optionsMenu.main_container,text="Close",command=self.closeMenu,style="TButton")
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
        # CPU Temp 
        if self.cpuTempCelsius: 
            _cpu_temp = float(self.find_cpu_temp()) # CELSIUS
            if _cpu_temp < 70:
                self.cpu_temp["foreground"] = "green"
                self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}˚C"
            elif _cpu_temp >= 71 and _cpu_temp < 85:
                self.cpu_temp["foreground"] = "orange"
                self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}˚C"
            else:
                self.cpu_temp["foreground"] = "red"
                self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}˚C"
        else: 
            _cpu_temp = int(float("%.2f" % ((float(self.find_cpu_temp()) * (9/5))+32))) # FARENHEIT
            if _cpu_temp < 158:
                self.cpu_temp["foreground"] = "green"
                self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}˚F"
            elif _cpu_temp >= 159 and _cpu_temp < 185:
                self.cpu_temp["foreground"] = "orange"
                self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}˚F"
            else:
                self.cpu_temp["foreground"] = "red"
                self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}˚F"
        
        # CPU Load
        _cpu_load = self.find_cpu_load()
        if _cpu_load < 50:
            self.cpu_load["foreground"] = "green"
            self.cpu_load["text"] = f"CPULoad: {_cpu_load}%"
        elif _cpu_load >= 50 and _cpu_load < 80:
            self.cpu_load["foreground"] = "orange"
            self.cpu_load["text"] = f"CPULoad: {_cpu_load}%"
        else:
            self.cpu_load["foreground"] = "red"
            self.cpu_load["text"] = f"CPULoad: {_cpu_load}%"
        # CPU Load Bar
        cpu_perc_on = chr(8718)
        cpu_perc_off = chr(4510)
        cpu_perc_on_count = cpu_perc_on * int((_cpu_load/10) + 1)
        cpu_perc_off_count = cpu_perc_off * (11 - len(cpu_perc_on_count))
        self.cpu_load_perc_bar["foreground"] = "violet red"
        self.cpu_load_perc_bar["text"] = f"CPU Load:\n[{cpu_perc_on_count}{cpu_perc_off_count}]"
        # CPU Load LEDs
        pins = int(_cpu_load/10)
        #pinsOff = int(_cpu_load/10)
        if self.ledBoard:
            print(f"On: {self.ledPins[:pins]}")
            print(f"Off: {self.ledPins[pins:]}")
            GPIO.output(self.ledPins[:pins], GPIO.HIGH)
            GPIO.output(self.ledPins[pins:], GPIO.LOW)

        # Memory
        mem = self.find_memory_stats()
        if mem.percent < 50:
            self.memory_stats["foreground"] = "green"
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"
        elif mem.percent >= 50 and mem.percent < 80:
            self.memory_stats["foreground"] = "orange"
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"
        else:
            self.memory_stats["foreground"] = "red"
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"        
        # Memory Bar
        mem_perc_on = chr(8718)
        mem_perc_off = chr(4510)
        mem_used = float("%.2f" % (mem.used/1000000))
        mem_total = float("%.2f" % (mem.total/1000000))
        mem_perc = int(float("%.2f" % (int(mem_used/1000000)/float(mem_total/1000000)*100.0))/10)
        mem_perc_on_count = mem_perc_on * (mem_perc + 1)
        mem_perc_off_count = mem_perc_off * (11 - len(mem_perc_on_count))
        self.mem_load_perc_bar["foreground"] = "violet red"
        self.mem_load_perc_bar["text"] = f"RAM Load:\n[{mem_perc_on_count}{mem_perc_off_count}]"
        
        # Network Status
        try:
            net_results = self.check_network_status()
            if net_results[1] == 4:
                self.network_status["foreground"] = "green"
                self.network_status["text"] = f"NetStatus: Good\nLatency: Avg({net_results[0]}ms)\nMax({net_results[3]}ms)\nMin({net_results[4]}ms)"
            elif net_results[1] < 4 and net_results[1] > 0:
                self.network_status["foreground"] = "orange"
                self.network_status["text"] = f"NetStatus: Poor\nLatency: Avg({net_results[0]}ms)\nMax({net_results[3]}ms)\nMin({net_results[4]}ms)"
            else:
                self.network_status["foreground"] = "red"
                self.network_status["text"] = f"NetStatus: '8.8.8.8' is unreachable."
        except OSError:
            self.network_status["foreground"] = "red"
            self.network_status["text"] = f"NetStatus: Failed"
        
        # IP Address
        current_ip = self.find_network_ip()
        if current_ip != self.last_ip:
            last_ip = current_ip
            self.ip["foreground"] = "white"
            self.ip["text"] = f"IP: {last_ip}"
        
        # MAC Address
        self.mac["foreground"] = "white"
        self.mac["text"] = f"MAC: {self.find_network_mac()}"
        self.master.update()
    #    
    # MW.Check Network Status
    #        
    def check_network_status(self):
        
        x = [str(reply) for reply in list(ping("8.8.8.8"))]
        pings = {}
        ping_count = 0
        latency = 0
        successes = 0
        failures = 0
        
        for reply in x:
        
            match = re.search("(\d+\.\d+)ms", reply)
            
            if "group" in dir(match):
                pings[ping_count] = (match.group(1), True)
            else:
                pings[ping_count] = ("Failed", False)
            
            ping_count += 1
        
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
    def find_network_ip(self):
        
        net = NetworkInterface(monitoring_latency=1)
        return f"{net.ip_address}"
    #    
    # MW.Find Memory Stats
    #    
    def find_memory_stats(self):
        return psutil.virtual_memory()
    #    
    # MW.Find CPU Temp
    #    
    def find_cpu_temp(self):
        
        cpu_temp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
        x = re.search("\d+\.\d+", cpu_temp)
        return x.group(0)
    #    
    # MW.Find CPU Load
    #    
    def find_cpu_load(self):
        
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
    #    
    # Options Menu Class (OM)
    #
class OptionsMenu():
    def __init__(self, master):
        
        # Object Variables
        self.last_ip = ""
        self.pingLatList = []
        self.sleepTime = 1000
        self.isStopped = False
        
        # Create Window Elements
        self.master = master
        self.build_master_window()
        self.positioning_frames()
        self.widgets()
        self.menus()
        self.master.after(self.sleepTime, self.run)
        self.master.mainloop()
    #    
    # OM.Build Master Window
    #
    def build_master_window(self):
        self.style.theme_use("app_style")
        self.master.geometry("150x150")
        self.master.title("SystemStatistics")
    #    
    # OM.Positioning Frames
    #       
    def positioning_frames(self):
        self.main_container = ttk.Frame(self.master, style="TFrame")
        self.top_frame = ttk.Frame(self.main_container, style="TFrame")
        self.bottom_frame = ttk.Frame(self.main_container, style="TFrame")
        self.top_left = ttk.Frame(self.top_frame, style="TFrame")
        self.top_right = ttk.Frame(self.top_frame, style="TFrame")
        self.bottom_left = ttk.Frame(self.bottom_frame, style="TFrame")
        self.bottom_right = ttk.Frame(self.bottom_frame, style="TFrame")
        self.main_container.pack(side="top", fill="both", expand=True)
        self.top_frame.pack(side="top", fill="x", expand=False)
        self.bottom_frame.pack(side="bottom", fill="both", expand=False)
        self.top_left.pack(side="left", fill="x", padx=0, pady=0, expand=False)
        self.top_right.pack(side="right", fill="x", expand=False)
        self.bottom_left.pack(side="left", fill="x", expand=True)
        self.bottom_right.pack(side="right", fill="x", expand=True)
    #    
    # OM.Widgets
    #
    def widgets(self):
        self.close_button = ttk.Button(self.bottom_frame, command=self.master.destroy, text="Close",style="TButton")
    #    
    # OM.Run
    #      
    def run(self):
        if not self.isStopped:
            self.close_button.pack(bottom_frame, style="TButton")
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
