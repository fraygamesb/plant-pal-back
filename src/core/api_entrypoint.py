import os
import sys
from argparse import ArgumentParser
from pathlib import Path

import uvicorn
from fastapi import FastAPI

if os.getenv(key="ENVIRONMENT", default="local") == "local":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.api.v1.endpoints.auth.register import router as user_router
from core.api.v1.endpoints.auth.login import router as user_login_router

app = FastAPI()

app.include_router(user_router)
app.include_router(user_login_router)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Enter host")
    parser.add_argument("--port", type=int, default=8000, help="Enter port")
    parser.add_argument("--reload", action="store_true", default=True)

    args = parser.parse_args()

    uvicorn.run(
        "core.api_entrypoint:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
