import psutil # Allows access to virtual memor stats
from pyspectator.processor import Cpu # Python library for access resource stats (CPU)
from pyspectator.network import NetworkInterface # Library for access resource stats (NIC) 
from pythonping import ping # Library used for the simplified running of network commands
import re # Regex for detecting patterns in strings
import subprocess # Library for running terminal commands through Python
import tkinter as tk # Library used to create the GUI and its widgets
from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import *
        
mycolor = "#000000"
mycolor2 = "#430040"

# ASCII Codes
#
# 35: #
# 4510: ᆞ
# 8718: ∎


# ToDoList
#  
# 1) Switch between C and F for CPU temp with radio button
# 2) Create "percentage bars" for CPU Load, RAM Utilization
# 3) Add Menu system with options


class MainWindow():
    
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
        
    def build_master_window(self):
        #self.master.tk_setPalette(background=mycolor, foreground="black", activeBackground="white", activeForeground="black")
        self.style = ttk.Style()
        self.style.theme_create("app_style", parent="alt",settings={
        ".":             {"configure": {"background"      : "dim grey",
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
                            "map"      : {"background"      : [("active", "spring green")],
                                        "foreground"      : [("active", 'black')]}},
            
        "TEntry":        {"configure": {"foreground"      : "black"}},
        "Horizontal.TProgressbar":{"configure": {"background": "slate gray"}}
        })
        self.style.theme_use("app_style")
        self.master.geometry("600x150")
        self.master.title("SystemStatistics")
        
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
        
    def menus(self):
        self.menu01 = tk.Menu(self.master)
        self.submenu01 = tk.Menu(self.menu01, tearoff=False)
        self.submenu01.add_command(label="Options",command=self.OpenOptionsMenu)
        self.menu01.add_cascade(label="File", menu=self.submenu01)
        self.master.config(menu=self.menu01)
        
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
      
    def destroyMe(self):
        self.master.destroy()
    
    def destroyApplication(self,timeToSleep=0):
        if timeToSleep > 0:
            self.master.after(timeToSleep*1000, self.destroyMe)
      
    def OpenOptionsMenu(self):
        print("Hey, hey, hey! Im FAT32!")
      
    def updateGUI(self):
        # CPU Temp
        _cpu_temp = float(self.find_cpu_temp())
        if _cpu_temp < 70:
            self.cpu_temp["foreground"] = "green"
            self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}C"
        elif _cpu_temp >= 71 and _cpu_temp < 85:
            self.cpu_temp["foreground"] = "orange"
            self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}C"
        else:
            self.cpu_temp["foreground"] = "red"
            self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}C"
        
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
        
        cpu_perc_on = chr(8718)
        cpu_perc_off = chr(4510)
        cpu_perc_on_count = cpu_perc_on * int((_cpu_load/10) + 1)
        cpu_perc_off_count = cpu_perc_off * (11 - len(cpu_perc_on_count))
        self.cpu_load_perc_bar["foreground"] = "violet red"
        self.cpu_load_perc_bar["text"] = f"CPU Load:\n[{cpu_perc_on_count}{cpu_perc_off_count}]"
        
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
        
        # ASCII Codes
        #
        # 35: #
        # 4510: ᆞ
        # 8718: ∎
        #
        mem_perc_on = chr(8718)
        mem_perc_off = chr(4510)
        mem_used = float("%.2f" % (mem.used/1000000))
        mem_total = float("%.2f" % (mem.total/1000000))
        mem_perc = int(float("%.2f" % (int(mem.used/1000000)/float(mem.total/1000000)*100.0))/10)
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
        
    def find_network_mac(self):
        
        net = NetworkInterface(monitoring_latency=1)
        return f"{net.hardware_address}"
    
    def find_network_ip(self):
        
        net = NetworkInterface(monitoring_latency=1)
        return f"{net.ip_address}"
    
    def find_memory_stats(self):
        return psutil.virtual_memory()
    
    def find_cpu_temp(self):
        
        cpu_temp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
        x = re.search("\d+\.\d+", cpu_temp)
        return x.group(0)
    
    def find_cpu_load(self):
        
        cpu = Cpu(monitoring_latency=1)
        return cpu.load
