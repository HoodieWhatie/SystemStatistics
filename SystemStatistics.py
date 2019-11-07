import math
import os # Allows access to system statistics
import psutil # Allows access to virtual memor stats
from pyspectator.processor import Cpu # Python library for access resource stats (CPU)
from pyspectator.network import NetworkInterface # Library for access resource stats (NIC) 
from pythonping import ping # Library used for the simplified running of network commands
import re # Regex for detecting patterns in strings
import subprocess # Library for running terminal commands through Python
from time import sleep # Pauses code exection. Time passed to method in "seconds"
import tkinter as tk # Library used to create the GUI and its widgets
from tkinter import *

mycolor = "#000000"
mycolor2 = "#430040"


class Application(tk.Frame):
    
    def __init__(self, master):
        
        # Object Variables
        self.last_ip = ""
        self.ping_lat_list = []
        
        # Tkinter Window Elements
        self.master = master
        self.master.tk_setPalette(background=mycolor, foreground="black",
               activeBackground="black", activeForeground=mycolor2)
        self.master.geometry("500x165")
        self.master.title("SystemStatistics")
        
        self.main_container = Frame(master)
        self.top_frame = Frame(self.main_container)
        self.bottom_frame = Frame(self.main_container)
        self.top_left = Frame(self.top_frame)
        self.top_right = Frame(self.top_frame)
        self.main_container.pack(side="top", fill="both", expand=True)
        self.top_frame.pack(side="top", fill="x", expand=False)
        self.bottom_frame.pack(side="bottom", fill="both", expand=True)
        self.top_left.pack(side="left", fill="x", expand=True)
        self.top_right.pack(side="right", fill="x", expand=True)
        
        # Tkinter Widgets
        self.cpu_temp = tk.Label(self.top_left, text="CPUTemp:", font="Helvetica 14 bold")
        self.cpu_load = tk.Label(self.top_left, text="CPULoad:", font="Helvetica 14 bold", justify="left")
        self.memory_stats = tk.Label(self.top_left, text="RAM:", font="Helvetica 14 bold", justify="left")
        self.network_status = tk.Label(self.top_right, text="NetStatus:", font="Helvetica 14 bold", justify="right")
        self.ip = tk.Label(self.master, text="IP:")
        self.mac = tk.Label(self.master, text="MAC:")
        self.close_button = tk.Button(self.master, command=self.master.destroy, fg="red", text="Close")
        self.sleepTime = 500
        self.isStopped = False
        self.master.after(self.sleepTime, self.run)
        self.master.mainloop()
        
    def run(self):
        if not self.isStopped:
            self.cpu_temp.pack()
            self.cpu_load.pack()
            self.memory_stats.pack()
            self.network_status.pack()
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
      
    def updateGUI(self):
        # CPU Temp
        _cpu_temp = float(self.find_cpu_temp())
        if _cpu_temp < 70:
            self.cpu_temp["fg"] = "green"
            self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}C"
        elif _cpu_temp >= 71 and _cpu_temp < 85:
            self.cpu_temp["fg"] = "orange"
            self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}C"
        else:
            self.cpu_temp["fg"] = "red"
            self.cpu_temp["text"] = f"CPUTemp: {_cpu_temp}C"
        
        # CPU Load
        _cpu_load = self.find_cpu_load()
        if _cpu_load < 50:
            self.cpu_load["fg"] = "green"
            self.cpu_load["text"] = f"CPULoad: {_cpu_load}%"
        elif _cpu_load >= 50 and _cpu_load < 80:
            self.cpu_load["fg"] = "orange"
            self.cpu_load["text"] = f"CPULoad: {_cpu_load}%"
        else:
            self.cpu_load["fg"] = "red"
            self.cpu_load["text"] = f"CPULoad: {_cpu_load}%"
        
        # Memory
        mem = self.find_memory_stats()
        if mem.percent < 50:
            self.memory_stats["fg"] = "green"
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"
        elif mem.percent >= 50 and mem.percent < 80:
            self.memory_stats["fg"] = "orange"
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"
        else:
            self.memory_stats["fg"] = "red"
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB of {int(mem.total/1000000)}MB"        
        
        # Network Status
        try:
            net_results = self.check_network_status()
            if net_results[1] == 4:
                self.network_status["fg"] = "green"
                self.network_status["text"] = f"NetStatus: Good\nLatency: Avg({net_results[0]}ms)\nMax({net_results[3]}ms)\nMin({net_results[4]}ms)"
            elif net_results[1] < 4 and net_results[1] > 0:
                self.network_status["fg"] = "orange"
                self.network_status["text"] = f"NetStatus: Poor\nLatency: Avg({net_results[0]}ms)\nMax({net_results[3]}ms)\nMin({net_results[4]}ms)"
            else:
                self.network_status["fg"] = "red"
                self.network_status["text"] = f"NetStatus: '8.8.8.8' is unreachable."
        except OSError:
            self.network_status["fg"] = "red"
            self.network_status["text"] = f"NetStatus: Failed"
        
        # IP Address
        current_ip = self.find_network_ip()
        if current_ip != self.last_ip:
            last_ip = current_ip
            self.ip["fg"] = "white"
            self.ip["text"] = f"IP: {last_ip}"
        
        # MAC Address
        self.mac["fg"] = "white"
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
                self.ping_lat_list.append(float(pings[i][0]))
                successes += 1
            else:
                failures += 1
        
        if successes > 0:
            latency = "%.2f" % (sum(self.ping_lat_list)/float(len(self.ping_lat_list)))
            if len(self.ping_lat_list) > 100:
                    _min = min(self.ping_lat_list)
                    _max = max(self.ping_lat_list)
                    self.ping_lat_list = self.ping_lat_list[:49]
                    self.ping_lat_list.append(_min)
                    self.ping_lat_list.append(_max)
            return (float(latency),successes,failures,max(self.ping_lat_list),min(self.ping_lat_list))
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


if __name__ == "__main__":
    root = tk.Tk()
    application = Application(root)
    root.mainloop()


