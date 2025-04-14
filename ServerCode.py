from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with the actual IP address of your ESP32
ESP32_IP = "192.168.1.5"
ESP32_PORT = 80  # The port the ESP32 is listening on

# Store the latest status update from the ESP32
esp32_status = {'led_state': False} # Initialize LED state

@app.route('/')
def index():
    return render_template('index.html', status=esp32_status)

@app.route('/api/update_status', methods=['POST'])
def update_status():
    if request.is_json:
        data = request.get_json()
        global esp32_status
        esp32_status['led_state'] = data.get('led_state', False) # Update only LED state
        print(f"ESP32 Status Updated: {esp32_status}")
        return jsonify({"status": "success"}), 202
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/api/send_command', methods=['POST'])
def send_command():
    action = request.form.get('action')
    if action == 'toggle':
        try:
            esp32_url = f"http://{ESP32_IP}:{ESP32_PORT}/control"
            response = requests.post(esp32_url, data={'command': action})
            response.raise_for_status()
            return jsonify({'status': 'success', 'message': 'Toggle command sent to ESP32'})
        except requests.exceptions.RequestException as e:
            return jsonify({'status': 'error', 'message': f'Error communicating with ESP32: {e}'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Invalid command'}), 400

@app.route('/api/get_status')
def get_status():
    return jsonify(esp32_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)