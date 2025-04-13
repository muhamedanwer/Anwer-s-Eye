import tkinter as tk
from tkinter import ttk
import threading
import time

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("System Monitor")
        self.root.geometry("900x700")
        self.root.config(bg="#f0f0f0")
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tabs = {}
        
        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
    
    def add_tab(self, name: str, tab):
        """Add a new tab to the notebook"""
        self.tabs[name] = tab
        self.notebook.add(tab, text=name)
    
    def update_loop(self):
        """Main update loop for all tabs"""
        while self.running:
            try:
                # Update all tabs
                for tab in self.tabs.values():
                    tab.update()
                
                time.sleep(1)
            except Exception as e:
                print(f"Error in update loop: {e}")
    
    def start(self):
        """Start the application"""
        self.update_thread.start()
        self.root.mainloop()
    
    def stop(self):
        """Stop the application"""
        self.running = False
        self.root.destroy() 