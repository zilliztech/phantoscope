import os
import sys
import glob
import getopt
import base64
import requests

data_dir = "/tmp/256_ObjectCategories"
upload_url = "http://127.0.0.1:5000/v1/application/example/upload"

if __name__ == "__main__":

    opts, args = getopt.getopt(sys.argv[1:], '-h-d:-s:', ['help', 'data_path=', "server="])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[*] Help info")
            exit()
        if opt_name in ('-s', '--server'):
            server_addr = opt_value
            print("[*] Server address:port is ", server_addr)
            upload_url = "http://%s/v1/application/example/upload" % server_addr
            continue
        if opt_name in ('-d', '--data_path'):
            data_dir = opt_value
            print("[*] Data directory is ", data_dir)
            continue

    file_list = []
    success_count, fail_count = 0, 0
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".jpg"):
                file_list.append(os.path.join(root, file))

    for img in file_list:
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = str(encoded_string, encoding='utf-8')
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
            r = requests.post(upload_url, json=data)
            if r.status_code == 200:
                success_count += 1
            else:
                fail_count += 1
            print("success: {} fail: {} total: {}".format(success_count, fail_count, len(file_list)))

    print("All data has been uploaded: \n",
          "success: {} fail: {} total: {}".format(success_count, fail_count, len(file_list)))
