import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MemoryTab(ttk.Frame):
    def __init__(self, parent, memory_monitor):
        super().__init__(parent)
        self.memory_monitor = memory_monitor
        
        # Create memory frame
        memory_frame = ttk.LabelFrame(self, text="Memory Usage")
        memory_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Memory usage label
        self.memory_usage_label = ttk.Label(memory_frame, text="0%", font=("Arial", 40))
        self.memory_usage_label.pack(pady=10)
        
        # Memory progress bar
        self.memory_progress = ttk.Progressbar(memory_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.memory_progress.pack(pady=10, padx=10, fill=tk.X)
        
        # Memory details
        self.memory_detail_label = ttk.Label(memory_frame, text="0 GB / 0 GB")
        self.memory_detail_label.pack(pady=5)
        
        # Memory usage graph
        self.memory_figure, self.memory_ax = plt.subplots(figsize=(4, 2))
        self.memory_canvas = FigureCanvasTkAgg(self.memory_figure, memory_frame)
        self.memory_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.memory_ax.set_ylim(0, 100)
        self.memory_ax.set_title("Memory Usage Over Time (%)")
        self.memory_line, = self.memory_ax.plot([], [], 'g-')
        
        # Swap memory frame
        swap_frame = ttk.LabelFrame(self, text="Swap Memory")
        swap_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Swap usage label
        self.swap_usage_label = ttk.Label(swap_frame, text="0%", font=("Arial", 20))
        self.swap_usage_label.pack(pady=5)
        
        # Swap progress bar
        self.swap_progress = ttk.Progressbar(swap_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.swap_progress.pack(pady=5, padx=10, fill=tk.X)
        
        # Swap details
        self.swap_detail_label = ttk.Label(swap_frame, text="0 GB / 0 GB")
        self.swap_detail_label.pack(pady=5)
    
    def update(self):
        """Update the memory tab with current data"""
        # Get memory usage
        memory = self.memory_monitor.get_memory_usage()
        swap = self.memory_monitor.get_swap_usage()
        
        # Update memory widgets
        self.memory_usage_label.config(text=f"{memory['percent']:.1f}%")
        self.memory_progress["value"] = memory['percent']
        
        memory_used_gb = memory['used'] / (1024 * 1024 * 1024)
        memory_total_gb = memory['total'] / (1024 * 1024 * 1024)
        self.memory_detail_label.config(text=f"{memory_used_gb:.1f} GB / {memory_total_gb:.1f} GB")
        
        # Update swap widgets
        self.swap_usage_label.config(text=f"{swap['percent']:.1f}%")
        self.swap_progress["value"] = swap['percent']
        
        swap_used_gb = swap['used'] / (1024 * 1024 * 1024)
        swap_total_gb = swap['total'] / (1024 * 1024 * 1024)
        self.swap_detail_label.config(text=f"{swap_used_gb:.1f} GB / {swap_total_gb:.1f} GB")
        
        # Update memory graph
        memory_history = self.memory_monitor.get_memory_history()
        x_data = list(range(len(memory_history)))
        
        self.memory_line.set_data(x_data, memory_history)
        self.memory_ax.set_xlim(0, max(59, len(x_data)))
        self.memory_figure.canvas.draw_idle() 