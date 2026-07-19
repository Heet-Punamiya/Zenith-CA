def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [b'{"status": "online", "message": "Zenith CA backend is running successfully. Streamlit UI must be run locally."}']
