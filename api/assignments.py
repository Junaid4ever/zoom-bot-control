from http.server import BaseHTTPRequestHandler
import json
import time

# Global storage
assignments = {}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract colab_id from path
        path = self.path
        colab_id = path.split('/')[-1]
        
        # Get pending assignments
        pending = assignments.get(colab_id, [])
        
        # Clear after sending
        if colab_id in assignments:
            del assignments[colab_id]
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'assignments': pending}
        self.wfile.write(json.dumps(response).encode())
        return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return