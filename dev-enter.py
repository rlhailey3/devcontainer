#!/usr/bin/env python3

import json
import subprocess
import os
import argparse

def main():
    config_file = ".devcontainer"

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--ephemeral", dest="ephemeral", help="If used, container will be deleted after use", action="store_true")
    args = parser.parse_args();

    if check_config(config_file):
        with open(config_file, "r") as file:
            config: dict[str,str] = json.load(file)
        print("[+] entering devcontainer with the following properties")
        for x in config:
            print("\t{0} = {1}".format(x, config[x]))
        if run_container(config):
            exit_container(config, args)
        else:
            # TODO unable to run container
            pass

    else:
        print("[-] no devcontainer configuration exists for this project")
        print("\trun dev-create.py to create a devcontainer for this project")

def run_container(config: dict[str,str]) -> int:
    if search_container(config) == "":
        print("[+] Container does not exist -- creating container")
        if not create_container(config):
            # TODO - Unable to create container message
            return 0
    run_command: list[str] = ["podman", "start", "--attach", config["name"]]
    if not subprocess.call(run_command):
        return 1
    else:
        return 0

def create_container(config: dict[str,str]) -> int:
    create_command: list[str] = ["podman", "create", "-t", "--name", config["name"], "--hostname", config["hostname"], config["image"], "/bin/bash"]
    if not subprocess.call(create_command):
        if config["type"] == "dir":
            for item in os.listdir(config["path"]):
                src_path: str = "{0}/{1}".format(config["path"], item)
                dst_path: str = "{0}:.".format(config["name"])
                copy_command: list[str] = ["podman", "cp", src_path, dst_path]
                if subprocess.call(copy_command):
                    # TODO Failed to copy items
                    return 0
            return 1
        else:
            # TODO Add branch for repo type
            return 0
    else:
        # TODO - Failed to create container
        return 0

def exit_container(config: dict[str, str], args: argparse.Namespace) -> int:
    src_path: str = "{0}:/home/{1}/project/.".format(config["name"], os.getlogin())
    copy_command: list[str] = ["podman", "cp", src_path, "."]
    rm_command: list[str] = ["podman", "rm", config["name"]]
    if not subprocess.call(copy_command, stdout=subprocess.DEVNULL):
        if args.ephemeral:
            print("[+] Deleting container")
            subprocess.call(rm_command, stdout=subprocess.DEVNULL)
    else:
        # TODO Error handle copy failure
        return 0
    return 1

def search_container(config: dict[str, str]) -> str:
    filter_str = "name={0}".format(config["name"])
    search_command = ["podman", "ps", "--filter", filter_str, "--quiet", "--all"]
    process = subprocess.Popen(search_command, stdout=subprocess.PIPE)
    process.wait()
    return process.stdout.read().decode().replace("\n", "") # pyright: ignore [reportOptionalMemberAccess] << stdout is None untill process runs

def check_config(config_file:str) -> int:
    if os.path.exists(config_file):
        return 1
    else:
        return 0

if __name__ == "__main__":
    main()
