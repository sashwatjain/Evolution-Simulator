
<h1 align="center">🧬 Evolution Simulator — Version 1</h1>

<p align="center">
A real-time artificial life simulation built with Python & Pygame  
<br>
Organisms compete, evolve, mutate, reproduce & adapt — just like real Darwinian evolution.
</p>

---

# 🎥 Simulation Preview
<!-- Replace with your GIF -->
<p align="center">
  <img src="SIMULATION_GIF.gif" width="700">
</p>

---

# 📖 Overview

**Evolution Simulator V1** is an artificial ecosystem where digital organisms interact with their environment and evolve over time.  
They must **search for food**, **stay hydrated**, **avoid starvation**, and **find mates** to reproduce.

Every organism has genes controlling:

- Speed  
- Size  
- Metabolism  
- Vision  
- Mutation rate  
- Reproduction thresholds  
- Sex (male/female)  
- Color channels (inherited + blended)  

Traits are inherited via **genetic crossover** and changed via **mutation**.  
Over time, species adapt to environmental constraints, creating true **natural selection**.

This simulation visualizes:

- 🧬 Genetic drift  
- 💥 Competition for resources  
- 💧 Survival pressure  
- 👨‍👩‍👧 Sexual reproduction  
- 🎨 Color blending inheritance  
- 📈 Long-term evolutionary trends  

---

# 🧠 Evolution Theory Demonstrated

### **1. Natural Selection**
Organisms best adapted to food/water availability survive longer and produce more offspring.

### **2. Mutation**
Random mutations introduce genetic variation, enabling new traits to emerge.

### **3. Sexual Reproduction**
Two parents contribute to one offspring, mixing traits and increasing diversity.

### **4. Fitness Pressure**
- High metabolism → faster starvation  
- High speed → better food access  
- Larger size → stronger presence but more resource cost  

The environment shapes species over many generations.

### **5. Extinction & Dominance**
Species may wipe each other out or dominate based on evolutionary advantage.

---

# 🧩 Tech Stack

| Component      | Used For |
|----------------|----------|
| **Python 3.12+** | Core logic |
| **Pygame**       | Rendering & simulation loop |
| **Numpy**        | Fast numerical ops |
| **Matplotlib**   | Population & trait graphs |
| **Custom Modules** | Physics, genetics, world logic |

---

# 📁 Folder Structure

    Evolution_Simulator/
    │
    ├── main.py # Game entry point
    ├── config.py # Global settings & species definitions
    │
    ├── core/
    │ ├── simulation.py # Main simulation engine
    │ ├── world.py # Food/Water plants
    │ ├── organisms.py # Organism class & attributes
    │ ├── genome.py # Genes, inheritance, mutation
    │ ├── physics.py # Movement, steering, wandering
    │ ├── utils.py # Helpers
    │
    ├── rendering/
    │ ├── renderer.py # Drawing organisms & plants
    │ ├── graphs.py # Population & trait graphs
    │
    ├── data/
    │ └── snapshots/ # Optional save slots
    │
    └── assets/ # Banners, icons, fonts



---

# 🚀 Features (V1)

### 🌱 Ecosystem
- Fruit-bearing plants  
- Water plants  
- Dynamic regrowth system  

### 🐣 Organisms
- Male = diamond-shaped  
- Female = circle-shaped  
- Size & color vary with genetics  
- Smooth movement & hunger-based behavior  

### 🧬 Genetics
- Genome with multiple traits  
- Crossover (two-parent mixing)  
- Mutation (Gaussian, drift, salt & pepper)  
- Color blending inheritance  
- Species tracking (Red, Green, Blue)  

### 📊 Graphs & Metrics
- Total population over time  
- Species population graph  
- Average size  
- Average speed  
- Evolution trendlines  

---

# ⚙️ Installation

### 1. Clone repository

git clone https://github.com/sashwatjain/Evolution_Simulator.git

cd Evolution_Simulator

### 2. Create virtual environment

python -m venv venv

venv\Scripts\activate # Windows

source venv/bin/activate # Mac/Linux

### 3. Install dependencies

pip install pygame numpy matplotlib

### 4. Run the simulation


---

# 🔧 Configuration

Open **config.py** to adjust:

- World size  
- Initial population  
- Food/water spawn rate  
- Species default genes  
- Max energy/water  
- Mutation types  
- Graph history length  

You can create unique evolution environments by customizing these.

---

# 🔮 Roadmap (Future Versions)

### V2 Planned Features:
- 🕹 Live UI sliders for changing environment  
- 👆 Click organism → detailed genome popup  
- 🌤 Seasonal cycles (scarcity → abundance)  
- 🐺 Predator species  
- 🧠 Evolving neural-network brains  
- 🎨 Better rendering (glow, outlines, animations)  
- 💾 Save/load evolution states  
- 📈 More advanced statistical graphs  

---

# 🤝 Contributing

Pull requests & suggestions are welcome!  
Feel free to fork and build upon the simulation.
Developer - Sashwat jain

---

<p align="center">
  ⭐ If you enjoy this project, give it a star on GitHub!  
</p>
