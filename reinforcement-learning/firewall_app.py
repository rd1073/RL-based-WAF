from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Load the Q-table
q_table = np.load("q_table.npy")

@app.route('/api/submit', methods=['POST'])
def submit_query():
    data = request.get_json()
    query = data.get('query', '')

    # Simple keyword matching for SQLi detection (could be enhanced)
    state = 0 if any(keyword in query.lower() for keyword in ['select', 'union', 'or', '--', 'drop']) else 1

    action = np.argmax(q_table[state])  # Get the action from the Q-table

    if action == 0:
        response = {"message": "Request blocked: SQL Injection detected."}
    else:
        response = {"message": "Request allowed."}

    return jsonify(response), 200

@app.route('/api/get_qtable', methods=['GET'])
def get_qtable():
    return jsonify(q_table.tolist()), 200

if __name__ == '__main__':
    app.run(debug=True)
