from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Flask, Response, request
import random
import time


app = Flask(__name__)

# Create a Counter metric to track the total number of requests
REQUEST_COUNT = Counter('app_requests_total',
                        'Total number of requests to this app')

# Create a Histogram metric to track request duration
REQUEST_DURATION = Histogram(
    'app_request_duration_seconds', 'Duration of requests to this app')


@app.before_request
def before_request():
    request.start_time = time.time()
    REQUEST_COUNT.inc()


@app.after_request
def after_request(response):
    request_duration = time.time() - request.start_time
    REQUEST_DURATION.observe(request_duration)
    return response


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route('/fast')
def fast():
    return "This is a fast response!"


@app.route('/slow')
def slow():
    time.sleep(2)
    return "This is a slow response!"


@app.route('/error')
def error():
    if random.random() < 0.5:
        return "This request was successful!", 200
    else:
        return "This request resulted in an error!", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
