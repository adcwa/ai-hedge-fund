import os
import sys
import json
import time
import threading
import queue
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from src
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
# 添加 src 目录到 Python 路径，这样 agents 模块就可以被找到
sys.path.append(os.path.join(parent_dir, 'src'))

# Import the necessary modules from the existing codebase
from src.utils.analysts import ANALYST_CONFIG
from src.llm.models import AVAILABLE_MODELS
from src.main import run_hedge_fund
from src.utils.progress import progress

# Load environment variables
load_dotenv()

# For Vercel serverless environment, we'll use a simpler approach
# instead of global queues which won't work well in serverless
class VercelProgressListener:
    def __init__(self):
        self.updates = []
        
    def on_update(self, agent, ticker, status, message=None):
        # Store updates in a list
        self.updates.append({
            'agent': agent,
            'ticker': ticker,
            'status': status,
            'message': message,
            'timestamp': time.time()
        })

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
    """Render the main page"""
    # Get analysts and models for the UI
    analysts = [{"id": key, "name": config["display_name"]} 
                for key, config in ANALYST_CONFIG.items()]
    
    models = [{"id": model.model_name, 
               "name": model.display_name,
               "provider": model.provider.value} 
              for model in AVAILABLE_MODELS]
    
    return render_template('index.html', analysts=analysts, models=models)

@app.route('/api/progress/<session_id>')
def get_progress(session_id):
    """Get progress updates for a session"""
    # In a serverless environment, we'll use a polling approach
    # This endpoint will return the latest updates since the last poll
    
    # In a real implementation, you would store progress in a database
    # or cache service like Redis that persists between function invocations
    
    # For demo purposes, we'll return a mock response
    return jsonify({
        "status": "running",
        "updates": [
            {"agent": "Portfolio Manager", "ticker": "AAPL", "status": "analyzing", "message": "Analyzing Apple Inc."}
        ]
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Run the hedge fund analysis"""
    data = request.json
    
    # Extract parameters from the request
    tickers = [ticker.strip() for ticker in data.get('tickers', '').split(',')]
    selected_analysts = data.get('analysts', [])
    model_name = data.get('model', 'gpt-4o')
    model_provider = data.get('provider', 'OpenAI')
    
    # Create a unique session ID
    session_id = f"{int(time.time())}-{hash(str(tickers) + str(selected_analysts))}"
    
    # Create progress listener
    progress_listener = VercelProgressListener()
    
    # Set progress callback
    progress.set_callback(progress_listener.on_update)
    
    # Default portfolio with initial cash
    portfolio = {
        "cash": 100000.0,
        "margin_requirement": 0.0,
        "positions": {}
    }
    
    # Get current date as end date
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime("%Y-%m-%d")
    # Default start date is 3 months ago
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    # For Vercel serverless, we'll run the analysis synchronously
    # This is not ideal for long-running tasks, but it's a starting point
    try:
        # For demo purposes, we'll run a simplified version
        # In production, you would use a task queue or database to track progress
        result = run_hedge_fund(
            tickers=tickers,
            start_date=start_date,
            end_date=end_date,
            portfolio=portfolio,
            show_reasoning=True,
            selected_analysts=selected_analysts,
            model_name=model_name,
            model_provider=model_provider
        )
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "result": result
        })
        
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in analyze: {str(e)}\n{error_traceback}")
        
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/analysts')
def get_analysts():
    """Get the list of available analysts"""
    analysts = [{"id": key, "name": config["display_name"]} 
                for key, config in ANALYST_CONFIG.items()]
    return jsonify(analysts)

@app.route('/api/models')
def get_models():
    """Get the list of available models"""
    models = [{"id": model.model_name, 
               "name": model.display_name,
               "provider": model.provider.value} 
              for model in AVAILABLE_MODELS]
    return jsonify(models)

# For Vercel serverless deployment
app.debug = False

# Export the Flask app for Vercel
index = app 