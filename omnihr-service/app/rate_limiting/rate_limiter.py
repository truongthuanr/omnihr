# app/rate_limiting/rate_limiter.py
from fastapi import Request, HTTPException
from functools import wraps
import inspect

def rate_limited(rate_limiter):
    # func: router handler function
    def decorator(func):
        @wraps(func)
        # *args, **kwargs: wrap from router handler function.
        async def wrapper(*args, **kwargs):
            # Get request param from router kwargs
            request: Request = kwargs.get("request")
            if not request:
                # if not found request from kwargs, find from arg
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            # get host ip from request
            ip = request.client.host if request else "anonymous"
            
            # Handle both sync and async functions
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper
    return decorator
