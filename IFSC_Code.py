import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/ifsc', methods=['GET'])
def ifsc_info():
    ifsc = request.args.get('ifsc', '').strip().upper()
    if not ifsc:
        return jsonify({
            "error": "IFSC code parameter required (e.g., /ifsc?ifsc=HDFC0000001)",
            "credit": "@HYPERMX7"
        }), 400

    try:
        # Razorpay free public IFSC API (no key needed)
        resp = requests.get(f"https://ifsc.razorpay.com/{ifsc}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            data["credit"] = "@HYPERMX7"   # 👈 tera stamp har success response pe
            return jsonify(data)
        elif resp.status_code == 404:
            return jsonify({
                "error": "IFSC code not found in Razorpay database",
                "credit": "@HYPERMX7"
            }), 404
        else:
            return jsonify({
                "error": f"Razorpay API returned status {resp.status_code}",
                "credit": "@HYPERMX7"
            }), resp.status_code
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Razorpay API request timed out",
            "credit": "@HYPERMX7"
        }), 504
    except requests.RequestException as e:
        return jsonify({
            "error": f"Request failed: {str(e)}",
            "credit": "@HYPERMX7"
        }), 500

@app.route('/')
def home():
    return jsonify({
        "app": "IFSC Info API",
        "credit": "@HYPERMX7",
        "usage": "/ifsc?ifsc=HDFC0000001"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)