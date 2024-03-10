# app.py
import logging
from flask import Flask, request, jsonify, send_file
from model import adjust_question_distribution
import performancePlot as pp

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        logging.debug(f"Received prediction request data: {data}")

        adjusted_questions = adjust_question_distribution(data)
        logging.debug(f"Processed prediction. Adjusted questions: {adjusted_questions}")

        response = jsonify(adjusted_questions)
        logging.debug(f"Sending response: {response.get_data(as_text=True)}")
        return response
    except Exception as e:
        logging.error(f"Error processing prediction request: {str(e)}")
        return jsonify({"error": "Error processing request"}), 500



@app.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json()
    pp.generate_performance_report(data)
    return send_file("performance_report.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
