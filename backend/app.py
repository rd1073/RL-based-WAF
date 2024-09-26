from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load the SVM model and vectorizer
model = joblib.load('svm_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
model_ddos = joblib.load('svm_ddos_model.pkl')  # Model for DDoS detection
le_src_ip = joblib.load('le_src_ip.pkl')
le_dst_ip = joblib.load('le_dst_ip.pkl')
le_label = joblib.load('le_label.pkl')


@app.route('/api/submit', methods=['POST'])
def submit_query():
    data = request.get_json()

    def check_ddos():
        src_ip = data.get('src_ip', '')
        dst_ip = data.get('dst_ip', '')
        tcp_srcport = data.get('tcp_srcport', 0)
        tcp_dstport = data.get('tcp_dstport', 0)
        ip_proto = data.get('ip_proto', 0)  # This should match the dataset's protocol values
        tcp_flags_syn = data.get('tcp_flags_syn', 0)
        tcp_flags_reset = data.get('tcp_flags_reset', 0)
        tcp_flags_push = data.get('tcp_flags_push', 0)
        tcp_flags_ack = data.get('tcp_flags_ack', 0)
        ip_flags_mf = data.get('ip_flags_mf', 0)
        ip_flags_df = data.get('ip_flags_df', 0)
        ip_flags_rb = data.get('ip_flags_rb', 0)
        tcp_seq = data.get('tcp_seq', 0)
        tcp_ack = data.get('tcp_ack', 0)
        packets = data.get('packets', 0)
        bytes_count = data.get('bytes', 0)
        data = request.get_json()

        # Prepare the features for DDoS prediction
        ddos_features = np.array([[
        le_src_ip.transform([src_ip])[0],  # Encode source IP
        le_dst_ip.transform([dst_ip])[0],  # Encode destination IP
        tcp_srcport,
        tcp_dstport,
        ip_proto,
        tcp_flags_syn,
        tcp_flags_reset,
        tcp_flags_push,
        tcp_flags_ack,
        ip_flags_mf,
        ip_flags_df,
        ip_flags_rb,
        tcp_seq,
        tcp_ack,
        packets,
        bytes_count ]])
     # Predict DDoS attack
        ddos_prediction = model_ddos.predict(ddos_features)[0]

        if ddos_prediction == le_label.transform(['DDoS-PSH-ACK'])[0]:  # Adjust based on your label encoding
            response={"message": "Request blocked: DDoS attack detected."}
        return None
    

    # Check for DDoS first
    
        





    
    query = data.get('query', '')

    # Vectorize the query
    query_vectorized = vectorizer.transform([query])

    # Predict the class of the query
    prediction = model.predict(query_vectorized)[0]

    # Create response based on prediction
    if prediction == 1:
        response = {"message": "Request blocked: SQL Injection detected."}
    elif prediction == 2:
        response = {"message": "Request blocked: Cross-Site Scripting detected."}
    else:
        ddos_response = check_ddos()
        if ddos_response:
            return jsonify(ddos_response), 200
        else:
            response = {"message": "Request allowed."}


    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)