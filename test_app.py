import unittest
from flask import Flask
from flask_testing import TestCase
from app import app  
import os
from io import StringIO

class TestHerHealthApp(TestCase):
    
    def create_app(self):
        """Override this method to configure the app for testing"""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = os.urandom(24)  
        return app

    def test_home_page(self):
        """Test if the home page loads correctly"""
        response = self.client.get('/')
        self.assert200(response)  
        self.assertIn("Welcome to HerHealth", response.data.decode()) 

    def test_endometriosis_quiz(self):
        """Test the Endometriosis quiz page and submission"""
        response = self.client.get('/endometriosis')
        self.assert200(response)  
        
        # Simulate form submission for Endometriosis quiz
        form_data = {
            'pelvic pain': 'Yes',
            'painful periods': 'Yes',
            'heavy menstrual flow': 'Yes',
            'pain during intercourse': 'No',
            'difficulty getting pregnant': 'Yes'
        }
        response = self.client.post('/endometriosis', data=form_data)
       
        
        # Test that session data was correctly set and contains recommendations
        with self.client.session_transaction() as session:
            self.assertIn('recommendation', session)
            self.assertIn('condition', session)
            self.assertEqual(session['condition'], 'Endometriosis')

    def test_pcos_quiz(self):
        """Test the PCOS quiz page and submission"""
        response = self.client.get('/pcos')
        self.assert200(response)
        
        form_data = {
            'irregular periods': 'Yes',
            'difficulty losing weight': 'Yes',
            'excessive hair growth': 'Yes',
            'acne': 'Yes',
            'thinning hair': 'No'
        }
        response = self.client.post('/pcos', data=form_data)
          
        
        with self.client.session_transaction() as session:
            self.assertIn('recommendation', session)
            self.assertIn('condition', session)
            self.assertEqual(session['condition'], 'PCOS')

    def test_breast_exam_quiz(self):
        """Test the Breast Exam quiz page and submission"""
        response = self.client.get('/breast-exam')
        self.assert200(response)
        
        form_data = {
            'lump': 'Yes',
            'pain': 'No',
            'skin_change': 'No',
            'discharge': 'No'
        }
        response = self.client.post('/breast-exam', data=form_data)
       
        
        with self.client.session_transaction() as session:
            self.assertIn('recommendation', session)
            self.assertIn('condition', session)
            self.assertEqual(session['condition'], 'Breast Health')

    def test_result_page(self):
        """Test if the result page loads correctly with session data"""
        
        with self.client.session_transaction() as session:
            session['recommendation'] = "Consider visiting a doctor for further evaluation."
            session['condition'] = "Endometriosis"
            session['questions'] = ["Do you experience pelvic pain?", "Do you have painful periods?"]
            session['answers'] = ['Yes', 'Yes']
        
        response = self.client.get('/result')
        self.assert200(response) 
        self.assertIn("Endometriosis", response.data.decode())  
        self.assertIn("Consider visiting a doctor", response.data.decode())  

    def test_missing_session_data(self):
        """Test if missing session data results in an error message"""
        response = self.client.get('/result')
        self.assertEqual(response.data.decode(), "Error: Missing data, please complete the quiz again.")

if __name__ == '__main__':
    unittest.main()
