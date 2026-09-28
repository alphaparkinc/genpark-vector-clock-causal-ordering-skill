from client import VectorClockCausalTracker

def run_example():
    print("=== GenPark Vector Clock Example ===")
    tracker = VectorClockCausalTracker("node-A")
    tracker.tick()
    cmp_res = tracker.compare_clocks({"node-A": 1, "node-B": 0}, {"node-A": 1, "node-B": 1})
    print("Relationship:", cmp_res["causal_relationship"])

if __name__ == "__main__":
    run_example()
