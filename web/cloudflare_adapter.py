from flask import Flask, request
import json

def cloudflare_adapter(app: Flask):
    """
    Adapter to make Flask work with Cloudflare Workers
    """
    def handle_request(request_data):
        # Parse the request data
        method = request_data.get('method', 'GET')
        path = request_data.get('path', '/')
        headers = request_data.get('headers', {})
        body = request_data.get('body', '')
        
        # Create a Flask request context
        with app.test_request_context(
            path=path,
            method=method,
            headers=headers,
            data=body
        ):
            # Process the request with Flask
            response = app.full_dispatch_request()
            
            # Return the response in a format Cloudflare Workers can understand
            return {
                'status': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
    
    return handle_request 