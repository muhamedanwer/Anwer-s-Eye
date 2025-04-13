import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DiskTab(ttk.Frame):
    def __init__(self, parent, disk_monitor):
        super().__init__(parent)
        self.disk_monitor = disk_monitor
        
        # Create disk I/O frame
        disk_io_frame = ttk.LabelFrame(self, text="Disk I/O")
        disk_io_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Disk I/O stats
        self.disk_stats_frame = ttk.Frame(disk_io_frame)
        self.disk_stats_frame.pack(fill=tk.X, pady=5)
        
        self.read_speed_label = ttk.Label(self.disk_stats_frame, text="Read: 0 MB/s")
        self.read_speed_label.pack(side=tk.LEFT, padx=20)
        
        self.write_speed_label = ttk.Label(self.disk_stats_frame, text="Write: 0 MB/s")
        self.write_speed_label.pack(side=tk.LEFT, padx=20)
        
        # Disk I/O graph
        self.disk_figure, self.disk_ax = plt.subplots(figsize=(8, 3))
        self.disk_canvas = FigureCanvasTkAgg(self.disk_figure, disk_io_frame)
        self.disk_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.disk_ax.set_title("Disk I/O (MB/s)")
        self.disk_read_line, = self.disk_ax.plot([], [], 'r-', label='Read')
        self.disk_write_line, = self.disk_ax.plot([], [], 'b-', label='Write')
        self.disk_ax.legend()
        
        # Create disk usage frame
        disk_usage_frame = ttk.LabelFrame(self, text="Disk Usage")
        disk_usage_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a frame for each partition
        self.partition_frames = {}
        self.partition_labels = {}
        self.partition_progress = {}
    
    def update(self):
        """Update the disk tab with current data"""
        # Get disk I/O
        read_mb_per_sec, write_mb_per_sec = self.disk_monitor.get_disk_io()
        
        # Update disk I/O widgets
        self.read_speed_label.config(text=f"Read: {read_mb_per_sec:.2f} MB/s")
        self.write_speed_label.config(text=f"Write: {write_mb_per_sec:.2f} MB/s")
        
        # Update disk I/O graph
        disk_io_history = self.disk_monitor.get_disk_io_history()
        x_data = list(range(len(disk_io_history)))
        
        read_data = [data[0] for data in disk_io_history]
        write_data = [data[1] for data in disk_io_history]
        
        self.disk_read_line.set_data(x_data[:len(read_data)], read_data)
        self.disk_write_line.set_data(x_data[:len(write_data)], write_data)
        
        max_value = max(max(read_data, default=1), max(write_data, default=1))
        self.disk_ax.set_ylim(0, max_value * 1.1 or 1)
        self.disk_ax.set_xlim(0, max(59, len(x_data)))
        self.disk_figure.canvas.draw_idle()
        
        # Update disk usage
        disk_usage = self.disk_monitor.get_disk_usage()
        
        # Remove old partition frames
        for mountpoint in list(self.partition_frames.keys()):
            if mountpoint not in disk_usage:
                self.partition_frames[mountpoint].destroy()
                del self.partition_frames[mountpoint]
                del self.partition_labels[mountpoint]
                del self.partition_progress[mountpoint]
        
        # Update or create partition frames
        for mountpoint, usage in disk_usage.items():
            if mountpoint not in self.partition_frames:
                # Create new partition frame
                frame = ttk.Frame(self.winfo_children()[1])  # disk_usage_frame
                frame.pack(fill=tk.X, padx=5, pady=2)
                
                label = ttk.Label(frame, text=mountpoint)
                label.pack(side=tk.LEFT, padx=5)
                
                progress = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
                progress.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                detail = ttk.Label(frame, text="")
                detail.pack(side=tk.LEFT, padx=5)
                
                self.partition_frames[mountpoint] = frame
                self.partition_labels[mountpoint] = (label, detail)
                self.partition_progress[mountpoint] = progress
            
            # Update partition widgets
            used_gb = usage['used'] / (1024 * 1024 * 1024)
            total_gb = usage['total'] / (1024 * 1024 * 1024)
            
            self.partition_progress[mountpoint]["value"] = usage['percent']
            self.partition_labels[mountpoint][1].config(
                text=f"{used_gb:.1f} GB / {total_gb:.1f} GB ({usage['percent']:.1f}%)"
            ) 