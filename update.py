import sys
import json

args = sys.argv
print(args)

if len(args) < 2:
    print("Usage: python update.py <channel.json>")
    exit(1)
    
version = 0

with open('channel.json', 'r') as f:
    data = json.load(f)
    version = data["version"]

if version == 0:
    print("No version found in channel.json")
    exit(1)

version += 1

cmds = args[1:]

with open('channel.json', 'w') as f:
    json.dump({"version": version, "cmd": cmds}, f, indent="    ")