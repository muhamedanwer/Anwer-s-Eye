# System Monitor

A Python-based system monitoring tool that provides real-time information about CPU, memory, disk, and process usage.

## System Architecture

```mermaid
graph TD
    %% Main Application Structure
    subgraph Main Application
        App[Application Core]
    end

    %% Monitoring Components
    subgraph Monitoring Layer
        CPU[CPU Monitor]
        MEM[Memory Monitor]
        DISK[Disk Monitor]
        PROC[Process Monitor]
    end

    %% UI Components
    subgraph UI Layer
        MW[Main Window]
        CT[CPU Tab]
        MT[Memory Tab]
        DT[Disk Tab]
        PT[Process Tab]
    end

    %% Data Flow
    subgraph Data Flow
        direction LR
        DC[Data Collection] --> DP[Data Processing] --> V[Visualization]
    end

    %% Connections
    App --> MW
    App --> CPU
    App --> MEM
    App --> DISK
    App --> PROC

    MW --> CT
    MW --> MT
    MW --> DT
    MW --> PT

    CPU --> CT
    MEM --> MT
    DISK --> DT
    PROC --> PT

    %% Styling
    classDef app fill:#f9f,stroke:#333,stroke-width:2px
    classDef monitor fill:#bbf,stroke:#333,stroke-width:2px
    classDef ui fill:#bfb,stroke:#333,stroke-width:2px
    classDef flow fill:#fbb,stroke:#333,stroke-width:2px

    class App app
    class CPU,MEM,DISK,PROC monitor
    class MW,CT,MT,DT,PT ui
    class DC,DP,V flow
```

## Features

- CPU Monitoring
  - Overall CPU usage
  - Per-core CPU usage
  - CPU frequency information
  - Historical CPU usage graphs

- Memory Monitoring
  - Physical memory usage
  - Swap memory usage
  - Memory usage graphs
  - Detailed memory statistics

- Disk Monitoring
  - Disk I/O rates
  - Disk usage per partition
  - I/O history graphs
  - Partition usage details

- Process Management
  - List of running processes
  - Process details (CPU, memory, status)
  - Process sorting options
  - Process termination capability

## Installation

1. Clone the repository:
```bash
git clone https://github.com/muhamedanwer/Anwer-s-Eye
cd Anwer-s-Eye
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

## Project Structure

```
sys_mon/
├── src/
│   ├── monitor/
│   │   ├── cpu_monitor.py
│   │   ├── memory_monitor.py
│   │   ├── disk_monitor.py
│   │   └── process_monitor.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── cpu_tab.py
│   │   ├── memory_tab.py
│   │   ├── disk_tab.py
│   │   └── process_tab.py
├── requirements.txt
└── main.py
```

## Dependencies

- psutil: System and process utilities
- matplotlib: Plotting library
- numpy: Numerical computing

## License

MIT License 
