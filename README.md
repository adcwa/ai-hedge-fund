# AI Hedge Fund

This is a proof of concept for an AI-powered hedge fund.  The goal of this project is to explore the use of AI to make trading decisions.  This project is for **educational** purposes only and is not intended for real trading or investment.

This system employs several agents working together:

1. Ben Graham Agent - The godfather of value investing, only buys hidden gems with a margin of safety
2. Bill Ackman Agent - An activist investors, takes bold positions and pushes for change
3. Cathie Wood Agent - The queen of growth investing, believes in the power of innovation and disruption
4. Charlie Munger Agent - Warren Buffett's partner, only buys wonderful businesses at fair prices
5. Stanley Druckenmiller Agent - Macro trading legend who hunts for asymmetric opportunities with explosive growth potential
6. Warren Buffett Agent - The oracle of Omaha, seeks wonderful companies at a fair price
7. Valuation Agent - Calculates the intrinsic value of a stock and generates trading signals
8. Sentiment Agent - Analyzes market sentiment and generates trading signals
9. Fundamentals Agent - Analyzes fundamental data and generates trading signals
10. Technicals Agent - Analyzes technical indicators and generates trading signals
11. Risk Manager - Calculates risk metrics and sets position limits
12. Portfolio Manager - Makes final trading decisions and generates orders

<img width="1020" alt="Screenshot 2025-03-08 at 4 45 22 PM" src="https://github.com/user-attachments/assets/d8ab891e-a083-4fed-b514-ccc9322a3e57" />

**Note**: the system simulates trading decisions, it does not actually trade.

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No warranties or guarantees provided
- Past performance does not indicate future results
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions

By using this software, you agree to use it solely for learning purposes.

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
  - [Running the Hedge Fund](#running-the-hedge-fund)
  - [Running the Backtester](#running-the-backtester)
  - [Using the Web Interface](#using-the-web-interface)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Feature Requests](#feature-requests)
- [License](#license)
- [Deploying to Vercel](#deploying-to-vercel)

## Setup

Clone the repository:
```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Set up your environment variables:
```bash
# Create .env file for your API keys
cp .env.example .env
```

4. Set your API keys:
```bash
# For running LLMs hosted by openai (gpt-4o, gpt-4o-mini, etc.)
# Get your OpenAI API key from https://platform.openai.com/
OPENAI_API_KEY=your-openai-api-key

# For running LLMs hosted by groq (deepseek, llama3, etc.)
# Get your Groq API key from https://groq.com/
GROQ_API_KEY=your-groq-api-key

# For getting financial data to power the hedge fund
# Get your Financial Datasets API key from https://financialdatasets.ai/
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

**Important**: You must set `OPENAI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY`, or `DEEPSEEK_API_KEY` for the hedge fund to work.  If you want to use LLMs from all providers, you will need to set all API keys.

Financial data for AAPL, GOOGL, MSFT, NVDA, and TSLA is free and does not require an API key.

For any other ticker, you will need to set the `FINANCIAL_DATASETS_API_KEY` in the .env file.

## Usage

### Running the Hedge Fund
```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

**Example Output:**
<img width="992" alt="Screenshot 2025-01-06 at 5 50 17 PM" src="https://github.com/user-attachments/assets/e8ca04bf-9989-4a7d-a8b4-34e04666663b" />

You can also specify a `--show-reasoning` flag to print the reasoning of each agent to the console.

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --show-reasoning
```
You can optionally specify the start and end dates to make decisions for a specific time period.

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01 
```

### Running the Backtester

```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

**Example Output:**
<img width="941" alt="Screenshot 2025-01-06 at 5 47 52 PM" src="https://github.com/user-attachments/assets/00e794ea-8628-44e6-9a84-8f8a31ad3b47" />

You can optionally specify the start and end dates to backtest over a specific time period.

```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01
```

### Using the Web Interface

The AI Hedge Fund now includes a web interface with Apple-inspired UI styling for a more user-friendly experience.

To run the web interface:

```bash
# Install Flask if not already installed
poetry add flask

# Run the web application
poetry run python web/app.py
```

Then open your browser and navigate to http://localhost:5000

The web interface provides:
- Input for stock tickers
- Selection of AI analysts
- Choice of LLM models
- Real-time progress tracking
- Detailed results display with analyst signals, trading decisions, and reasoning

<img width="1000" alt="AI Hedge Fund Web Interface" src="https://github.com/user-attachments/assets/web-interface-screenshot.png" />

## Project Structure 
```
ai-hedge-fund/
├── src/
│   ├── agents/                   # Agent definitions and workflow
│   │   ├── bill_ackman.py        # Bill Ackman agent
│   │   ├── fundamentals.py       # Fundamental analysis agent
│   │   ├── portfolio_manager.py  # Portfolio management agent
│   │   ├── risk_manager.py       # Risk management agent
│   │   ├── sentiment.py          # Sentiment analysis agent
│   │   ├── technicals.py         # Technical analysis agent
│   │   ├── valuation.py          # Valuation analysis agent
│   │   ├── warren_buffett.py     # Warren Buffett agent
│   ├── tools/                    # Agent tools
│   │   ├── api.py                # API tools
│   ├── backtester.py             # Backtesting tools
│   ├── main.py                   # Main entry point
├── web/                          # Web interface
│   ├── app.py                    # Flask application
│   ├── static/                   # Static assets
│   │   ├── css/                  # CSS styles
│   │   ├── js/                   # JavaScript files
│   ├── templates/                # HTML templates
├── pyproject.toml
├── ...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

**Important**: Please keep your pull requests small and focused.  This will make it easier to review and merge.

## Feature Requests

If you have a feature request, please open an [issue](https://github.com/virattt/ai-hedge-fund/issues) and make sure it is tagged with `enhancement`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Deploying to Vercel

This application can be deployed to Vercel by following these steps:

### Prerequisites

1. A [Vercel account](https://vercel.com/signup)
2. [Vercel CLI](https://vercel.com/docs/cli) installed (optional for local testing)
3. API keys for the LLM providers you want to use (OpenAI, Anthropic, etc.)

### Deployment Steps

1. Fork or clone this repository to your GitHub account
2. Connect your GitHub repository to Vercel:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" > "Project"
   - Select your repository
   - Configure the project:
     - Framework Preset: Other
     - Root Directory: ./
     - Build Command: None
     - Output Directory: None
     - Install Command: pip install -r requirements.txt

3. Set up environment variables:
   - In the Vercel project settings, go to "Environment Variables"
   - Add all the required API keys from your `.env` file:
     - `OPENAI_API_KEY`
     - `ANTHROPIC_API_KEY`
     - `GROQ_API_KEY`
     - `GOOGLE_API_KEY`
     - `DEEPSEEK_API_KEY`
     - `FINANCIAL_DATASETS_API_KEY`

4. Deploy the application:
   - Click "Deploy"
   - Wait for the deployment to complete
   - Access your application at the provided URL

### Local Testing with Vercel

To test the deployment locally before pushing to production:

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel login` to authenticate
3. Run `vercel dev` to start a local development server
4. Access the application at http://localhost:3000

### Troubleshooting

- If you encounter memory issues during deployment, consider optimizing your dependencies or upgrading your Vercel plan
- For SSE (Server-Sent Events) functionality, ensure your Vercel function timeout is set to a higher value in the project settings
- Check Vercel logs for any deployment or runtime errors
