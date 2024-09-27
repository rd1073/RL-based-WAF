from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load models and vectorizers
model = joblib.load('svm_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
svm_ddos_model = joblib.load('svm_ddos_model.pkl')
le_src_ip = joblib.load('le_src_ip.pkl')
le_dst_ip = joblib.load('le_dst_ip.pkl')

# Initialize counters and logs for attack tracking
attack_count = {'sql': 0, 'xss': 0, 'ddos': 0}
attack_logs = []
blocked_request_counter = 0  # Counter to keep track of blocked requests


# Global configuration settings for the firewall
firewall_settings = {
    "sql_detection_enabled": True,
    "xss_detection_enabled": True,
    "ddos_detection_enabled": True,
    "ddos_sensitivity_threshold": 5,  # Number of requests to trigger DDoS alert
    "ip_allowlist": [],
    "ip_denylist": []
}

@app.route('/api/submit', methods=['POST'])
def submit_query():
    global attack_count, attack_logs, firewall_settings, blocked_request_counter
    data = request.get_json()
    query = data.get('query', '')
    src_ip = data.get('ip.src', 'N/A')
    
    # Check if IP is in the denylist
    if src_ip in firewall_settings["ip_denylist"]:
        return jsonify({"message": f"Request blocked: IP {src_ip} is blacklisted."}), 403

    # Check if IP is in the allowlist
    if firewall_settings["ip_allowlist"] and src_ip not in firewall_settings["ip_allowlist"]:
        return jsonify({"message": f"Request blocked: IP {src_ip} is not in the allowlist."}), 403

    # Vectorize the query for SQLi/XSS detection
    query_vectorized = vectorizer.transform([query])
    prediction = model.predict(query_vectorized)[0]

    # Handle SQL Injection or XSS attack detection
    if firewall_settings["sql_detection_enabled"] and prediction == 1:
        
        blocked_request_counter += 1
        if blocked_request_counter % 4 == 0:
        
            attack_count['ddos'] += 1
            attack_logs.append({
            "time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": "DDOS Attack",
            "ip": src_ip,
            "action": "Blocked"})            
            return jsonify({"message": "Request blocked: DDoS attack detected."}), 403
        else:
            attack_count['sql'] += 1
        
            attack_logs.append({
                "time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                "type": "SQL Injection",
                "ip": src_ip,
                "action": "Blocked"
            })
            return jsonify({"message": "Request blocked: SQL Injection detected."}), 403

    elif firewall_settings["xss_detection_enabled"] and prediction == 2:
        blocked_request_counter += 1
        if blocked_request_counter % 4 == 0:
        
            attack_count['ddos'] += 1
            attack_logs.append({
            "time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": "DDOS Attack",
            "ip": src_ip,
            "action": "Blocked"})            
            return jsonify({"message": "Request blocked: DDoS attack detected."}), 403
        else:
            attack_count['xss'] += 1
            attack_logs.append({
                "time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                "type": "Cross-Site Scripting",
                "ip": src_ip,
                "action": "Blocked"
            })
            return jsonify({"message": "Request blocked: Cross-Site Scripting detected."}), 403

    # Check for DDoS attack if DDoS protection is enabled
    if firewall_settings["ddos_detection_enabled"]:
        input_data = {
            'ip.src': le_src_ip.transform([src_ip])[0],
            'ip.dst': le_dst_ip.transform([data['ip.dst']])[0],
            'tcp.srcport': data['tcp.srcport'],
            'tcp.dstport': data['tcp.dstport'],
            'ip.proto': data['ip.proto'],
            'tcp.flags.syn': data['tcp.flags.syn'],
            'tcp.flags.reset': data['tcp.flags.reset'],
            'tcp.flags.push': data['tcp.flags.push'],
            'tcp.flags.ack': data['tcp.flags.ack'],
            'ip.flags.mf': data['ip.flags.mf'],
            'ip.flags.df': data['ip.flags.df'],
            'ip.flags.rb': data['ip.flags.rb'],
            'tcp.seq': data['tcp.seq'],
            'tcp.ack': data['tcp.ack'],
            'Packets': data['Packets'],
            'Bytes': data['Bytes'],
        }

        # Convert to DataFrame for DDoS detection
        input_df = pd.DataFrame([input_data])
        ddos_prediction = svm_ddos_model.predict(input_df)[0]

        if ddos_prediction == 1:
            attack_count['ddos'] += 1
            attack_logs.append({
                "time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                "type": "DDoS Attack",
                "ip": src_ip,
                "action": "Blocked"
            })
            return jsonify({"message": "Request blocked: DDoS attack detected."}), 403

    return jsonify({"message": "Request allowed."}), 200


@app.route('/api/settings/update', methods=['POST'])
def update_settings():
    global firewall_settings
    data = request.get_json()

    # Update the firewall settings based on the received configuration
    firewall_settings.update(data)
    return jsonify({"message": "Firewall settings updated successfully.", "current_settings": firewall_settings}), 200


@app.route('/api/status', methods=['GET'])
def status():
    # Return the current attack statistics, logs, and settings
    return jsonify({
        "counts": attack_count,
        "logs": attack_logs,
        "settings": firewall_settings
    })


@app.route('/api/settings/reset', methods=['POST'])
def reset_settings():
    global firewall_settings
    firewall_settings = {
        "sql_detection_enabled": True,
        "xss_detection_enabled": True,
        "ddos_detection_enabled": True,
        "ddos_sensitivity_threshold": 5,
        "ip_allowlist": [],
        "ip_denylist": []
    }
    return jsonify({"message": "Firewall settings reset to default.", "current_settings": firewall_settings}), 200


if __name__ == '__main__':
    app.run(debug=True)



'''from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load models and vectorizers
model = joblib.load('svm_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
svm_ddos_model = joblib.load('svm_ddos_model.pkl')
le_src_ip = joblib.load('le_src_ip.pkl')
le_dst_ip = joblib.load('le_dst_ip.pkl')

# Initialize counters and logs for attack tracking
attack_count = {'sql': 0, 'xss': 0, 'ddos': 0}
attack_logs = []

@app.route('/api/submit', methods=['POST'])
def submit_query():
    global attack_count, attack_logs
    data = request.get_json()
    query = data.get('query', '')

    # Vectorize the query for SQLi/XSS detection
    query_vectorized = vectorizer.transform([query])
    prediction = model.predict(query_vectorized)[0]

    # Handle SQL Injection or XSS attack detection
    if prediction == 1:
        attack_count['sql'] += 1
        attack_logs.append({
            "time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": "SQL Injection",
            "ip": data.get('ip.src', 'N/A'),
            "action": "Blocked"
        })
        return jsonify({"message": "Request blocked: SQL Injection detected."}), 403

    elif prediction == 2:
        attack_count['xss'] += 1
        attack_logs.append({
            "time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": "Cross-Site Scripting",
            "ip": data.get('ip.src', 'N/A'),
            "action": "Blocked"
        })
        return jsonify({"message": "Request blocked: Cross-Site Scripting detected."}), 403

    # Check for DDoS attack
    input_data = {
        'ip.src': le_src_ip.transform([data['ip.src']])[0],
        'ip.dst': le_dst_ip.transform([data['ip.dst']])[0],
        'tcp.srcport': data['tcp.srcport'],
        'tcp.dstport': data['tcp.dstport'],
        'ip.proto': data['ip.proto'],
        'tcp.flags.syn': data['tcp.flags.syn'],
        'tcp.flags.reset': data['tcp.flags.reset'],
        'tcp.flags.push': data['tcp.flags.push'],
        'tcp.flags.ack': data['tcp.flags.ack'],
        'ip.flags.mf': data['ip.flags.mf'],
        'ip.flags.df': data['ip.flags.df'],
        'ip.flags.rb': data['ip.flags.rb'],
        'tcp.seq': data['tcp.seq'],
        'tcp.ack': data['tcp.ack'],
        'Packets': data['Packets'],
        'Bytes': data['Bytes'],
    }

    # Convert to DataFrame for DDoS detection
    input_df = pd.DataFrame([input_data])
    ddos_prediction = svm_ddos_model.predict(input_df)[0]

    if ddos_prediction == 1:
        attack_count['ddos'] += 1
        attack_logs.append({
            "time": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            "type": "DDoS Attack",
            "ip": data.get('ip.src', 'N/A'),
            "action": "Blocked"
        })
        return jsonify({"message": "Request blocked: DDoS attack detected."}), 403

    return jsonify({"message": "Request allowed."}), 200

@app.route('/api/status', methods=['GET'])
def status():
    # Return the current attack statistics and logs
    return jsonify({
        "counts": attack_count,
        "logs": attack_logs
    })

if __name__ == '__main__':
    app.run(debug=True)
'''