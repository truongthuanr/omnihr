# app/rate_limiting/fixed_window.py
import time
from threading import Lock
from collections import defaultdict

from app.rate_limiting.base import RateLimitStrategy
from app.servicelog.servicelog import logger

class FixedWindowLimiter(RateLimitStrategy):
    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
        max_global_requests: int = None  # Ignore if not set
    ):
        self.max_requests = max_requests
        self.window = window_seconds
        self.max_global_requests = max_global_requests

        self.counters = defaultdict(lambda: [0, 0.0])  # {ip: [count, window_start]}
        self.global_counter = [0, 0.0]                 # [count, window_start]
        self.lock = Lock()
        logger.info(
            f"[Limiter Init] FixedWindowLimiter(max_requests={max_requests}, "
            f"window={window_seconds}s, max_global_requests={max_global_requests})"
        )

    def is_allowed(self, identifier: str) -> bool:
        now = time.time()
        with self.lock:
            # Cleanup: remove IPs inactive for more than 2 window durations
            stale_ips = [
                ip for ip, (_, start) in self.counters.items()
                if now - start >= self.window * 2
            ]
            for ip in stale_ips:
                del self.counters[ip]
                logger.debug(f"[Cleanup] Removed stale IP: {ip}")

            # Global limit
            g_count, g_start = self.global_counter
            # If window expired: reset global counter
            if now - g_start >= self.window:
                self.global_counter = [1, now]
                logger.info("[Global] Reset window.")
            # If global request count exceeds limit: reject request
            elif self.max_global_requests is not None and g_count >= self.max_global_requests:
                logger.info(f"[BLOCKED - GLOBAL] IP={identifier} | count={g_count}/{self.max_global_requests}")
                return False
            # Otherwise: increment global counter
            else:
                self.global_counter[0] += 1
                logger.debug(f"[Global] Incremented: {self.global_counter[0]}")

            # Per-IP limit
            count, start = self.counters[identifier]

            # If window expired: reset per-IP counter
            if now - start >= self.window:
                self.counters[identifier] = [1, now]
                logger.info(f"[IP] Reset window: {identifier}")
                return True
            # If per-IP request count is within limit: allow and increment
            elif count < self.max_requests:
                self.counters[identifier][0] += 1
                logger.debug(f"[IP] {identifier}: count={self.counters[identifier][0]}/{self.max_requests}")
                return True

            # Otherwise: reject
            logger.info(f"[BLOCKED - IP] {identifier}: count={count}/{self.max_requests}")
            return False

