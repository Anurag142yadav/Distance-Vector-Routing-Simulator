import time
from flask import Flask, render_template, jsonify

# --- This is our DVR logic from before ---
INFINITY = 16

class Router:
    def __init__(self, router_id):
        self.router_id = router_id
        self.neighbors = {}
        self.table = {}
        self.table[self.router_id] = {"cost": 0, "next_hop": self.router_id}

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost
        self.table[neighbor_id] = {"cost": cost, "next_hop": neighbor_id}

    def get_full_table(self):
        return self.table.copy()

    def update_table(self, all_tables_snapshot):
        table_changed = False
        new_table = {}
        new_table[self.router_id] = {"cost": 0, "next_hop": self.router_id}

        # Get all possible destinations from the snapshot
        all_destinations = set(all_tables_snapshot.keys())
        for router_table in all_tables_snapshot.values():
            all_destinations.update(router_table.keys())

        for dest in all_destinations:
            if dest not in new_table:
                new_table[dest] = {"cost": INFINITY, "next_hop": "-"}
        
        for neighbor_id, link_cost in self.neighbors.items():
            neighbor_table = all_tables_snapshot.get(neighbor_id, {})
            for destination_id, neighbor_data in neighbor_table.items():
                if neighbor_data.get("next_hop") == self.router_id:
                    continue 

                new_cost = link_cost + neighbor_data.get("cost", INFINITY)
                if new_cost >= INFINITY:
                    new_cost = INFINITY

                if new_cost < new_table[destination_id]["cost"]:
                    new_table[destination_id] = {
                        "cost": new_cost,
                        "next_hop": neighbor_id
                    }

        if self.table != new_table:
            self.table = new_table
            table_changed = True
        return table_changed

# --- This new class manages our whole network simulation ---
class Network:
    def __init__(self):
        self.routers = {}
        self.round_count = 0
        self.reset_network()

    def reset_network(self):
        """Resets the network to its initial state."""
        self.routers = {}
        self.round_count = 0
        
        router_A = Router("A")
        router_B = Router("B")
        router_C = Router("C")
        router_D = Router("D")
        
        # Add routers to the network
        self.routers = {
            "A": router_A,
            "B": router_B,
            "C": router_C,
            "D": router_D
        }

        # Define the topology
        router_A.add_neighbor("B", 2)
        router_A.add_neighbor("D", 1)

        router_B.add_neighbor("A", 2)
        router_B.add_neighbor("C", 3)
        router_B.add_neighbor("D", 7)

        router_C.add_neighbor("B", 3)
        router_C.add_neighbor("D", 11)

        router_D.add_neighbor("A", 1)
        router_D.add_neighbor("B", 7)
        router_D.add_neighbor("C", 11)
        
        print("--- Network Reset to Initial State ---")

    def step(self):
        """Runs one round of the simulation."""
        self.round_count += 1
        print(f"--- Simulating Round {self.round_count} ---")
        
        # 1. Get a snapshot of all tables *before* the round
        all_tables_snapshot = {}
        for router_id, router in self.routers.items():
            all_tables_snapshot[router_id] = router.get_full_table()

        # 2. Each router updates its table based on the snapshot
        network_changed = False
        for router in self.routers.values():
            if router.update_table(all_tables_snapshot):
                network_changed = True
                
        return network_changed

    def get_network_state(self):
        """Prepares the network state for the frontend."""
        state = {
            "round": self.round_count,
            "tables": {}
        }
        for router_id, router in self.routers.items():
            # Sort the table for consistent display
            sorted_table = dict(sorted(router.table.items()))
            state["tables"][router_id] = sorted_table
        return state

# --- This is the Flask (Web Server) part ---
app = Flask(__name__)

# Create a single, global network object
network = Network()

@app.route("/")
def home():
    """Serves the main HTML page."""
    # Flask automatically looks in the "templates" folder
    return render_template("index.html")

# --- API Endpoints ---

@app.route("/api/reset")
def api_reset():
    """Resets the simulation and returns the initial state."""
    network.reset_network()
    return jsonify(network.get_network_state())

@app.route("/api/step")
def api_step():
    """Runs one simulation step and returns the new state."""
    network_changed = network.step()
    state = network.get_network_state()
    state["converged"] = not network_changed
    return jsonify(state)

# --- Run the application ---
if __name__ == "__main__":
    app.run(debug=True)