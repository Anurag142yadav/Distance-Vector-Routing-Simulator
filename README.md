

## 💻 Interactive Distance Vector Routing (DVR) Simulator

A web-based, interactive simulation demonstrating the **Distance Vector Routing (DVR) algorithm** (Bellman-Ford) in a 4-router network. This tool provides a visual, step-by-step breakdown of how routers exchange information and **converge** on stable routing tables. It was developed to illustrate fundamental concepts in network routing for Engineering.

## ✨ Key Features

* **Step-by-Step Execution:** Manually control the pace of the simulation by running one round of the DVR algorithm with the **"Step"** button.
* **Visual Convergence:** Observe how routing tables update dynamically and track when the network achieves a fully **"converged"** (stable) state.
* **Bellman-Ford Logic:** Accurate backend implementation calculating the minimum-cost paths for all destinations.
* **Loop Prevention:** Critical implementation of the **Split Horizon** rule to mitigate the **"count-to-infinity"** problem.
* **Clear State Display:** Routing tables are rendered clearly showing the **Destination**, **Cost**, and **Next Hop** for each router.

## ⚙️ Architecture and Technology Stack

The simulator uses a classic Client-Server architecture:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend Logic** | **Python** | Contains the core `Router` and `Network` classes, implementing the DVR and Bellman-Ford algorithms. |
| **Web Server** | **Flask** | Provides the RESTful API endpoints (`/api/step`, `/api/reset`) to handle requests from the frontend. |
| **Frontend Interface** | **HTML/CSS/JavaScript** | Manages the UI, sends asynchronous `fetch` requests to the API, and dynamically renders the updated routing tables. |

## 🚀 Getting Started

Follow these steps to set up and run the simulator locally.

Prerequisites

You need Python installed on your system.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Anurag142yadav/Distance-Vector-Routing-Simulator.git
    cd Distance-Vector-Routing-Simulator
    ```

2.  **Install Flask:**
    ```bash
    pip install flask
    ```

### Running the Simulator

1.  **Start the Backend Server:**
    ```bash
    python app.py
    ```
    The server will typically start on `http://127.0.0.1:5000`.

2.  **Access the Application:**
    Open your web browser and navigate to the local server address: `http://127.0.0.1:5000`

### Usage

1.  The initial state (Round 0) will be displayed.
2.  Click the **"Step"** button to execute Round 1.
3.  Continue clicking **"Step"** to watch the routing tables change until the status indicates **"Converged."**
4.  Click **"Reset Simulation"** to restart the process.

---

### Project Details

* **Course:** BTech.
* **Team:** Anurag yadav & Aryan yadav
* **Professor:** Ass.Prof. Vimal Kumar
