# Text Summarization Service Setup Guide

This guide explains how to set up and run the Python-based text summarization service for your College Connect Flutter app.

## Overview

The app now uses a Python backend service with the **BART (Facebook's Bidirectional and Auto-Regressive Transformers)** model for high-quality text summarization instead of Dart-based summarization.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- CUDA compatible GPU (optional but recommended for faster summarization)

## Installation Steps

### 1. Install Python Dependencies

Navigate to the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- **Flask**: Web framework for the API
- **transformers**: Hugging Face transformers library with pre-trained models
- **torch**: PyTorch deep learning framework
- **requests**: HTTP library
- **python-dotenv**: Environment variable management

### 2. Download the Model

The first time you run the service, it will automatically download the BART model (~1.6GB). This may take a few minutes depending on your internet speed.

## Running the Service

### Option 1: Command Line

```bash
python summarization_service.py
```

The service will start on `http://localhost:5000`

### Option 2: Using a Process Manager (Recommended for Production)

Install gunicorn:
```bash
pip install gunicorn
```

Run the service:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 summarization_service.py:app
```

## API Endpoints

### 1. Health Check
```
GET /health
```
Response:
```json
{
  "status": "healthy",
  "service": "Text Summarization Service"
}
```

### 2. Summarize Text
```
POST /summarize
Content-Type: application/json

{
  "text": "Your text to summarize here...",
  "max_length": 150,
  "min_length": 50
}
```

Response:
```json
{
  "success": true,
  "summary": "Summarized text here...",
  "original_length": 500,
  "summary_length": 50
}
```

### 3. Summarize as Bullet Points
```
POST /summarize-bullets
Content-Type: application/json

{
  "text": "Your text to summarize here...",
  "num_bullets": 5
}
```

Response:
```json
{
  "success": true,
  "bullets": [
    "First key point.",
    "Second key point.",
    "Third key point."
  ],
  "count": 3,
  "original_length": 500,
  "summary_length": 50
}
```

## Configuration

### Adjusting Summarization Parameters

Edit `summarization_service.py` to modify default parameters:

```python
# In the summarize endpoint
max_length = data.get('max_length', 150)  # Maximum summary length
min_length = data.get('min_length', 50)   # Minimum summary length
```

### Using Different Models

You can use other Hugging Face summarization models by changing the model name:

```python
# In line: summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Other options:
# - "google/pegasus-arxiv"
# - "facebook/bart-base"
# - "t5-base"
# - "sshleifer/distilbart-cnn-6-6"
```

## Connecting Flutter App to Service

### Local Development

The Flutter app expects the service at `http://localhost:5000`

### Remote Server

To use a remote server, you can modify the URL in `view_materials.dart`:

```dart
// Change this line in _generateSummaryFromPython()
final Uri summaryUrl = Uri.parse('http://your-server-ip:5000/summarize-bullets');
```

## Troubleshooting

### Service Won't Start
- **Issue**: Module not found errors
  - **Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

### Model Download Fails
- **Issue**: Can't download model (network timeout)
  - **Solution**: Download the model manually or increase timeout: `pip install transformers[torch]`

### Slow Summarization
- **Issue**: Summarization takes too long
  - **Solution**: Use a GPU if available, or switch to a faster model like `distilbart`

### Connection Refused from Flutter
- **Issue**: Flutter app can't connect to service
  - **Solution**: 
    - Make sure service is running
    - Check if localhost:5000 is accessible
    - For Android emulator, use `10.0.2.2` instead of `localhost`

### Out of Memory Errors
- **Issue**: Python process uses too much memory
  - **Solution**: Use a smaller model or reduce batch size

## Performance Tips

1. **Use GPU**: Install CUDA and cuDNN for faster summarization
2. **Cache Results**: Consider caching summaries in the app
3. **Batch Processing**: Send multiple texts together for efficiency
4. **Model Selection**: Use `distilbart` for faster but slightly less accurate results

## Model Comparison

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| facebook/bart-large-cnn | 1.6GB | Slow | Very High | High-quality academic content |
| facebook/bart-base | 500MB | Medium | High | General purpose |
| google/pegasus-arxiv | 600MB | Medium | High | Research papers |
| sshleifer/distilbart-cnn-6-6 | 300MB | Fast | Good | Quick summaries |

## Stop the Service

Press `Ctrl+C` in the terminal where the service is running.

## Security Notes

- The current implementation listens on all interfaces (`0.0.0.0`)
- For production, consider:
  - Running behind a reverse proxy (Nginx)
  - Adding API authentication
  - Rate limiting requests
  - Using HTTPS

## Next Steps

1. Ensure Python 3.8+ is installed
2. Run `pip install -r requirements.txt`
3. Run `python summarization_service.py`
4. Test the service at `http://localhost:5000/health`
5. Run your Flutter app and test the summarization feature

Enjoy improved text summarization powered by state-of-the-art AI models!
