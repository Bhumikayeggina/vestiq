#!/bin/bash
# Starts the Vestiq web app on port 8501 (open http://localhost:8501 on the Windows laptop).
cd /home/hadoop/vestiq/app
/home/hadoop/.local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
