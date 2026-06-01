from flask import Flask, jsonify, request
from collections import deque
import os

app = Flask(__name__)
queue = deque()

@app.route('/spawn', methods=['POST'])
def spawn():
    data = request.get_json(force=True)
    username = data.get('username', '').strip()
    if username:
        queue.append(username)
    return jsonify({'ok': True})

@app.route('/poll', methods=['GET'])
def poll():
    if queue:
        return jsonify({'username': queue.popleft()})
    return jsonify({'username': None})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
