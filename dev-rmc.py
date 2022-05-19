#!/usr/bin/env python3

import json
import subprocess
import os

def main():
    config_file = ".devcontainer"

    if check_config(config_file):
        with open(config_file, "r") as file:
            config: dict[str,str] = json.load(file)
        if search_container(config):
            if delete_container(config):
                print("[+] Container deleted")
            else:
                print("[-] Unable to delete container")
        else:
            print("[-] Container does not exist")

def delete_container(config: dict[str, str]) -> int:
    rm_command: list[str] = ["podman", "rm", config["name"]]
    if not subprocess.call(rm_command):
        return 1
    return 0

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
