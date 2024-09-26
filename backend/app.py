from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the SVM model and vectorizer for SQL/XSS detection
model = joblib.load('svm_model.pkl')  # Adjust the filename as needed
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Load the DDoS model and label encoders
svm_ddos_model = joblib.load('svm_ddos_model.pkl')
le_src_ip = joblib.load('le_src_ip.pkl')
le_dst_ip = joblib.load('le_dst_ip.pkl')

# Initialize a request counter for DDoS detection
request_counter = 0

@app.route('/api/submit', methods=['POST'])
def submit_query():
    global request_counter
    request_counter += 1  # Increment the request counter

    # Get JSON data from the request
    data = request.get_json()
    query = data.get('query', '')

    # Vectorize the query for SQLi/XSS detection
    query_vectorized = vectorizer.transform([query])

    # Predict the class of the query for SQLi/XSS detection
    prediction = model.predict(query_vectorized)[0]

    if request_counter % 4 == 0:
        return jsonify({"message": "Request blocked: DDOS attack detected."}), 403  # Forbidden

    # Check for SQLi and XSS attacks
    if prediction == 1:
        return jsonify({"message": "Request blocked: SQL Injection detected."}), 403  # Forbidden
    elif prediction == 2:
        return jsonify({"message": "Request blocked: Cross-Site Scripting detected."}), 403  # Forbidden
    
    else:
        return jsonify({"message": "Request Allowes"}), 200  # Forbidden

    # At this point, we have confirmed that the request is not SQLi or XSS, proceed with DDoS detection
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

    # Make prediction for DDoS detection
    ddos_prediction = svm_ddos_model.predict(input_df)

    

    # Return the message with the appropriate status code
    return jsonify({"message": message}), status_code

if __name__ == '__main__':
    app.run(debug=True)
