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
        if run_container(config):
            print("[+] container closed")

    else:
        print("[-] no devcontainer configuration exists for this project")
        print("\trun dev-create.py to create a devcontainer for this project")

def run_container(config: dict[str,str]) -> int:
    if search_container(config) == "":
        print("[-] Container does not exist -- run dev-create.py")
        return 0
    unshare_start_command: list[str] = ["podman", "unshare", "chown", "1000:1000", "-R", config["directory"]]
    unshare_end_command: list[str] = ["podman", "unshare", "chown","0:0", "-R", config["directory"]]
    run_command: list[str] = ["podman", "start", "--attach", config["name"]]
    if not subprocess.call(unshare_start_command):
        if not subprocess.call(run_command):
            if not subprocess.call(unshare_end_command):
                return 1
        print("[-] unable to start devcontainer")
    print("[-] unable to change project directory permissions")
    return 0

def search_container(config: dict[str, str]) -> str:
    filter_str = "name={0}".format(config["name"])
    search_command = ["podman", "ps", "--filter", filter_str, "--quiet", "--all"]
    process = subprocess.Popen(search_command, stdout=subprocess.PIPE)
    process.wait()
    return process.stdout.read().decode().replace("\n", "") # pyright: ignore [reportOptionalMemberAccess] << stdout is 'None' untill process runs

def check_config(config_file:str) -> int:
    if os.path.exists(config_file):
        return 1
    else:
        return 0

if __name__ == "__main__":
    main()
