````markdown
# 🏭 Paint Shop Conveyor System Simulation

## 🎯 Project Overview

This project implements a **Discrete Event Simulation (DES)** of an automotive **paint shop conveyor system** using **SimPy**.  
The objective is to analyze **throughput, waiting time, resource utilization, and bottlenecks** in a 3-station production line:

**Cleaning → Primer → Painting**

The system realistically models random arrivals, machine constraints, FIFO queues, and a fixed shift duration to produce actionable optimization insights.

---

## ✨ Key Features

- 🚗 Realistic car arrivals (uniform: **8–12 minutes**)
- 🔁 Sequential station processing with **FIFO queues**
- 🚨 Real-time bottleneck detection (queue length > 3 cars)
- 📊 Performance metrics:
  - Utilization
  - Average waiting time
  - Throughput
  - Queue length
- 📁 Automatic **Excel logging** for analysis
- 📈 Presentation & interview ready outputs

---

## 📊 Simulation Results (480-Minute Shift)

- **Total Cars Completed:** 49  
- **Average System Time:** 674.42 minutes  

### 🚨 Bottleneck Summary

| Station | Utilization | Max Queue |
|-------|------------|-----------|
| 🎨 Painting | **355.89%** | 24 cars |
| 🧼 Cleaning | 172.40% | 21 cars |
| 🧪 Primer | Stable | Minimal |

> Utilization above 100% indicates **capacity overload**

---

## 🏗️ System Architecture

```text
CAR GENERATOR
      ↓
[CLEANING (1)]
      ↓
[PRIMER (2)]
      ↓
[PAINTING (1)]
      ↓
     EXIT

(All queues are FIFO)
````

A real-time **bottleneck monitor** tracks queue growth dynamically.

---

## 🚀 Quick Start

### Clone Repository

```bash
git clone https://github.com/Yatendra-K-yadav/Autonext_AI-Paint-Shop-Conveyor-System-Simulation.git
cd Autonext_AI-Paint-Shop-Conveyor-System-Simulation
```

### Create Virtual Environment

```bash
python -m venv myvenv
```

Activate:

**Windows**

```bash
myvenv\Scripts\activate
```

**macOS / Linux**

```bash
source myvenv/bin/activate
```

### Install Dependencies

```bash
pip install simpy openpyxl
```

### Run Simulation

```bash
python main.py
```

---

## 📁 Project Structure

```text
├── config.py                  # Simulation parameters
├── main.py                    # Entry point
├── src/
│   ├── simulation.py          # SimPy engine
│   ├── entities.py            # Car & Station classes
│   ├── metrics.py             # KPI calculations
│   └── bottleneck_detector.py # Real-time monitoring
├── output/
│   ├── simulation_log.txt
│   └── simulation_log.xlsx    # 📊 Excel analytics
├── README.md
└── .gitignore
```

---

## 🔧 Technologies Used

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| **Python 3.11+** | Core language             |
| **SimPy**        | Discrete event simulation |
| **openpyxl**     | Excel logging & analysis  |

---

## 📈 Sample Output

```text
================================================================================
STATION 3: PAINTING (CRITICAL BOTTLENECK)
Number of Machines: 1
Utilization: 355.89% ← OVERLOADED!
Max Queue Length: 24 cars
Average Wait Time: 420.45 minutes ← DISASTROUS!
================================================================================
```


## 📊 Excel Analysis

The simulation generates:

📁 `output/simulation_log.xlsx`

### Included Sheets

* **Events Log** – Timestamped simulation actions
* **Queue Evolution** – Bottleneck growth over time
* **Car Journeys** – Individual car lifecycle metrics

💡 Tip: Create a PivotChart (Queue Length vs Time) to visualize congestion.

---

## 🧪 Validation & Testing

* Arrival Rate: Uniform 8–12 min ✅
* Expected Output: 48–49 cars ✅
* Utilization >100% detection ✅
* Bottleneck alerts triggered **160+ times** ✅


**How does SimPy work?**

* `yield env.timeout()` simulates time
* `Resource` manages queues and contention

**How to fix the bottleneck?**
Add machine + smart scheduling → 20% gain at minimal cost

---

## 🔄 What-If Analysis

Edit `config.py`:

```python
PAINTING_MACHINES = 2
ARRIVAL_MIN = 15
ARRIVAL_MAX = 20
```

Re-run simulation to compare scenarios.
