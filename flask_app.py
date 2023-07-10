from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Access and process the data from the POST request
        data = request.json
        prompt = data.get("text", "")

        # Call the dependency script and pass the prompt as input using subprocess.Popen
        cmd = ["python", "main.py --openai-api-key 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"]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding="utf-8")

        # Write the prompt to the process stdin
        process.stdin.write(prompt)
        process.stdin.flush()

        # Read input from the request in chunks and feed it back to the process stdin
        while True:
            chunk = request.stream.read(4096)
            if not chunk:
                break
            process.stdin.write(chunk)
            process.stdin.flush()

        # Close the process stdin to indicate that no more input will be provided
        process.stdin.close()

        # Get the output from the process stdout
        output_text = process.stdout.read()

        # Wait for the process to finish and get the return code
        return_code = process.wait()

        # Send the output as a response
        response = {'text': output_text}
        return jsonify(response)

        # Render the index template for GET requests
    return jsonify({"message": "Session initialized"})


@socketio.on('message')
def handle_message(message):
    # Handle SocketIO message events if needed
    pass


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)