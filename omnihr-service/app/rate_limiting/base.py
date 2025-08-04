# app/rate_limiting/base.py
class RateLimitStrategy:
    def is_allowed(self, identifier: str) -> bool:
        raise NotImplementedError
