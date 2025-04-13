import psutil
from typing import List, Dict, Optional

class ProcessMonitor:
    def get_processes(self, sort_by: str = 'memory_percent', limit: int = 50) -> List[Dict]:
        """
        Get information about running processes.
        Args:
            sort_by: Field to sort by ('memory_percent', 'cpu_percent', 'name')
            limit: Maximum number of processes to return
        Returns:
            List[Dict]: List of process information dictionaries
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort processes
        if sort_by == 'memory_percent':
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        elif sort_by == 'cpu_percent':
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        elif sort_by == 'name':
            processes.sort(key=lambda x: x['name'].lower())
        
        return processes[:limit]
    
    def get_process_details(self, pid: int) -> Optional[Dict]:
        """
        Get detailed information about a specific process.
        Args:
            pid: Process ID
        Returns:
            Optional[Dict]: Process details or None if process not found
        """
        try:
            proc = psutil.Process(pid)
            return {
                'pid': proc.pid,
                'name': proc.name(),
                'status': proc.status(),
                'cpu_percent': proc.cpu_percent(),
                'memory_percent': proc.memory_percent(),
                'memory_info': proc.memory_info()._asdict(),
                'create_time': proc.create_time(),
                'num_threads': proc.num_threads(),
                'username': proc.username()
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
    
    def kill_process(self, pid: int) -> bool:
        """
        Kill a process by its PID.
        Args:
            pid: Process ID
        Returns:
            bool: True if process was killed, False otherwise
        """
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False 