import os
import sys
import glob
import getopt
import json
import base64
import requests

data_dir = "/tmp/256_ObjectCategories"
server_addr = "127.0.0.1:5000"
application_name = "example"


def get_application_body():
    global application_name
    global server_addr
    url = "http://%s/v1/application/%s" % (server_addr, application_name)
    reply = requests.get(url)
    content = json.loads(reply.content)
    application_feilds = content["_fields"]
    image_field = "full"
    for field_name, value in application_feilds.items():
        if value.get("type", None) == 'object':
            image_field = field_name
            break

    def get_json_body(base64_image):
        template_data = {
            "fields": {
                image_field: {
                    "data": base64_image
                }
            },
            "targetFields": {
                "data": base64_image
            }
        }
        return template_data

    return get_json_body


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], '-h-d:-s:-n:', ['help', 'data_path=', "server=", 'name'])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print("[*] Help info")
            exit()
        if opt_name in ('-s', '--server'):
            server_addr = opt_value
            print("[*] Server address:port is ", server_addr)
            continue
        if opt_name in ('-d', '--data_path'):
            data_dir = opt_value
            print("[*] Data directory is ", data_dir)
            continue
        if opt_name in ('-n', '--name'):
            application_name = opt_value
            print("[*] Application name is ", data_dir)
            continue

    upload_url = "http://%s/v1/application/%s/upload" % (server_addr, application_name)
    print("upload url is ", upload_url)

    template_data_fn = get_application_body()
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
            data = template_data_fn(encoded_string)
            r = requests.post(upload_url, json=data)
            if r.status_code == 200:
                success_count += 1
            else:
                fail_count += 1
                print("Error due to: ", r.content)
            print("success: {} fail: {} total: {}".format(success_count, fail_count, len(file_list)))

    print("All data has been uploaded: \n",
          "success: {} fail: {} total: {}".format(success_count, fail_count, len(file_list)))
