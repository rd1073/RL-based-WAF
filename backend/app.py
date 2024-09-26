from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load the SVM model and vectorizer
model = joblib.load('svm_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

@app.route('/api/submit', methods=['POST'])
def submit_query():
    data = request.get_json()
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
        response = {"message": "Request allowed."}

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
