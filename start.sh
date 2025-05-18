#!/bin/bash

# Start FastAPI in the background
uvicorn api:app --host 0.0.0.0 --port 80 &

# Start Streamlit (will keep the container running)
streamlit run app.py --server.port=8001 --server.address=0.0.0.0
