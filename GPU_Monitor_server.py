import psutil
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import time


GPU_PREFIXES = ['NVIDIA', 'GeForce', 'Quadro']
UPDATE_RATE = 2
CUDA_PATH = '/usr/local'
PORT = 60022

LAST_UPDATE = 0
CPU_INFO = ''
MEM_INFO = ''
GPU_INFO = ''

app = Flask(__name__)
CORS(app)

@app.route('/system_info')
def get_system_info():
    global LAST_UPDATE, CPU_INFO, MEM_INFO, GPU_INFO
    
    if time.time() - LAST_UPDATE > UPDATE_RATE:
        update_param()
        get_info()
        LAST_UPDATE = time.time()

    system_info = {
        'cpu': CPU_INFO,
        'mem': MEM_INFO,
        'gpu': GPU_INFO
    }
    return jsonify(system_info)

def update_param():
    global UPDATE_RATE, CUDA_PATH, GPU_PREFIXES, PORT
    try:
        setting_file = open('/'.join(__file__.split('/')[:-1])+'/setting.txt', 'r')
        lines = setting_file.readlines()
        for line in lines:
            key,value = line.split('=')[:2]
            value=value.replace('\n', '')
            if key == 'UPDATE_RATE': UPDATE_RATE = int(value)
            elif key == 'CUDA_PATH': CUDA_PATH = value
            elif key == 'GPU_PREFIXES': GPU_PREFIXES = value.split(',')
            elif key == 'PORT': PORT = int(value)
    except: pass


def get_mem_info():
    mem_percent = psutil.virtual_memory().percent
    mem = subprocess.check_output(['free', '-h']).decode('utf-8')

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

    gpu_text = []
    driver_version = ''
    for line in output.split('\n'):
        fields = line.split(',')
        fields = [f.strip() for f in fields]
        driver_version, gpu_uuid, gpu_index, gpu_name, gpu_temp, gpu_util, gpu_mem_used, gpu_mem_total = fields
        for prefixes in GPU_PREFIXES:
            gpu_name = gpu_name.replace(prefixes, '')
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


        gpu_text += [f' [{gpu_index}] {gpu_name} | {int(gpu_temp):3d}C, {int(gpu_util):3d}% | {int(gpu_mem_used):5d} / {int(gpu_mem_total):5d} MiB, {gpu_mem_util}% | {",".join(process_info)}']
    
    cuda_text = []
    try:
        cuda_out = subprocess.check_output(['ls', '-al', CUDA_PATH]).decode('utf-8').strip()
        for line in cuda_out.split('\n'):
            if 'cuda' in line:
                cuda_text.append(''.join(line.split()[8:]))
        cuda_text = '*'+' , '.join(cuda_text)
    except Exception as e: cuda_text = str(e)

    gpu_text = [f'Driver version:{driver_version} - CUDA: {cuda_text}'] + gpu_text
    gpu_text = '\n'.join(gpu_text).replace('\n', '<br>')
    return gpu_text

def get_info():
    global CPU_INFO, MEM_INFO, GPU_INFO

    try:
        CPU_INFO = get_cpu_info()
    except Exception as e:
        CPU_INFO = 'CPU info get error: '+str(e) + '\n'
        print(CPU_INFO)

    try:
        MEM_INFO = get_mem_info()
    except Exception as e:
        MEM_INFO = 'Memory info get error: '+str(e) + '\n'
        print(MEM_INFO)

    try:
        GPU_INFO = get_gpu_info()
    except Exception as e:
        GPU_INFO = 'GPU info get error: '+str(e) + '\n'
        print(GPU_INFO)


if __name__ == '__main__':
    update_param()
    app.run(host='0.0.0.0', port=PORT)
