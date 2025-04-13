import psutil
import collections
from typing import List, Tuple

class CPUMonitor:
    def __init__(self, history_length: int = 60):
        self.num_cpus = psutil.cpu_count()
        self.cpu_history = collections.deque(maxlen=history_length)
        self.cpu_cores_history = [collections.deque(maxlen=history_length) for _ in range(self.num_cpus)]
    
    def get_cpu_usage(self) -> Tuple[float, List[float]]:
        """
        Get current CPU usage for overall and per-core.
        Returns:
            Tuple[float, List[float]]: (overall_cpu_percent, cpu_percent_per_core)
        """
        cpu_percent = psutil.cpu_percent()
        cpu_percent_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
        
        self.cpu_history.append(cpu_percent)
        for i, core_percent in enumerate(cpu_percent_per_core):
            self.cpu_cores_history[i].append(core_percent)
        
        return cpu_percent, cpu_percent_per_core
    
    def get_cpu_frequency(self) -> Tuple[float, float, float]:
        """
        Get CPU frequency information.
        Returns:
            Tuple[float, float, float]: (current_freq, min_freq, max_freq)
        """
        freq = psutil.cpu_freq()
        return freq.current, freq.min, freq.max
    
    def get_cpu_history(self) -> Tuple[List[float], List[List[float]]]:
        """
        Get historical CPU usage data.
        Returns:
            Tuple[List[float], List[List[float]]]: (overall_history, cores_history)
        """
        return list(self.cpu_history), [list(history) for history in self.cpu_cores_history]
    
    def get_cpu_count(self) -> int:
        """
        Get the number of CPU cores.
        Returns:
            int: Number of CPU cores
        """
        return self.num_cpus 