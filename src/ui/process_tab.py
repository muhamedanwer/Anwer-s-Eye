import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ProcessTab(ttk.Frame):
    def __init__(self, parent, process_monitor):
        super().__init__(parent)
        self.process_monitor = process_monitor
        
        # Create process treeview
        columns = ("PID", "Name", "CPU %", "Memory %", "Status")
        self.process_tree = ttk.Treeview(self, columns=columns, show="headings")
        
        # Define headings
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Show Details", command=self.show_process_details)
        self.context_menu.add_command(label="Kill Process", command=self.kill_process)
        
        # Bind right-click event
        self.process_tree.bind("<Button-3>", self.show_context_menu)
        
        # Add refresh button
        refresh_button = ttk.Button(self, text="Refresh Processes", command=self.update)
        refresh_button.pack(pady=10)
        
        # Add sort options
        sort_frame = ttk.Frame(self)
        sort_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT, padx=5)
        
        self.sort_var = tk.StringVar(value="memory_percent")
        ttk.Radiobutton(sort_frame, text="Memory", variable=self.sort_var, 
                       value="memory_percent", command=self.update).pack(side=tk.LEFT)
        ttk.Radiobutton(sort_frame, text="CPU", variable=self.sort_var, 
                       value="cpu_percent", command=self.update).pack(side=tk.LEFT)
        ttk.Radiobutton(sort_frame, text="Name", variable=self.sort_var, 
                       value="name", command=self.update).pack(side=tk.LEFT)
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.process_tree.identify_row(event.y)
        if item:
            self.process_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def show_process_details(self):
        """Show detailed information about selected process"""
        selection = self.process_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        pid = int(self.process_tree.item(item)['values'][0])
        
        details = self.process_monitor.get_process_details(pid)
        if details:
            message = (
                f"PID: {details['pid']}\n"
                f"Name: {details['name']}\n"
                f"Status: {details['status']}\n"
                f"CPU %: {details['cpu_percent']:.1f}\n"
                f"Memory %: {details['memory_percent']:.1f}\n"
                f"Threads: {details['num_threads']}\n"
                f"User: {details['username']}\n"
                f"Created: {details['create_time']}"
            )
            messagebox.showinfo("Process Details", message)
        else:
            messagebox.showerror("Error", "Could not get process details")
    
    def kill_process(self):
        """Kill selected process"""
        selection = self.process_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        pid = int(self.process_tree.item(item)['values'][0])
        name = self.process_tree.item(item)['values'][1]
        
        if messagebox.askyesno("Confirm Kill", f"Are you sure you want to kill process {name} (PID: {pid})?"):
            if self.process_monitor.kill_process(pid):
                messagebox.showinfo("Success", f"Process {name} (PID: {pid}) killed successfully")
                self.update()
            else:
                messagebox.showerror("Error", f"Could not kill process {name} (PID: {pid})")
    
    def update(self):
        """Update the process list"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        # Get processes
        processes = self.process_monitor.get_processes(sort_by=self.sort_var.get())
        
        # Add processes to treeview
        for proc in processes:
            values = (
                proc['pid'],
                proc['name'],
                f"{proc['cpu_percent']:.1f}",
                f"{proc['memory_percent']:.1f}",
                proc['status']
            )
            self.process_tree.insert("", tk.END, values=values) 