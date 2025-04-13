import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import List, Tuple

class CPUTab(ttk.Frame):
    def __init__(self, parent, cpu_monitor):
        super().__init__(parent)
        self.cpu_monitor = cpu_monitor
        
        # Create CPU frame
        cpu_frame = ttk.LabelFrame(self, text="CPU Usage")
        cpu_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Overall CPU usage
        self.cpu_usage_label = ttk.Label(cpu_frame, text="0%", font=("Arial", 40))
        self.cpu_usage_label.pack(pady=10)
        
        # CPU progress bar
        self.cpu_progress = ttk.Progressbar(cpu_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.cpu_progress.pack(pady=10, padx=10, fill=tk.X)
        
        # Individual CPU cores frame
        cores_frame = ttk.Frame(cpu_frame)
        cores_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create a grid of CPU core indicators
        self.core_labels = []
        self.core_progress = []
        for i in range(self.cpu_monitor.get_cpu_count()):
            core_frame = ttk.Frame(cores_frame)
            core_frame.pack(fill=tk.X, padx=5, pady=2)
            
            label = ttk.Label(core_frame, text=f"Core {i}:")
            label.pack(side=tk.LEFT, padx=5)
            
            progress = ttk.Progressbar(core_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
            progress.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            self.core_labels.append(label)
            self.core_progress.append(progress)
        
        # CPU usage graph
        self.cpu_figure, self.cpu_ax = plt.subplots(figsize=(4, 2))
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_figure, cpu_frame)
        self.cpu_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_ax.set_title("CPU Usage Over Time (%)")
        
        # Create lines for each CPU core
        self.cpu_lines = []
        colors = plt.cm.viridis(np.linspace(0, 1, self.cpu_monitor.get_cpu_count()))
        for i in range(self.cpu_monitor.get_cpu_count()):
            line, = self.cpu_ax.plot([], [], color=colors[i], label=f'Core {i}')
            self.cpu_lines.append(line)
        self.cpu_ax.legend(loc='upper right')
    
    def update(self):
        """Update the CPU tab with current data"""
        # Get current CPU usage
        cpu_percent, cpu_percent_per_core = self.cpu_monitor.get_cpu_usage()
        
        # Update overall CPU widgets
        self.cpu_usage_label.config(text=f"{cpu_percent:.1f}%")
        self.cpu_progress["value"] = cpu_percent
        
        # Update individual core widgets
        for i, core_percent in enumerate(cpu_percent_per_core):
            self.core_progress[i]["value"] = core_percent
            self.core_labels[i].config(text=f"Core {i}: {core_percent:.1f}%")
        
        # Update graph
        overall_history, cores_history = self.cpu_monitor.get_cpu_history()
        x_data = list(range(len(overall_history)))
        
        for i, line in enumerate(self.cpu_lines):
            line.set_data(x_data, cores_history[i])
        self.cpu_ax.set_xlim(0, max(59, len(x_data)))
        self.cpu_figure.canvas.draw_idle() 