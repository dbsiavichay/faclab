import os

import environ

env = environ.Env()

DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"
# Config Minio
MINIO_STORAGE_ENDPOINT = env("MINIO_STORAGE_ENDPOINT", default="localhost:9000")
MINIO_STORAGE_ACCESS_KEY = env("MINIO_STORAGE_ACCESS_KEY", default="access_key")
MINIO_STORAGE_SECRET_KEY = env("MINIO_STORAGE_SECRET_KEY", default="secret_key")
MINIO_STORAGE_USE_HTTPS = env.bool("MINIO_STORAGE_USE_HTTPS", False)
# Config Buckets Static Media for default
MINIO_STORAGE_MEDIA_BUCKET_NAME = env(
    "MINIO_MEDIA_BUCKET", default="faclab.media.bucket"
)
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_STATIC_BUCKET_NAME = env(
    "MINIO_STATIC_BUCKET", default="faclab.static.bucket"
)
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True

PROTOCOL = "https://" if MINIO_STORAGE_USE_HTTPS else "http://"
MINIO_SERVER_URL = PROTOCOL + env("MINIO_SERVER_URL", default="localhost:9000")
MINIO_STORAGE_STATIC_URL = os.path.join(
    MINIO_SERVER_URL, MINIO_STORAGE_STATIC_BUCKET_NAME
)
MINIO_STORAGE_MEDIA_URL = os.path.join(
    MINIO_SERVER_URL, MINIO_STORAGE_MEDIA_BUCKET_NAME
)
