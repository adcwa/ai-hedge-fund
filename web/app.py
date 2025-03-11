import os
import sys
import json
from flask import Flask, render_template, request, jsonify
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

# Load environment variables
load_dotenv()

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

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Run the hedge fund analysis"""
    data = request.json
    
    # Extract parameters from the request
    tickers = [ticker.strip() for ticker in data.get('tickers', '').split(',')]
    selected_analysts = data.get('analysts', [])
    model_name = data.get('model', 'gpt-4o')
    model_provider = data.get('provider', 'OpenAI')
    
    # Default portfolio with initial cash
    portfolio = {
        "cash": 100000.0,
        "margin_requirement": 0.0,
        "positions": {}
    }
    
    # 获取当前日期作为结束日期
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime("%Y-%m-%d")
    # 默认开始日期为 3 个月前
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    # Run the hedge fund analysis
    try:
        result = run_hedge_fund(
            tickers=tickers,
            start_date=start_date,  # 使用字符串格式的日期，而不是 None
            end_date=end_date,      # 使用字符串格式的日期，而不是 None
            portfolio=portfolio,
            show_reasoning=True,
            selected_analysts=selected_analysts,
            model_name=model_name,
            model_provider=model_provider
        )
        
        return jsonify({"success": True, "result": result})
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in analyze: {str(e)}\n{error_traceback}")
        return jsonify({"success": False, "error": str(e)})

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

if __name__ == '__main__':
    app.run(debug=True, port=5000) 