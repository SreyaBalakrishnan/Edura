from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS
import os
import logging

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the summarization pipeline
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    logger.info("Summarization model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    summarizer = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Text Summarization Service'
    }), 200

@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Summarize text endpoint
    
    Expected JSON:
    {
        "text": "text to summarize",
        "max_length": 150,
        "min_length": 50
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text'
            }), 400
        
        text = data.get('text', '').strip()
        max_length = data.get('max_length', 150)
        min_length = data.get('min_length', 50)
        
        if not text:
            return jsonify({
                'error': 'Text cannot be empty'
            }), 400
        
        if len(text.split()) < 20:
            return jsonify({
                'summary': text,
                'message': 'Text too short to summarize'
            }), 200
        
        if summarizer is None:
            return jsonify({
                'error': 'Summarization model not loaded'
            }), 500
        
        # Generate summary
        summary_result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        summary_text = summary_result[0]['summary_text']
        
        return jsonify({
            'success': True,
            'summary': summary_text,
            'original_length': len(text.split()),
            'summary_length': len(summary_text.split())
        }), 200
    
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return jsonify({
            'error': f'Summarization failed: {str(e)}'
        }), 500

@app.route('/summarize-bullets', methods=['POST'])
def summarize_bullets():
    """
    Summarize text and return as bullet points
    
    Expected JSON:
    {
        "text": "text to summarize",
        "num_bullets": 5
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text'
            }), 400
        
        text = data.get('text', '').strip()
        num_bullets = data.get('num_bullets', 5)
        
        if not text:
            return jsonify({
                'error': 'Text cannot be empty'
            }), 400
        
        if len(text.split()) < 20:
            return jsonify({
                'bullets': [text],
                'message': 'Text too short to summarize'
            }), 200
        
        if summarizer is None:
            return jsonify({
                'error': 'Summarization model not loaded'
            }), 500
        
        # Generate summary
        max_length = min(150, len(text.split()) // 2)
        min_length = min(50, len(text.split()) // 3)
        
        summary_result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        summary_text = summary_result[0]['summary_text']
        
        # Split into bullet points
        sentences = summary_text.split('. ')
        bullets = [s.strip() + '.' if not s.endswith('.') else s.strip() for s in sentences if s.strip()]
        
        # Limit to requested number
        bullets = bullets[:num_bullets]
        
        return jsonify({
            'success': True,
            'bullets': bullets,
            'count': len(bullets),
            'original_length': len(text.split()),
            'summary_length': len(summary_text.split())
        }), 200
    
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return jsonify({
            'error': f'Summarization failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
