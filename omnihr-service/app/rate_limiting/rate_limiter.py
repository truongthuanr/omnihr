# app/rate_limiting/rate_limiter.py
from fastapi import Request, HTTPException
from functools import wraps
import inspect

from app.servicelog.servicelog import logger

def rate_limited(rate_limiter):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            ip = request.client.host if request else "anonymous"
            logger.debug(f"[RateLimiter] Incoming request from IP: {ip}")

            if not rate_limiter.is_allowed(ip):
                logger.info(f"[RateLimiter] Rate limit exceeded for IP: {ip}")
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            logger.debug(f"[RateLimiter] Allowed IP: {ip}, proceeding to handler.")

            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper
    return decorator
