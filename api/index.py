"""
Vercel Serverless Function - Minimal Test
"""

def handler(request, context):
    """Simple handler for testing"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": '{"message": "Hello from Python!", "success": true}'
    }
