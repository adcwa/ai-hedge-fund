from app import app
from cloudflare_adapter import cloudflare_adapter

# Create the adapter function
handler = cloudflare_adapter(app)

def handle_request(request):
    """
    Entry point for Cloudflare Workers
    """
    return handler(request) 