from flask import Flask, request
from calls import generate_output
from processor import process_request
app = Flask(__name__)

@app.route("/process", methods=['POST'])
def process():
    prompt = request.json['prompt']
    processed_data = process_request(prompt)
    return {'processed_data': processed_data}

app.run(debug=True)

# if __name__ == "__main__":
#     app.run(debug=True)