import docker
import json
import os
import time
from datetime import datetime

client = docker.from_env()

while True:
    client.login(username="puller", password="puller", registry="new-tube.ru")

    os.system("git pull")

    current_ids = json.load(open("current_ids.json"))

    need_restart = False
    with open("images-list") as images_list:
        for image_name in images_list.readlines():
            image_name = image_name.strip()
            client.images.pull(image_name)
            id = client.images.get(image_name).id
            if image_name not in current_ids or current_ids[image_name] != id:
                current_ids[image_name] = id
                need_restart = True

    current_ids["checked_at"] = str(datetime.now())

    json.dump(current_ids, open("current_ids.json", 'w'))

    if need_restart:
        os.chdir("/home/new-tube/new-tube/server/")
        os.system("docker login --username puller --password puller new-tube.ru && docker-compose down && git pull && docker-compose pull && docker-compose up -d")
        os.chdir("/home/new-tube/new-tube/server-updater/")

    time.sleep(60 * 5)
