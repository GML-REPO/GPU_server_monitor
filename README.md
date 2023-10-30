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

To install GPU Monitor on your server, you need a superuser for Add Service.

If you don't want or can't get permission, run a python file directly on the server.

To check the process is running, 
```
sudo systemctl status GPU_Monitor.service
```

If you want to change the port, revise the python code.


## Usage
### Client-side
Just drag&drop client html file to your web-browser.

You can add the server with IP and PORT number.

And, you can save and load the server list.
