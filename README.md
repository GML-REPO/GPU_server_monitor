# GPUserver_Monitor

Simple GPU Server Monitor

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Requirements
### Client-side
web-browser for html
### Server-side

```
nvidia-smi
```

```
python3
psutil
subprocess
flask
flask_cors
```

## Installation
### Server-side
```
sudo bash setup_GPU_Monitor_server.sh
```
And follow the instruction from the prompt.

To install GPU Monitor on your server, you need a superuser permission to register Service.

If you don't want or can't get a permission, run the python file directly on the server manually.

To check the process(service) is running, 
```
sudo systemctl status GPU_Monitor.service
```

If you want to change some variables like port, update_rate, cuda_path, etc.,

change the setting.txt in the save path(default:/usr/local/bin/GPU_Monitor/setting.txt)

and then, restart the service or the python file.


## Usage
### Client-side
Just drag&drop client html file to your web-browser.

You can add the server with IP and PORT number.

And, you can save and load the server list.
