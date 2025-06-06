from flask import Flask, send_file, request, jsonify,render_template_string
import requests
import boto3
import json
from flask import redirect
app = Flask(__name__)

# ✅ Backend internal load balancer URL
BACKEND_URL = "http://172.16.0.4:8080"



@app.route('/')
def index():
    return send_file('index.html')

@app.route('/get_data')
def get_data():
    return send_file('get_data.html')

@app.route('/delete')
def delete():
    return send_file('delete.html')


@app.route('/data')
def data():
    return send_file('data.html')

# ✅ Proxy /submit to backend + push message to SQS
@app.route('/submit', methods=['POST'])
def proxy_submit():
    form_data = request.form.to_dict()
    try:
        # Forward form data to backend submit endpoint
        response = requests.post(f"{BACKEND_URL}/submit", data=form_data)
        return redirect('/submitteddata')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/submitteddata")
def submitted_data():
    try:
        response = requests.get(f"{BACKEND_URL}/submitteddata")
        response.raise_for_status()
        users = response.json()
    except Exception as e:
        users = []

    # Read HTML from file manually
    with open("submitteddata.html", "r") as f:
        html_content = f.read()

    # Inject variables
    return render_template_string(html_content, users=users)


# ✅ Proxy /get-data/<id> to backend (optional)
@app.route('/get-data/<int:user_id>', methods=['GET'])
def proxy_get_data(user_id):
    try:
        response = requests.get(f"{BACKEND_URL}/get-data/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Proxy /delete/<id> to backend (optional)
@app.route('/delete/<int:user_id>', methods=['DELETE'])
def proxy_delete(user_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/delete/{user_id}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
