#!/usr/bin/env python
"""
Run script for the AI Hedge Fund web application.
This script provides a convenient way to start the web server.
"""

import os
import sys

# 添加当前目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app import app

if __name__ == '__main__':
    print("Starting AI Hedge Fund web application...")
    print("Open your browser and navigate to http://localhost:5000")
    app.run(debug=True, port=5000) 