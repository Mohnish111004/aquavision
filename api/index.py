"""
Vercel Serverless Function Entry Point
This file handles all API requests for the deployed application
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the Flask app
from backend.app import app

# Vercel serverless function handler
def handler(event, context):
    """Handle incoming requests"""
    return app(event, context)

# For Vercel, we need to export the app
application = app
