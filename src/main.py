import os
from collections import defaultdict

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import geopandas as gpd

from deps import FramesOfObjectsDepsMarker
from routes import router_object


def register_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    frames_of_objects = defaultdict(gpd.GeoDataFrame)

    app.dependency_overrides.update(  # type: ignore
        {
            FramesOfObjectsDepsMarker: lambda: frames_of_objects,
        }
    )

    app.include_router(router_object)

    return app


def main() -> None:
    app = register_app()

    uvicorn.run(
        app,
        host=os.getenv("SERVER_HOST", default="127.0.0.1"),
        port=int(os.getenv("SERVER_PORT", default="8197")),
    )


if __name__ == "__main__":
    main()
