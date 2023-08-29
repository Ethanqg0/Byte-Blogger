from flask import Flask, jsonify
import time

app = Flask(__name__)

def simulate_work():
    time.sleep(0.1)  # Simulate 0.1 seconds of work

@app.route('/test_caching')
def test_caching():
    # Test without caching
    start_time = time.time()
    simulate_work()
    first_test_time = time.time() - start_time

    # Test with caching
    total_time_with_caching = 0
    for _ in range(99):
        start_time = time.time()
        simulate_work()
        total_time_with_caching += time.time() - start_time

    average_time_with_caching = total_time_with_caching / 99

    caching_efficiency = first_test_time / average_time_with_caching

    result = {
        "first_test_time": first_test_time,
        "average_time_with_caching": average_time_with_caching,
        "caching_efficiency": caching_efficiency
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
