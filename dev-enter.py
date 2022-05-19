#!/usr/bin/env python3

import json
import subprocess
import os

def main():
    config_file = ".devcontainer"

    if check_config(config_file):
        with open(config_file, "r") as file:
            config: dict[str,str] = json.load(file)
        print("[+] entering devcontainer with the following properties")
        for x in config:
            print("\t{0} = {1}".format(x, config[x]))
        if not run_container(config):
            exit_container(config)
        else:
            # TODO unable to run container
            pass

    else:
        print("[-] no devcontainer configuration exists for this project")
        print("\trun dev-create.py to create a devcontainer for this project")

def run_container(config: dict[str,str]) -> int:
    create_command: list[str] = ["podman", "create", "-t", "--name", config["name"], "--hostname", config["hostname"], config["image"], "/bin/bash"]
    run_command: list[str] = ["podman", "start", "--attach", config["name"]]
    subprocess.call(create_command)
    if config["type"] == "dir":
        for item in os.listdir(config["path"]):
            src_path: str = "{0}/{1}".format(config["path"], item)
            dst_path: str = "{0}:.".format(config["name"])
            copy_command: list[str] = ["podman", "cp", src_path, dst_path]
            subprocess.call(copy_command)
    else:
        # TODO Add branch for repo type
        pass
    if subprocess.call(run_command):
        return 1
    else:
        return 0

def exit_container(config: dict[str, str]):
    src_path: str = "{0}:/home/{1}/project/.".format(config["name"], os.getlogin())
    copy_command: list[str] = ["podman", "cp", src_path, "."]
    rm_command: list[str] = ["podman", "rm", config["name"]]
    if not subprocess.call(copy_command):
        subprocess.call(rm_command)
    else:
        # TODO Error handle copy failure
        pass

def check_config(config_file:str) -> int:
    if os.path.exists(config_file):
        return 1
    else:
        return 0

if __name__ == "__main__":
    main()
