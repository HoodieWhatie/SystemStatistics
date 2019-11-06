import os # Allows access to system statistics
import psutil # Allows access to virtual memor stats
from pyspectator.processor import Cpu # Python library for access resource stats (CPU)
from pyspectator.network import NetworkInterface # Library for access resource stats (NIC) 
from pythonping import ping # Library used for the simplified running of network commands
import re # Regex for detecting patterns in strings
import subprocess # Library for running terminal commands through Python
from time import sleep # Pauses code exection. Time passed to method in 'seconds'
import tkinter as tk # Library used to create the GUI and its widgets
from tkinter import *

mycolor = '#000000' # set your favourite rgb color
mycolor2 = '#430040'  # or use hex if you prefer 

class Application(tk.Frame):
    
    def __init__(self, master=None):
        self.root = tk.Tk()
        self.root.tk_setPalette(background=mycolor, foreground='black',
               activeBackground='black', activeForeground=mycolor2)
        self.root.geometry("500x150")
        self.root.title("SystemStatistics")
        self.cpu_temp = tk.Label(self.root, text="CPUTemp:")
        self.cpu_load = tk.Label(self.root, text="CPULoad:")
        self.memory_stats = tk.Label(self.root, text="RAM:")
        self.ip = tk.Label(self.root, text="IP:")
        self.mac = tk.Label(self.root, text="MAC:")
        self.network_status = tk.Label(self.root, text="NetStatus:")
        self.close_button = tk.Button(self.root, command=self.root.destroy, fg="red", text="Close")
        self.updateGUI()
    
    def run(self):
        self.cpu_temp.pack()
        self.cpu_load.pack()
        self.memory_stats.pack()
        self.network_status.pack()
        self.ip.pack()
        self.mac.pack()
        self.close_button.pack()
        while True:
            self.updateGUI()
            sleep(2)
        self.root.mainloop()
            
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
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB used of {int(mem.total/1000000)}MB"
        elif mem.percent >= 50 and mem.percent < 80:
            self.memory_stats["fg"] = "orange"
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB used of {int(mem.total/1000000)}MB"
        else:
            self.memory_stats["fg"] = "red"
            self.memory_stats["text"] = f"RAM: {int(mem.used/1000000)}MB used of {int(mem.total/1000000)}MB"        
        
        net_results = self.check_network_status()
        if net_results[1] == 4:
            self.network_status["fg"] = "green"
            self.network_status["text"] = f"NetStatus: Healthy | AvgLatency: {net_results[0]}"
        elif net_results[1] < 4 and net_results[1] > 0:
            self.network_status["fg"] = "orange"
            self.network_status["text"] = f"NetStatus: Problems | AvgLatency: {float(net_results[0])} | Success: {net_results[1]} Fail: {net_results[2]}"
        else:
            self.network_status["fg"] = "red"
            self.network_status["text"] = f"NetStatus: Failed | Success: {net_results[1]} Fail: {net_results[2]}"
        
        self.ip["fg"] = "white"
        self.ip["text"] = f"IP: {self.find_network_ip()}"
        self.mac["fg"] = "white"
        self.mac["text"] = f"MAC: {self.find_network_mac()}"
        self.root.update()
        
    def check_network_status(self):
        
        x = [str(reply) for reply in list(ping("8.8.8.8"))]
        pings = {}
        ping_count = 0
        latency = 0
        successes = 0
        failures = 0
        
        for reply in x:
        
            match = re.search("(\d+\.\d+)ms", reply)
            
            if 'group' in dir(match):
                pings[ping_count] = (match.group(1), True)
            else:
                pings[ping_count] = ("Failed", False)
            
            ping_count += 1
        
        for i in range(len(pings)):
            if pings[i][1] == True:
                latency += float(pings[i][0])
                successes += 1
            else:
                failures += 1
        
        if latency > 0:
            latency = "%.2f" % (latency/successes)
            return (float(latency),successes,failures)
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
    Application().run()


