import sys, json
from client import VectorClockCausalTracker

tracker = VectorClockCausalTracker()

def handle_jsonrpc(line):
    global tracker
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-vector-clock-causal-ordering-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "tick_clock", "description": "Tick logical clock.", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "compare_clocks", "description": "Compare two clocks.", "inputSchema": {"type": "object", "properties": {"clock_1": {"type": "object"}, "clock_2": {"type": "object"}}, "required": ["clock_1", "clock_2"]}},
                {"name": "benchmark_causal_tracking", "description": "Run benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "tick_clock":
                res = tracker.tick()
            elif tool == "compare_clocks":
                res = tracker.compare_clocks(args.get("clock_1", {}), args.get("clock_2", {}))
            elif tool == "benchmark_causal_tracking":
                res = tracker.benchmark_causal_tracking()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
