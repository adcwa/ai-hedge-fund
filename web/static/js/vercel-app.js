// Vercel-specific JavaScript for the AI Hedge Fund web app

// Function to handle form submission for analysis
async function submitAnalysisForm(event) {
    event.preventDefault();
    
    // Show loading state
    document.getElementById('loading-indicator').style.display = 'flex';
    document.getElementById('results-container').style.display = 'none';
    document.getElementById('error-container').style.display = 'none';
    
    // Get form data
    const tickers = document.getElementById('tickers').value;
    const selectedAnalysts = Array.from(
        document.querySelectorAll('input[name="analysts"]:checked')
    ).map(el => el.value);
    const model = document.getElementById('model').value;
    const provider = document.getElementById('provider').value;
    
    try {
        // Send analysis request
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tickers,
                analysts: selectedAnalysts,
                model,
                provider
            }),
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'An unknown error occurred');
        }
        
        // For Vercel, we get the result directly in the response
        displayResults(data.result);
        
    } catch (error) {
        console.error('Error during analysis:', error);
        document.getElementById('error-message').textContent = error.message;
        document.getElementById('error-container').style.display = 'block';
    } finally {
        document.getElementById('loading-indicator').style.display = 'none';
    }
}

// Function to display results
function displayResults(result) {
    const resultsContainer = document.getElementById('results-container');
    
    // Clear previous results
    resultsContainer.innerHTML = '';
    
    if (!result || !result.portfolio) {
        resultsContainer.innerHTML = '<div class="alert alert-warning">No results available</div>';
        resultsContainer.style.display = 'block';
        return;
    }
    
    // Create portfolio summary
    const portfolioSummary = document.createElement('div');
    portfolioSummary.className = 'portfolio-summary';
    portfolioSummary.innerHTML = `
        <h3>Portfolio Summary</h3>
        <div class="summary-item">
            <span>Cash:</span>
            <span>$${window.appHelpers.formatNumber(result.portfolio.cash.toFixed(2))}</span>
        </div>
        <div class="summary-item">
            <span>Total Value:</span>
            <span>$${window.appHelpers.formatNumber(result.portfolio.total_value.toFixed(2))}</span>
        </div>
    `;
    
    // Create positions table
    const positionsTable = document.createElement('div');
    positionsTable.className = 'positions-table';
    
    let positionsHTML = `
        <h3>Positions</h3>
        <table>
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Shares</th>
                    <th>Entry Price</th>
                    <th>Current Price</th>
                    <th>P&L</th>
                    <th>Signal</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    // Add positions
    if (result.portfolio.positions && Object.keys(result.portfolio.positions).length > 0) {
        for (const [ticker, position] of Object.entries(result.portfolio.positions)) {
            const pnlPercent = position.unrealized_pnl_percent || 0;
            const pnlClass = pnlPercent >= 0 ? 'positive' : 'negative';
            const signalClass = window.appHelpers.getSignalClass(position.signal || 'NEUTRAL');
            
            positionsHTML += `
                <tr>
                    <td>${ticker}</td>
                    <td>${window.appHelpers.formatNumber(position.shares)}</td>
                    <td>$${position.entry_price.toFixed(2)}</td>
                    <td>$${position.current_price.toFixed(2)}</td>
                    <td class="${pnlClass}">${window.appHelpers.formatPercentage(pnlPercent)}</td>
                    <td class="signal ${signalClass}">${position.signal || 'NEUTRAL'}</td>
                </tr>
            `;
        }
    } else {
        positionsHTML += `
            <tr>
                <td colspan="6" class="no-data">No positions</td>
            </tr>
        `;
    }
    
    positionsHTML += `
            </tbody>
        </table>
    `;
    
    positionsTable.innerHTML = positionsHTML;
    
    // Add to results container
    resultsContainer.appendChild(portfolioSummary);
    resultsContainer.appendChild(positionsTable);
    
    // Show results
    resultsContainer.style.display = 'block';
}

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    const analysisForm = document.getElementById('analysis-form');
    if (analysisForm) {
        analysisForm.addEventListener('submit', submitAnalysisForm);
    }
}); 