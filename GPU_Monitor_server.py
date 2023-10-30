import psutil
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import time

# GPU_MONITOR_PYTHON_PATH = subprocess.check_output(['cat', '/usr/local/bin/GPU_Monitor/GPU_Monitor_python_path.path']).decode('utf-8').replace('\n','')
CPU_INFO = ''
MEM_INFO = ''
GPU_INFO = ''

T1 = 0

app = Flask(__name__)
CORS(app)


@app.route('/system_info')
def get_system_info():
    global T1, CPU_INFO, MEM_INFO, GPU_INFO
    
    if time.time() - T1 > 2:
        get_info()
        T1 = time.time()

    system_info = {
        'cpu': CPU_INFO,
        'mem': MEM_INFO,
        'gpu': GPU_INFO
    }
    return jsonify(system_info)

def get_mem_info():
    mem_percent = psutil.virtual_memory().percent
    mem = subprocess.check_output(['free', '-h']).decode('utf-8')#.replace('\n', '<br>')#.replace('\t', '    ')

    mem_text = []
    _m = mem.split('\n')
    _m[0] = f'{mem_percent}%'+_m[0]
    for __m in _m:
        tokens = __m.split(' ')
        rtokens = []
        for _t in tokens:
            if len(_t) != 0:
                rtokens.append(f'{_t:>13s}')

        mem_text += [' '.join(rtokens)]
    mem_text = '\n'.join(mem_text)
    
    return mem_text

def get_cpu_info():
    output = subprocess.check_output(['date'])
    output = output.decode('utf-8').strip()
    return f'{psutil.cpu_percent()}% | {output}'

def get_gpu_info():

    output = subprocess.check_output(['nvidia-smi', '--query-gpu=driver_version,gpu_uuid,index,name,temperature.gpu,utilization.gpu,memory.used,memory.total,', '--format=csv,noheader,nounits'])
    output = output.decode('utf-8').strip()
    output_proc = subprocess.check_output(['nvidia-smi', '--query-compute-apps=gpu_uuid,pid,used_memory', '--format=csv,noheader,nounits'])
    output_proc = output_proc.decode('utf-8').strip().split('\n')
    gpu_info = []

    gpu_text = []
    driver_version = ''
    for line in output.split('\n'):
        fields = line.split(',')
        fields = [f.strip() for f in fields]
        driver_version, gpu_uuid, gpu_index, gpu_name, gpu_temp, gpu_util, gpu_mem_used, gpu_mem_total = fields
        gpu_name = gpu_name.replace('NVIDIA ', '').replace('GeForce ', '').replace('Quadro ', '')
        gpu_mem_util = f'{float(gpu_mem_used) / float(gpu_mem_total) * 100:5.1f}'

        process_info = []
        if len(output_proc) > 0:
            for line_p in output_proc:
                fields_p = line_p.split(',')
                fields_p = [f.strip() for f in fields_p]
                if len(fields_p) > 1:
                    _gpu_uuid,_pid,_used_memory = fields_p
                    if gpu_uuid == _gpu_uuid:
                        try:
                            name_p = psutil.Process(int(_pid)).username()
                        except:
                            name_p = 'Unknown'

                        process_info += [f'{name_p}({_used_memory}MiB)']

        gpu_info.append({
            'driver_version':driver_version,
            'gpu_index':gpu_index,
            'gpu_name':gpu_name,
            'gpu_temp':gpu_temp,
            'gpu_util':gpu_util,
            'gpu_mem_util':gpu_mem_util,
            'gpu_mem_used':gpu_mem_used,
            'gpu_mem_total':gpu_mem_total,
            'proc':','.join(process_info),
        })

        gpu_text += [f' [{gpu_index}] {gpu_name} | {int(gpu_temp):3d}C, {int(gpu_util):3d}% | {int(gpu_mem_used):5d} / {int(gpu_mem_total):5d} MiB, {gpu_mem_util}% | {",".join(process_info)}']
    gpu_text = [f'Driver version:{driver_version}'] + gpu_text
    gpu_text = '\n'.join(gpu_text).replace('\n', '<br>')
    return gpu_text

def get_info():
    global CPU_INFO, MEM_INFO, GPU_INFO

    try:
        # CPU_INFO = subprocess.check_output([GPU_MONITOR_PYTHON_PATH, '-c', f'import {(__file__.split("/")[-1].split(".")[0])} as GET_INFO; print(GET_INFO.get_cpu_info())'], universal_newlines=True)
        CPU_INFO = get_cpu_info()
    except Exception as e:
        CPU_INFO = 'CPU info get error: '+str(e) + '\n'
        print(CPU_INFO)

    try:
        # MEM_INFO = subprocess.check_output([GPU_MONITOR_PYTHON_PATH, '-c', f'import {(__file__.split("/")[-1].split(".")[0])} as GET_INFO; print(GET_INFO.get_mem_info())'], universal_newlines=True)
        MEM_INFO = get_mem_info()
    except Exception as e:
        MEM_INFO = 'Memory info get error: '+str(e) + '\n'
        print(MEM_INFO)

    try:
        # GPU_INFO = subprocess.check_output([GPU_MONITOR_PYTHON_PATH, '-c', f'import {(__file__.split("/")[-1].split(".")[0])} as GET_INFO; print(GET_INFO.get_gpu_info())'], universal_newlines=True)
        GPU_INFO = get_gpu_info()
    except Exception as e:
        GPU_INFO = 'GPU info get error: '+str(e) + '\n'
        print(GPU_INFO)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60022)
    # print(get_cpu_info())
