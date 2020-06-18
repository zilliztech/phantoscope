import time
import os
import logging
import urllib.request
import base64
LOCAL_TMP_PATH = os.getenv("UPLOAD_FOLDER", "/tmp/")


def save_tmp_file(name, file_data=None, url=None):
    start = time.time()
    extension = 'jpg'
    file_path = os.path.join(LOCAL_TMP_PATH, name + '.' + extension)
    if file_data:
        img_data = file_data.split(",")
        if len(img_data) == 2:
            posting = img_data[0]
            data_type = posting.split("/")[1]
            extension = data_type.split(";")[0]
            encode_method = data_type.split(";")[1]
            if encode_method != "base64":
                logging.error("Encode method not base64")
                raise
            imgstring = img_data[1]
        else:
            imgstring = img_data[0]
        file_path = os.path.join(LOCAL_TMP_PATH, name + '.' + extension)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(imgstring))
    if url:
        try:
            urllib.request.urlretrieve(url, file_path)
        except Exception as e:
            logging.error("Download file from url error : %s", str(e), exc_info=True)
            raise
    end = time.time()
    logging.info('  save_tmp_file cost: {:.3f}s'.format(end - start))
    return file_path

# can define your utils code here
