import os

MINIO_ADDR = os.getenv("MINIO_ADDR", "192.168.1.10:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRECT_KEY", "minioadmin")
MINIO_1ST_BUCKET = os.getenv("1ST_BUCKET", "alpha")
MINIO_BUCKET_NUM = os.getenv("MINIO_OBJ_LIMIT", 20)

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "tmp/video")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", {"gif", "jpg", "jpeg", "png"})

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}

LOCAL_CACHE_PATH = "./tmp"
LOCAL_TMP_PATH = "/tmp"

STAGE_EXTRACT = "extract"
STAGE_PREDICT = "predict"
ALL_STAGE = [STAGE_EXTRACT, STAGE_PREDICT]

MILVUS_ADDR = os.getenv("MILVUS_ADDR", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")

SEARCH_MAGIC_NUM = os.getenv("SEARCH_MAGIC_NUM", 6)
SEARCH_COUNT_NUM = os.getenv("SEARCH COUNT NUM", 3)


#--------------
META_DATABASE_ENDPOINT = os.getenv("SEARCH_IMAGES_DATABASE_EP", "mysql://root:passwd@192.168.1.10:3306/search")
META_DATABASE_USERNAME = os.getenv("SEARCH_IMAGES_DATABASE_USERNAME", "root")
META_DATABASE_PASSWD = os.getenv("SEARCH_IMAGES_DATABASE_PASSWD", "passwd")
META_DATABASE_NAME = os.getenv("SEARCH_IMAGES_DATABASE_NAME", "search")
