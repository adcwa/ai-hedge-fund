import { getAssetFromKV } from '@cloudflare/kv-asset-handler'

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event))
})

/**
 * Handle incoming requests to the worker
 * @param {FetchEvent} event
 */
async function handleRequest(event) {
  const request = event.request
  try {
    const url = new URL(request.url)
    
    // Serve static files directly from the bucket
    if (url.pathname.startsWith('/static/')) {
      return await getAssetFromKV(event)
    }
    
    // For all other requests, pass to the Flask app
    // Extract request data to pass to the Flask app
    const method = request.method
    const path = url.pathname
    const headers = Object.fromEntries(request.headers.entries())
    
    // Get the request body if it exists
    let body = ''
    if (method !== 'GET' && method !== 'HEAD') {
      body = await request.text()
    }
    
    // Create the request object for the Flask app
    const flaskRequest = {
      method,
      path,
      headers,
      body
    }
    
    // Store the request in KV for debugging if needed
    await AI_HEDGE_FUND_KV.put(`request_${Date.now()}`, JSON.stringify(flaskRequest))
    
    // In a real implementation, you would call your Flask app here
    // For now, we'll return a mock response
    const mockResponse = {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: 'This is a mock response from Cloudflare Workers',
        request: flaskRequest
      })
    }
    
    // Create a response from the Flask app response
    const responseInit = {
      status: mockResponse.status,
      headers: mockResponse.headers
    }
    
    return new Response(mockResponse.body, responseInit)
  } catch (error) {
    return new Response(`Error: ${error.message}`, { status: 500 })
  }
} 