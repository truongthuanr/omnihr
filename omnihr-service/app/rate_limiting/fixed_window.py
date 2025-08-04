# app/rate_limiting/fixed_window.py
import time
from threading import Lock
from collections import defaultdict

from app.rate_limiting.base import RateLimitStrategy
from app.servicelog.servicelog import logger
from app.config.config import Config

class FixedWindowLimiter(RateLimitStrategy):
    def __init__(self):
        self.config = Config()
        self.counters = defaultdict(lambda: [0, 0.0])  # {ip: [count, window_start]}
        self.global_counter = [0, 0.0]                 # [count, window_start]
        self.lock = Lock()
        logger.info(f"[Limiter Init] FixedWindowLimiter")

    def is_allowed(self, identifier: str) -> bool:
        cfg = self.config.get_rate_limit_config()
        max_requests = cfg["max_requests"]
        window = cfg["window_seconds"]
        max_global_requests = cfg["max_global_requests"]
        logger.info(
            f"[Limiter Config] Get Limiter configuration from file: (max_requests={max_requests}, "
            f"window={window}, max_global_requests={max_global_requests})"
        )
        now = time.time()
        with self.lock:
            # Cleanup: remove IPs inactive for more than 2 window durations
            stale_ips = [
                ip for ip, (_, start) in self.counters.items()
                if now - start >= window * 2
            ]
            for ip in stale_ips:
                del self.counters[ip]
                logger.debug(f"[Cleanup] Removed stale IP: {ip}")

            # Global limit
            g_count, g_start = self.global_counter
            # If window expired: reset global counter
            if now - g_start >= window:
                self.global_counter = [1, now]
                logger.info("[Global] Reset window.")
            # If global request count exceeds limit: reject request
            elif max_global_requests is not None and g_count >= max_global_requests:
                logger.info(f"[BLOCKED - GLOBAL] IP={identifier} | count={g_count}/{max_global_requests}")
                return False
            # Otherwise: increment global counter
            else:
                self.global_counter[0] += 1
                logger.debug(f"[Global] Incremented: {self.global_counter[0]}")

            # Per-IP limit
            count, start = self.counters[identifier]

            # If window expired: reset per-IP counter
            if now - start >= window:
                self.counters[identifier] = [1, now]
                logger.info(f"[IP] Reset window: {identifier}")
                return True
            # If per-IP request count is within limit: allow and increment
            elif count < max_requests:
                self.counters[identifier][0] += 1
                logger.debug(f"[IP] {identifier}: count={self.counters[identifier][0]}/{max_requests}")
                return True

            # Otherwise: reject
            logger.info(f"[BLOCKED - IP] {identifier}: count={count}/{max_requests}")
            return False

