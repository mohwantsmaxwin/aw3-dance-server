from flask import Flask, jsonify, request
from collections import deque
import os
import time

app = Flask(__name__)
queue = deque()
seen_users = set()
last_spawn_time = {}
COOLDOWN_SECONDS = 300  # same person can't spam, 5 min cooldown

@app.route('/spawn', methods=['POST'])
def spawn():
    data = request.get_json(force=True)
    username = data.get('username', '').strip()
    if not username:
        return jsonify({'ok': False, 'reason': 'no username'})
    
    username_lower = username.lower()
    now = time.time()
    
    # Don't add duplicates to queue
    if username_lower in seen_users:
        return jsonify({'ok': False, 'reason': 'already queued or spawned'})
    
    # Cooldown check
    if username_lower in last_spawn_time:
        if now - last_spawn_time[username_lower] < COOLDOWN_SECONDS:
            return jsonify({'ok': False, 'reason': 'cooldown'})
    
    seen_users.add(username_lower)
    last_spawn_time[username_lower] = now
    queue.append(username)
    print(f"Queued: {username} (queue size: {len(queue)})")
    return jsonify({'ok': True})

@app.route('/poll', methods=['GET'])
def poll():
    if queue:
        return jsonify({'username': queue.popleft()})
    return jsonify({'username': None})

@app.route('/clear', methods=['POST'])
def clear():
    queue.clear()
    seen_users.clear()
    last_spawn_time.clear()
    return jsonify({'ok': True, 'message': 'cleared'})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'queue_size': len(queue),
        'total_spawned': len(seen_users)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
