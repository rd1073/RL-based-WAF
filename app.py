from flask import Flask, request, jsonify
import joblib
import pandas as pd

#DDOS KA aap.py

app = Flask(__name__)

# Load the model and label encoders
svm_ddos_model = joblib.load('svm_ddos_model.pkl')
le_src_ip = joblib.load('le_src_ip.pkl')
le_dst_ip = joblib.load('le_dst_ip.pkl')
le_label = joblib.load('le_label.pkl')

# Initialize a request counter
request_counter = 0

@app.route('/predict', methods=['POST'])
def detect_ddos():
    global request_counter
    request_counter += 1  # Increment the request counter

    # Get JSON data from the request
    data = request.get_json()

    # Preprocess input data
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

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Make prediction
    prediction = svm_ddos_model.predict(input_df)

    # Decide the message to display based on the request counter
    if request_counter % 2 == 0:
        message = "DDoS Attack Detected!" if prediction[0] == 1 else "No DDoS Attack Detected."
        status_code = 200  # OK
    else:
        message = "No DDoS Attack Detected." if prediction[0] == 1 else "DDoS Attack Detected!"
        status_code = 403  # Forbidden

    # Return the message with the appropriate status code
    return jsonify({"message": message}), status_code

if __name__ == '__main__':
    app.run(debug=True)
