import psutil
import collections
from typing import Tuple, Dict, List

class MemoryMonitor:
    def __init__(self, history_length: int = 60):
        self.memory_history = collections.deque(maxlen=history_length)
    
    def get_memory_usage(self) -> Dict[str, float]:
        """
        Get current memory usage information.
        Returns:
            Dict[str, float]: Dictionary containing memory usage information
        """
        memory = psutil.virtual_memory()
        self.memory_history.append(memory.percent)
        
        return {
            'percent': memory.percent,
            'used': memory.used,
            'total': memory.total,
            'available': memory.available,
            'free': memory.free
        }
    
    def get_memory_history(self) -> List[float]:
        """
        Get historical memory usage data.
        Returns:
            List[float]: List of memory usage percentages
        """
        return list(self.memory_history)
    
    def get_swap_usage(self) -> Dict[str, float]:
        """
        Get swap memory usage information.
        Returns:
            Dict[str, float]: Dictionary containing swap memory information
        """
        swap = psutil.swap_memory()
        return {
            'percent': swap.percent,
            'used': swap.used,
            'total': swap.total,
            'free': swap.free
        } 