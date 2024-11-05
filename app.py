from flask import Flask, render_template, request, redirect, url_for
import googlemaps
import google.generativeai as genai
import os

app = Flask(__name__)

# Set up Google Maps API
gmaps = googlemaps.Client(key='YOUR_GOOGLE_MAPS_API_KEY')  

# Configure the Gemini API
genai.configure(api_key="AIzaSyAd3KJ0mXHGb7MJ-a-vVci01OR-JEmx_tA")  

# Function to analyze quiz responses using Google Gemini
def analyze_quiz_with_gemini(answers):
    
    user_input = " ".join(answers)
    prompt = f"Based on the following answers to a health quiz: {user_input}, what would be your recommendation for further action?"

    # Generate a response from Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")  
    response = model.generate_content(prompt)

    return response.text

# Endpoint for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint for the Endometriosis quiz
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
        
        
        recommendation = analyze_quiz_with_gemini(answers)

        # Get user's location
        location = request.form['location']
        
        # Redirect to results page with the recommendation
        return redirect(url_for('result', location=location, recommendation=recommendation, condition="Endometriosis"))

    return render_template('endometriosis_quiz.html')

# Endpoint for the PCOS quiz
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
        
        # Analyze answers using Google Gemini
        recommendation = analyze_quiz_with_gemini(answers)

        # Get user's location
        location = request.form['location']
        
        # Redirect to results page with the recommendation
        return redirect(url_for('result', location=location, recommendation=recommendation, condition="PCOS"))

    return render_template('pcos_quiz.html')

# Endpoint for the Breast Self-Exam quiz
@app.route('/breast-exam', methods=['GET', 'POST'])
def breast_exam():
    if request.method == 'POST':
        # Get responses from the BSE quiz
        abnormalities = [
            request.form.get("lump"),
            request.form.get("pain"),
            request.form.get("skin_change"),
            request.form.get("discharge"),
        ]
        
        # Analyze the quiz answers using Google Gemini
        recommendation = analyze_quiz_with_gemini(abnormalities)

        # Get user's location
        location = request.form['location']
        
        # Redirect to results page with the recommendation
        return redirect(url_for('result', location=location, recommendation=recommendation, condition="Breast Health"))

    return render_template('breast_exam.html')

# Endpoint for displaying the result and healthcare provider recommendations
@app.route('/result')
def result():
    location = request.args.get('location')
    recommendation = request.args.get('recommendation')
    condition = request.args.get('condition')
    
    # Get the nearest healthcare providers using Google Maps API
    providers = find_nearby_providers(location)

    return render_template('result.html', location=location, providers=providers, recommendation=recommendation, condition=condition)

# Function to find nearby healthcare providers using Google Maps API
def find_nearby_providers(location):
    # Use Google Maps Geocoding API to get the coordinates of the location
    geocode_result = gmaps.geocode(location)
    if geocode_result:
        # Get the latitude and longitude of the location
        lat, lng = geocode_result[0]['geometry']['location'].values()
        # Search for nearby healthcare providers (e.g., hospitals)
        places_result = gmaps.places_nearby((lat, lng), radius=5000, type='hospital')
        
        # Return the names of nearby providers (simplified)
        return [place['name'] for place in places_result.get('results', [])]
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True)
