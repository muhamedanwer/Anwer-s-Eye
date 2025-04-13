import psutil
import collections
import time
from typing import Dict, List, Tuple

class DiskMonitor:
    def __init__(self, history_length: int = 60):
        self.disk_io_history = collections.deque(maxlen=history_length)
        self.last_disk_io = psutil.disk_io_counters()
        self.last_time = time.time()
    
    def get_disk_usage(self) -> Dict[str, Dict[str, float]]:
        """
        Get disk usage information for all partitions.
        Returns:
            Dict[str, Dict[str, float]]: Dictionary containing disk usage information for each partition
        """
        disk_usage = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.mountpoint] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            except (PermissionError, psutil.AccessDenied):
                continue
        return disk_usage
    
    def get_disk_io(self) -> Tuple[float, float]:
        """
        Get current disk I/O rates.
        Returns:
            Tuple[float, float]: (read_mb_per_sec, write_mb_per_sec)
        """
        current_time = time.time()
        time_delta = current_time - self.last_time
        current_disk_io = psutil.disk_io_counters()
        
        read_bytes = current_disk_io.read_bytes - self.last_disk_io.read_bytes
        write_bytes = current_disk_io.write_bytes - self.last_disk_io.write_bytes
        
        read_mb_per_sec = read_bytes / (1024 * 1024) / time_delta
        write_mb_per_sec = write_bytes / (1024 * 1024) / time_delta
        
        self.disk_io_history.append((read_mb_per_sec, write_mb_per_sec))
        
        self.last_disk_io = current_disk_io
        self.last_time = current_time
        
        return read_mb_per_sec, write_mb_per_sec
    
    def get_disk_io_history(self) -> List[Tuple[float, float]]:
        """
        Get historical disk I/O data.
        Returns:
            List[Tuple[float, float]]: List of (read_mb_per_sec, write_mb_per_sec) tuples
        """
        return list(self.disk_io_history) 