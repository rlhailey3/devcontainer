#!/usr/bin/env python3

import json
import os
import argparse


def main():
    config_file = ".devcontainer"
    container_image = "dev:latest"

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", type=str, help="name of the dev container", default="dev-{0}".format(os.path.basename(os.getcwd())))
    parser.add_argument("-H", "--hostname", dest="hostname", type=str, help="hostname of the dev container", default="dev")
    parser.add_argument("-i", "--image", dest="image", type=str, help="container image to use", default=container_image)
    parser.add_argument("-d", "--directory", dest="directory", type=str, help="directory path of project", default=os.getcwd())
    parser.add_argument("-t", "--type", dest="type", type=str, help="git repo or dir project type", default="dir")
    parser.add_argument("-p", "--path", dest="path", type=str, help="path to git repo or project directory", default=os.getcwd())
    args = parser.parse_args()

    config_path = args.directory + "/" + config_file

    if check_config(config_path, args):
        print("[+] creating devcontainer with the following properties")
        for x in vars(args):
            print("\t{0} = {1}".format(x, vars(args)[x]))
    else:
        print("[-] devcontainer already exists for this project")


def check_config(config_path: str, args: argparse.Namespace) -> int:
    if os.path.exists(config_path):
        return 0
    else:
        with open(config_path, "w+") as file:
            json.dump(vars(args), file, indent=4)
        return 1



if __name__ == "__main__":
    main()
