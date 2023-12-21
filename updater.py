import docker, json, os

client = docker.from_env()

current_ids = json.load(open("current_ids.json"))


need_restart = False
with open("images-list") as images_list:
    for image_name in images_list.readlines():
        client.images.pull(image_name)
        id = client.images.get(image_name).id
        if image_name not in current_ids or current_ids[image_name] != id:
            current_ids[image_name] = id
            need_restart = True

json.dump(current_ids, open("current_ids.json", 'w'))

if need_restart:
    os.system("./restart.sh")
