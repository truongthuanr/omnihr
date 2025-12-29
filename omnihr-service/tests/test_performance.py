import time

import pytest
import requests

# Point to the running service (container/host)
BASE_URL = "http://localhost:8000"
# Org key required by the API
ORG_KEY = "key-omnihr-001"

# Thresholds (ms) and run count
AVG_THRESHOLD_MS = 300.0
MAX_THRESHOLD_MS = 500.0
RUNS = 20


def test_employees_search_latency_under_threshold():
    url = f"{BASE_URL}/employees/search"
    headers = {"X-org-key": ORG_KEY}

    # Warm-up to avoid cold-start skew
    requests.get(url, headers=headers, timeout=5)

    latencies_ms = []
    filters = [
        {},  # no filter
        {"status_id": 1, "page": 1, "size": 10},
        {"department_id": 1, "page": 1, "size": 5},
        {"location_id": 2, "page": 2, "size": 5},
        {"company_id": 1, "position_id": 2, "page": 3, "size": 5},
    ]

    for i in range(RUNS):
        params = filters[i % len(filters)]
        start = time.perf_counter()
        response = requests.get(url, headers=headers, params=params, timeout=5)
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert response.status_code == 200
        latencies_ms.append(elapsed_ms)

    avg_ms = sum(latencies_ms) / len(latencies_ms)
    max_ms = max(latencies_ms)

    print(
        f"Latencies (ms): {[round(x, 2) for x in latencies_ms]} | "
        f"avg={avg_ms:.2f} | max={max_ms:.2f} | runs={RUNS}"
    )

    assert avg_ms < AVG_THRESHOLD_MS, f"Average latency too high: {avg_ms:.2f} ms"
    assert max_ms < MAX_THRESHOLD_MS, f"Slowest call exceeded limit: {max_ms:.2f} ms"
