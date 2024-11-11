from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as genai
import os
from IPython.display import Markdown

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Gemini API
genai.configure(api_key="AIzaSyAd3KJ0mXHGb7MJ-a-vVci01OR-JEmx_tA")

# Define questions for each quiz
questions_endometriosis = [
    "Do you experience pelvic pain?",
    "Do you have painful periods?",
    "Do you have heavy menstrual flow?",
    "Do you experience pain during intercourse?",
    "Do you have difficulty getting pregnant?"
]

questions_pcos = [
    "Do you have irregular periods?",
    "Do you have difficulty losing weight?",
    "Do you experience excessive hair growth?",
    "Do you have acne?",
    "Do you experience thinning hair?"
]

questions_breast_exam = [
    "Do you notice any lumps in your breast?",
    "Do you feel any pain in your breast?",
    "Have you noticed any skin changes in your breast?",
    "Do you have any discharge from your nipple?"
]

# Function to analyze quiz responses using Google Gemini
def analyze_quiz_with_gemini(questions, answers):
    # Create a prompt that includes both the questions and answers
    prompt = "Based on the following answers to a health quiz, provide recommendations for further action:\n"
    for question, answer in zip(questions, answers):
        prompt += f"Question: {question} - Answer: {answer}\n"
    
    # Generate a response from Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/endometriosis', methods=['GET', 'POST'])
def endometriosis_quiz():
    if request.method == 'POST':
        # Get responses from the form
        answers = [
            request.form.get("pelvic pain"),
            request.form.get("painful periods"),
            request.form.get("heavy menstrual flow"),
            request.form.get("pain during intercourse"),
            request.form.get("difficulty getting pregnant")
        ]
        
        # Debug: Log answers to verify
        print(f"Endometriosis answers: {answers}")
        
        # Store the answers and questions in session
        session['answers'] = answers
        session['questions'] = questions_endometriosis
        # Analyze answers using Google Gemini
        recommendation = analyze_quiz_with_gemini(questions_endometriosis, answers)
        session['recommendation'] = recommendation
        session['condition'] = "Endometriosis"
        
        return redirect(url_for('result'))

    return render_template('endometriosis_quiz.html')

@app.route('/pcos', methods=['GET', 'POST'])
def pcos_quiz():
    if request.method == 'POST':
        # Get responses from the form
        answers = [
            request.form.get("irregular periods"),
            request.form.get("difficulty losing weight"),
            request.form.get("excessive hair growth"),
            request.form.get("acne"),
            request.form.get("thinning hair")
        ]
        
        # Debug: Log answers to verify
        print(f"PCOS answers: {answers}")
        
        # Store the answers and questions in session
        session['answers'] = answers
        session['questions'] = questions_pcos
        # Analyze answers using Google Gemini
        recommendation = analyze_quiz_with_gemini(questions_pcos, answers)
        session['recommendation'] = recommendation
        session['condition'] = "PCOS"
        
        return redirect(url_for('result'))

    return render_template('pcos_quiz.html')

@app.route('/breast-exam', methods=['GET', 'POST'])
def breast_exam():
    if request.method == 'POST':
        # Get responses from the BSE quiz
        answers = [
            request.form.get("lump"),
            request.form.get("pain"),
            request.form.get("skin_change"),
            request.form.get("discharge"),
        ]
        
        # Debug: Log answers to verify
        print(f"Breast exam answers: {answers}")
        
        # Store the answers and questions in session
        session['answers'] = answers
        session['questions'] = questions_breast_exam
        # Analyze the quiz answers using Google Gemini
        recommendation = analyze_quiz_with_gemini(questions_breast_exam, answers)
        session['recommendation'] = recommendation
        session['condition'] = "Breast Health"
        
        return redirect(url_for('result'))

    return render_template('breast_exam.html')

@app.route('/result')
def result():
    # Retrieve the recommendation, condition, questions, and answers from the session
    recommendation = session.get('recommendation')
    condition = session.get('condition')
    questions = session.get('questions')
    answers = session.get('answers')

    # Debug: Log session data to verify
    print(f"Session Data: recommendation={recommendation}, condition={condition}, questions={questions}, answers={answers}")
    
    # Ensure the data exists in session
    if not all([recommendation, condition, questions, answers]):
        return "Error: Missing data, please complete the quiz again."

    # Zip the questions with their corresponding answers
    quiz_data = list(zip(questions, answers))
    
    return render_template('result.html', 
                           recommendation=recommendation, 
                           condition=condition, 
                           quiz_data=quiz_data)

if __name__ == '__main__':
    app.run(debug=True)
