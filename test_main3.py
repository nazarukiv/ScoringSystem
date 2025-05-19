import threading
import time
import random
import pytest

NUM_USERS = 500
NUM_REQUESTS = 20
DELAY_RANGE = (0.05, 0.2)

def query_system(user_id):

    time.sleep(random.uniform(*DELAY_RANGE))
    return f"User {user_id} received response"


def simulate_user(user_id, results):

    for _ in range(NUM_REQUESTS):
        response = query_system(user_id)
        results.append(response)


def test_run_stress_test():
    threads = []
    results = []
    start_time = time.time()

    for user_id in range(NUM_USERS):
        thread = threading.Thread(target=simulate_user, args=(user_id, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Stress test completed in {total_time:.2f} seconds")

    assert total_time < 30, "System response time exceeded acceptable limits!"


# run the stress test
if __name__ == "__main__":
    test_run_stress_test()