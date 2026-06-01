from flask import Flask, jsonify, request
from collections import deque

app = Flask(__name__)
queue = deque()

@app.route('/spawn', methods=['POST'])
def spawn():
    data = request.json
    username = data.get('username','').strip()
    if username:
        queue.append(username)
    return jsonify({'ok': True})

@app.route('/poll', methods=['GET'])
def poll():
    if queue:
        return jsonify({'username': queue.popleft()})
    return jsonify({'username': None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)