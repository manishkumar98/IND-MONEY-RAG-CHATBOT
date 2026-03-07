#!/bin/bash

# Start FastAPI in background
echo "🚀 Starting FastAPI Backend..."
python3 src/api/api.py &
API_PID=$!

# Wait for API to warm up
sleep 5

# Start Streamlit
echo "🎨 Starting Streamlit Frontend..."
python3 -m streamlit run src/ui/main_app.py --server.port 8501

# When Streamlit stops, kill the API
kill $API_PID
