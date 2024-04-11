import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

if ENVIRONMENT == "local":
    from .local import *  # NOQA: F401 F403
