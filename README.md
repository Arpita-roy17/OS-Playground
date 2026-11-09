# 💻 OS Playground – Interactive Operating System Simulator

An interactive web-based Operating System simulator built using Python and Streamlit. The project demonstrates important Operating System concepts through visualizations, simulations, and performance analysis.

## 📌 Project Overview

OS Playground is designed to make Operating System concepts easier to understand through practical experimentation.

Users can enter process details, execute CPU scheduling algorithms, compare their performance, understand starvation and aging, and examine resource allocation using Banker's Algorithm.

## 🎯 Objectives

- Understand fundamental Operating System concepts.
- Visualize CPU scheduling algorithms.
- Compare scheduling algorithms using performance metrics.
- Demonstrate process starvation and aging.
- Understand resource allocation and safe system states.
- Provide an interactive learning environment.

## ✨ Features

### 1. CPU Scheduling Simulator

Implements four CPU scheduling algorithms:

- **First Come First Serve (FCFS):** Processes execute in order of arrival.
- **Shortest Job First (SJF):** The ready process with the shortest burst time executes first. Non-preemptive implementation.
- **Priority Scheduling:** Processes execute according to priority. A smaller priority number indicates higher priority. Non-preemptive implementation.
- **Round Robin:** Each process receives CPU time according to a configurable time quantum.

Features include:
- Editable process details.
- Arrival time, burst time and priority inputs.
- Gantt chart visualization.
- Execution sequence.
- Completion time.
- Turnaround time.
- Waiting time.
- Response time.

### 2. Algorithm Comparison

Compares all four CPU scheduling algorithms using the same process inputs.

Includes:
- Performance comparison table.
- Average waiting time.
- Average turnaround time.
- Average response time.
- Performance graphs.
- Best-performing algorithm for each metric.
- Individual Gantt charts.

### 3. Starvation & Aging Simulator

Demonstrates how a process with low priority may wait for a long time while higher-priority processes continue executing.

The simulator compares:
- Scheduling without aging.
- Scheduling with aging.
- Process execution sequences.
- First CPU start time.
- Completion time.
- Total waiting time.

Aging gradually improves the priority of waiting processes to help prevent starvation.

### 4. Deadlock Simulator

Demonstrates resource allocation and system safety using **Banker's Algorithm**.

Includes:
- Allocation matrix.
- Maximum resource requirement matrix.
- Available resources.
- Need matrix calculation.
- Safe sequence identification.
- Safe and unsafe state detection.

The simulator helps explain how an operating system can avoid entering unsafe resource-allocation states.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data handling and tables |
| Matplotlib | Gantt chart visualization |

## 📂 Project Structure

```text
OS-Playground/
│
├── app.py             # Main Streamlit application
├── scheduling.py      # CPU scheduling algorithms
├── metrics.py         # Scheduling performance calculations
├── visualizer.py      # Gantt chart visualization
├── README.md          # Project documentation
└── venv/              # Python virtual environment
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Visual Studio Code (recommended)

### Step 1: Clone or download the project

Open a terminal in the project directory.

### Step 2: Create a virtual environment

```bash
python3 -m venv venv
```

### Step 3: Activate the virtual environment

For Linux or WSL Ubuntu:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install streamlit pandas matplotlib
```

### Step 5: Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 📊 Performance Metrics

The CPU Scheduling module calculates:

**1. Completion Time (CT)**

The time at which a process finishes execution.

**2. Turnaround Time (TAT)**

```text
TAT = Completion Time - Arrival Time
```

**3. Waiting Time (WT)**

```text
WT = Turnaround Time - Burst Time
```

**4. Response Time (RT)**

```text
RT = First CPU Start Time - Arrival Time
```

**5. Average Waiting Time**

```text
Average WT = Total Waiting Time / Number of Processes
```

Similar calculations are used for average turnaround time and average response time.

## 🎓 Operating System Concepts Covered

- Process scheduling
- CPU scheduling algorithms
- Preemptive and non-preemptive scheduling
- Scheduling performance metrics
- Gantt charts
- Process starvation
- Aging
- Deadlock
- Resource allocation
- Banker's Algorithm
- Safe and unsafe states

## 🚀 Future Enhancements

- Process synchronization simulation.
- Memory management and paging visualization.
- Page replacement algorithms (FIFO, LRU and Optimal).
- Disk scheduling algorithms.
- More advanced deadlock demonstrations.
- Exportable simulation reports.

## 👩‍💻 Project Information

**Project Name:** OS Playground – Interactive Operating System Simulator

**Domain:** Operating Systems

**Type:** Interactive Educational Web Application

**Developed Using:** Python, Streamlit, Pandas and Matplotlib

---

*OS Playground – Learn Operating Systems by Experimenting!*

