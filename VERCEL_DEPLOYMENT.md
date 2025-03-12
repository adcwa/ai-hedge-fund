# Deploying AI Hedge Fund to Vercel

This guide provides step-by-step instructions for deploying the AI Hedge Fund application to Vercel.

## Prerequisites

1. A [Vercel account](https://vercel.com/signup)
2. [Git](https://git-scm.com/downloads) installed on your local machine
3. API keys for the LLM providers you want to use (OpenAI, Anthropic, etc.)

## Deployment Steps

### 1. Prepare Your Repository

1. Fork or clone this repository to your GitHub account
2. Make sure your repository includes all the necessary files:
   - `vercel.json` - Configuration for Vercel deployment
   - `requirements.txt` - Python dependencies
   - `runtime.txt` - Python version specification
   - `.vercelignore` - Files to exclude from deployment

### 2. Connect to Vercel

1. Go to the [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" > "Project"
3. Select your GitHub repository
4. Configure the project:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: None
   - Output Directory: None
   - Install Command: pip install -r requirements.txt

### 3. Configure Environment Variables

In the Vercel project settings, go to "Environment Variables" and add the following:

- `OPENAI_API_KEY` - Your OpenAI API key
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `GROQ_API_KEY` - Your Groq API key
- `GOOGLE_API_KEY` - Your Google API key
- `DEEPSEEK_API_KEY` - Your DeepSeek API key
- `FINANCIAL_DATASETS_API_KEY` - Your Financial Datasets API key

### 4. Deploy

1. Click "Deploy"
2. Wait for the deployment to complete
3. Access your application at the provided URL

## Vercel Function Limitations

Vercel serverless functions have some limitations to be aware of:

1. **Execution Time**: Functions have a maximum execution time of 10 seconds on the Hobby plan (60 seconds on Pro plan)
2. **Memory**: Limited to 1GB on Hobby plan (4GB on Pro plan)
3. **Statelessness**: Functions are stateless, so they can't maintain state between invocations

For the AI Hedge Fund application, this means:

- Long-running analyses may time out
- Server-Sent Events (SSE) for real-time progress updates won't work as implemented in the local version
- You'll need to use a database or cache service for state persistence between function calls

## Optimizations for Vercel

The following optimizations have been made for Vercel deployment:

1. **Simplified Progress Tracking**: Using polling instead of SSE
2. **Synchronous Processing**: Running analyses synchronously instead of in background threads
3. **Reduced Dependencies**: Minimizing the number of dependencies to reduce cold start times

## Troubleshooting

### Function Timeouts

If you encounter function timeouts, consider:

1. Upgrading to a Vercel Pro plan for longer execution times
2. Breaking down the analysis into smaller chunks
3. Using a separate service for long-running tasks

### Cold Start Delays

Serverless functions can experience "cold starts" when they haven't been used recently:

1. Consider using a "warming" service to keep functions active
2. Optimize dependencies to reduce initialization time

### Memory Issues

If you encounter memory issues:

1. Reduce the number of dependencies
2. Optimize memory usage in your code
3. Upgrade to a plan with more memory

## Local Testing

To test the deployment locally before pushing to production:

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel login` to authenticate
3. Run `vercel dev` to start a local development server
4. Access the application at http://localhost:3000 