# AI Hedge Fund Web Application

This is a web-based interface for the AI Hedge Fund system, providing a user-friendly way to interact with the AI-powered stock analysis and trading decision engine.

## Features

- Input stock tickers for analysis
- Select AI analysts to perform the analysis
- Choose from various LLM models
- Real-time progress tracking of the analysis process
- Beautiful Apple-inspired UI design
- Detailed results display with analyst signals, trading decisions, and portfolio summary

## Setup

1. Make sure you have set up the main AI Hedge Fund system and installed all dependencies
2. Navigate to the web directory
3. Run the Flask application:

```bash
cd web
python app.py
```

4. Open your browser and go to http://localhost:5000

## Requirements

- All the requirements from the main AI Hedge Fund system
- Flask

## Usage

1. Enter comma-separated stock ticker symbols (e.g., AAPL,MSFT,NVDA)
2. Select one or more AI analysts to perform the analysis
3. Choose an LLM model from the dropdown
4. Click "Analyze Stocks" to start the analysis
5. Watch the real-time progress as the analysis is performed
6. View the detailed results, including analyst signals, trading decisions, and reasoning

## API Endpoints

- `GET /`: Main web interface
- `GET /api/analysts`: Get the list of available analysts
- `GET /api/models`: Get the list of available LLM models
- `POST /api/analyze`: Run the hedge fund analysis with the provided parameters

## License

Same as the main AI Hedge Fund system. 