from flask import Flask, request, jsonify
import openai
from models import db, QuestionAnswer
from db import init_db
from dotenv import load_dotenv
import os

#Load environment variables from the .env file into the application.
load_dotenv()

# Create a Flask application instance.
app = Flask(__name__)

# Set up the database URI for PostgreSQL, retrieving credentials from environment variables.
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"

# Disable modification tracking for SQLAlchemy to reduce overhead.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
init_db(app)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
            max_tokens=100
        )
        answer = response['choices'][0]['message']['content'].strip()

        qa = QuestionAnswer(question=question, answer=answer)
        db.session.add(qa)
        db.session.commit()

        return jsonify({"question": question, "answer": answer}), 200

# Handle the rate limit error from OpenAI's
    except openai.error.RateLimitError:
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)