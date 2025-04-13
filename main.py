from src.monitor.cpu_monitor import CPUMonitor
from src.monitor.memory_monitor import MemoryMonitor
from src.monitor.disk_monitor import DiskMonitor
from src.monitor.process_monitor import ProcessMonitor
from src.ui.main_window import MainWindow
from src.ui.cpu_tab import CPUTab
from src.ui.memory_tab import MemoryTab
from src.ui.disk_tab import DiskTab
from src.ui.process_tab import ProcessTab

def main():
    # Create monitors
    cpu_monitor = CPUMonitor()
    memory_monitor = MemoryMonitor()
    disk_monitor = DiskMonitor()
    process_monitor = ProcessMonitor()
    
    # Create main window
    window = MainWindow()
    
    # Create and add tabs
    window.add_tab("CPU", CPUTab(window.notebook, cpu_monitor))
    window.add_tab("Memory", MemoryTab(window.notebook, memory_monitor))
    window.add_tab("Disk", DiskTab(window.notebook, disk_monitor))
    window.add_tab("Processes", ProcessTab(window.notebook, process_monitor))
    
    # Set up window close handler
    window.root.protocol("WM_DELETE_WINDOW", window.stop)
    
    # Start the application
    window.start()

if __name__ == "__main__":
    main()