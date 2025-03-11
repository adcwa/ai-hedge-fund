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

# 创建一个全局的进度队列
progress_queues = {}

# 自定义进度监听器
class ProgressListener:
    def __init__(self, queue_id):
        self.queue = queue.Queue()
        progress_queues[queue_id] = self.queue
        
    def on_update(self, agent, ticker, status, message=None):
        # 将进度更新放入队列
        self.queue.put({
            'agent': agent,
            'ticker': ticker,
            'status': status,
            'message': message
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

@app.route('/api/progress/<queue_id>')
def get_progress(queue_id):
    """SSE endpoint for progress updates"""
    if queue_id not in progress_queues:
        return "Queue not found", 404
    
    def generate():
        q = progress_queues[queue_id]
        try:
            while True:
                # 非阻塞方式获取队列中的更新
                try:
                    update = q.get(block=False)
                    yield f"data: {json.dumps(update)}\n\n"
                except queue.Empty:
                    # 如果队列为空，等待一小段时间再试
                    time.sleep(0.1)
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
        except GeneratorExit:
            # 客户端断开连接时清理
            if queue_id in progress_queues:
                del progress_queues[queue_id]
    
    return Response(stream_with_context(generate()), 
                   mimetype='text/event-stream',
                   headers={'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive'})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Run the hedge fund analysis"""
    data = request.json
    
    # Extract parameters from the request
    tickers = [ticker.strip() for ticker in data.get('tickers', '').split(',')]
    selected_analysts = data.get('analysts', [])
    model_name = data.get('model', 'gpt-4o')
    model_provider = data.get('provider', 'OpenAI')
    
    # 创建唯一的队列ID
    queue_id = f"{int(time.time())}-{hash(str(tickers) + str(selected_analysts))}"
    
    # 创建进度监听器
    progress_listener = ProgressListener(queue_id)
    
    # 设置进度回调
    progress.set_callback(progress_listener.on_update)
    
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
    
    # 返回队列ID，前端将使用它来连接SSE
    response = {
        "success": True, 
        "queue_id": queue_id,
        "message": "分析已开始，请通过SSE连接获取实时进度"
    }
    
    # 在后台线程中运行分析
    def run_analysis():
        try:
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
            
            # 分析完成后，发送完成消息
            progress_queues[queue_id].put({
                'type': 'complete',
                'result': result
            })
            
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"Error in analyze: {str(e)}\n{error_traceback}")
            
            # 发送错误消息
            if queue_id in progress_queues:
                progress_queues[queue_id].put({
                    'type': 'error',
                    'error': str(e)
                })
    
    # 启动后台线程
    threading.Thread(target=run_analysis).start()
    
    return jsonify(response)

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