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
python3
flask
flask_cors
```


## Installation
### only for server
```
sudo bash setup_GPU_Monitor_server.sh
```
And follow the instruction from the prompt.

To install GPU Monitor on your server, you need a superuser for Add Service.

If you don't want or can't get the permission, you can run a Python file on your server.

in this case, you may need to change some lines in the python file.

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
