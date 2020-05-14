import base64
import requests
import glob
import os

dir = "/tmp/256_ObjectCategories"
addr = "http://127.0.0.1:6000/v1/application/example/upload"


if __name__ == "__main__":
    file_list = []
    success_count, fail_count = 0, 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".jpg"):
                file_list.append(os.path.join(root, file))
    for img in file_list:
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            data = {
                "fields": {
                    "full": {
                        "data": encoded_string
                    }
                },
                "targetFields": {
                    "data": encoded_string
                }
            }
            r = requests.post(addr, json=data)
            if r.status_code == 200:
                success_count += 1
            else:
                fail_count += 1
            print("success: {} fail: {} total: {}".format(success_count, fail_count, len(file_list)))
