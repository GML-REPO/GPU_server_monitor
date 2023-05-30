
echo "enter the python path which flask/flask_cors is installed: "
read GPU_Monitor_python_path
echo "Enter the path to local file will save: (default: /usr/local/bin)"
read SAVE_PATH

if [ -e "$SAVE_PATH" ]; then
    echo "local file saved in :$SAVE_PATH"
else
    echo "$SAVE_PATH is not exist. local file is saved in /usr/local/bin"
fi

if [ -e "$GPU_Monitor_python_path" ]; then
    echo "python path set : $GPU_Monitor_python_path"

    rm ./GPU_Monitor.service
    touch ./GPU_Monitor.service
    echo "[Unit]"  >> ./GPU_Monitor.service
    echo "Description=Server GPU Monitor Service by GmL" >> ./GPU_Monitor.service
    # echo "After=network.target" >> ./GPU_Monitor.service
    echo "" >> ./GPU_Monitor.service
    echo "[Service]" >> ./GPU_Monitor.service
    echo "ExecStart=$GPU_Monitor_python_path $SAVE_PATH/GPU_Monitor/GPU_Monitor_server.py" >> ./GPU_Monitor.service
    echo "WorkingDirectory=$SAVE_PATH/GPU_Monitor/" >> ./GPU_Monitor.service
    echo "" >> ./GPU_Monitor.service
    echo "[Install]" >> ./GPU_Monitor.service
    echo "WantedBy=default.target" >> ./GPU_Monitor.service


    sudo chmod 755 ./GPU_Monitor_server.py
    sudo rm -r $SAVE_PATH/GPU_Monitor/
    sudo mkdir $SAVE_PATH/GPU_Monitor/
    sudo cp ./GPU* $SAVE_PATH/GPU_Monitor/
    sudo cp $SAVE_PATH/GPU_Monitor/GPU_Monitor.service /etc/systemd/system/
    sudo chmod 644 /etc/systemd/system/GPU_Monitor.service
    sudo systemctl daemon-reload
    sudo systemctl enable GPU_Monitor.service
    sudo systemctl start GPU_Monitor.service
    sudo systemctl status GPU_Monitor.service
else
    echo "$GPU_Monitor_python_path is not exist"
fi
