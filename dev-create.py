#!/usr/bin/env python3

import json
import os
import argparse
import time
import subprocess


def main():
    config_file = ".devcontainer"
    container_image = "dev:latest"
    default_name = "dev-{0}-{1}".format(os.path.basename(os.getcwd()), time.time())
    default_hostname = os.path.basename(os.getcwd())

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", type=str, help="name of the dev container", default=default_name)
    parser.add_argument("-H", "--hostname", dest="hostname", type=str, help="hostname of the dev container", default=default_hostname)
    parser.add_argument("-i", "--image", dest="image", type=str, help="container image to use", default=container_image)
    parser.add_argument("-d", "--directory", dest="directory", type=str, help="directory path of project", default=os.getcwd())
    args = parser.parse_args()

    config_path = args.directory + "/" + config_file

    if check_config(config_path, args):
        print("[+] creating devcontainer with the following properties")
        for x in vars(args):
            print("\t{0} = {1}".format(x, vars(args)[x]))
        if create_container(args):
            print("[+] devcontainer created")
        else:
            print("[-] failed to create devcontainer")

    else:
        print("[-] devcontainer already exists for this project")

def create_container(args: argparse.Namespace):
    project_dir: str = "/project"
    volume_mount: str = "{0}:{1}:Z".format(args.directory, project_dir)
    create_command: list[str] = ["podman", "create", "--name", args.name, "--hostname", args.hostname, "--volume", volume_mount, "--tty", args.image]
    return not subprocess.call(create_command)

def check_config(config_path: str, args: argparse.Namespace) -> int:
    if os.path.exists(config_path):
        return 0
    else:
        with open(config_path, "w+") as file:
            json.dump(vars(args), file, indent=4)
        return 1



if __name__ == "__main__":
    main()
