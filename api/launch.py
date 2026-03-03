from http.server import BaseHTTPRequestHandler
import json
import time

# Global storage
colabs = {}
assignments = {}
bot_counter = 0

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global bot_counter
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            meeting_id = data.get('meeting_id')
            passcode = data.get('passcode', '')
            bot_count = int(data.get('bot_count', 10))
            duration = int(data.get('duration', 60))
            
            # Find available colabs
            available = []
            for cid, colab in colabs.items():
                if colab.get('busy_workers', 0) < 10:
                    available.append(cid)
            
            response_data = {'status': 'launched', 'bot_count': 0, 'bots': []}
            
            if available:
                # Simple distribution
                per_colab = bot_count // len(available)
                remainder = bot_count % len(available)
                
                for i, colab_id in enumerate(available):
                    count = per_colab + (1 if i < remainder else 0)
                    
                    if colab_id not in assignments:
                        assignments[colab_id] = []
                    
                    for j in range(count):
                        bot_counter += 1
                        bot_id = f"bot_{bot_counter}"
                        
                        assignments[colab_id].append({
                            'bot_id': bot_id,
                            'meeting_id': meeting_id,
                            'passcode': passcode,
                            'duration': duration
                        })
                        
                        if colab_id in colabs:
                            colabs[colab_id]['busy_workers'] = colabs[colab_id].get('busy_workers', 0) + 1
                            colabs[colab_id]['status'] = 'busy'
                        
                        response_data['bots'].append(bot_id)
                    
                    response_data['bot_count'] = len(response_data['bots'])
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
        
        return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return