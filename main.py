import os
import uvicorn
from loguru import logger
from fastapi import FastAPI
from importlib import import_module
from utils.rate_limit import limiter, _rate_limit_exceeded_handler, RateLimitExceeded

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def import_routers(directory: str, prefix: str = ""):
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isdir(full_path):
            version_prefix = f"{prefix}/{item}"
            import_routers(full_path, prefix=version_prefix)
        elif item == "route.py":
            module_path = directory.replace("/", ".") + ".route"
            module = import_module(module_path)
            router = getattr(module, "router")
            app.include_router(router, prefix=prefix)
            for route in router.routes:
                logger.info(f"Loaded endpoint: {prefix}{route.path}")

import_routers("routes")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
