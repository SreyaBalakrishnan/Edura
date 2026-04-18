#!/bin/bash
# Test the summarization service

echo "Testing Summarization Service"
echo "=============================="
echo ""

# Test health check
echo "1. Testing health check..."
curl -X GET http://localhost:5000/health
echo ""
echo ""

# Test summarize-bullets endpoint
echo "2. Testing summarize-bullets endpoint..."
curl -X POST http://localhost:5000/summarize-bullets \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning is a subset of artificial intelligence that focuses on the ability of computers to learn and improve from experience without being explicitly programmed. Machine learning algorithms use computational methods to learn information directly from data without relying on predetermined equations as models. The algorithms iteratively make predictions and get corrected, allowing them to learn over time. Deep learning is part of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised, or unsupervised.",
    "num_bullets": 3
  }'
echo ""
echo ""

# Test summarize endpoint
echo "3. Testing summarize endpoint..."
curl -X POST http://localhost:5000/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms including object-oriented, functional, and procedural programming. Python has become increasingly popular in data science, artificial intelligence, and web development. Its extensive standard library and third-party packages make it suitable for a wide range of applications.",
    "max_length": 100,
    "min_length": 50
  }'
echo ""
echo ""

echo "Test completed!"
