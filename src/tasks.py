import subprocess
import os
import psutil

DATA_PATH = 'data'

def test_stable_diffusion():
    pass

def write_pid(name, pid):
    with open(os.path.join(DATA_PATH, name), 'w') as f:
        f.write(str(pid))
    
def test_pid(name, key_word):
    # 打开${DATA_PATH}/${name}文件，读取其中的pid
    path = os.path.join(DATA_PATH, name)
    if not os.path.exists(path):
        return False
    pid_in_file = None
    with open(path, 'r') as f:
        pid_in_file = f.read().strip()
    # 检查系统中是否存在pid
    command = 'ps -ef | grep {} | grep -v grep | grep \'{}\''.format(pid_in_file, key_word)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid_in_system = process.stdout.read().decode('utf-8').strip()
    if pid_in_system == '':
        return False
    return True
    
def kill_pid(name, key_word):
    if not test_pid(name, key_word):
        print('pid not found.')
        return {
            'result': False,
            'msg': 'pid not found.'
        }
    # 打开${DATA_PATH}/${name}文件，读取其中的pid
    path = os.path.join(DATA_PATH, name)
    pid_in_file = None
    with open(path, 'r') as f:
        pid_in_file = f.read().strip()
    parent = psutil.Process(int(pid_in_file))
    children = parent.children(recursive=True)  # 获取所有子进程（包括递归子进程）

    for child in children:
        print('Terminating child process with PID: {}'.format(child.pid))
        child.terminate()  # 终止子进程
    parent.terminate()  # 终止父进程
    print('pid killed.')
    return {
        'result': True,
        'msg': 'ok.'
    }

def launch_stable_diffusion():
    path = '/Users/yujiaping/Documents/Tool/stable_diffusion/stable-diffusion-webui'
    cmd = 'bash webui.sh'
    pid_name = 'stable_diffusion.pid'
    if test_pid(pid_name, cmd):
        print('stable diffusion already launched.')
        return {
            'result': False,
            'msg': 'stable diffusion already launched.'
        }
    command = 'cd {} && {}'.format(path, cmd)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = process.pid
    write_pid('stable_diffusion.pid', pid)
    print('stable diffusion launched.')
    return {
        'result': True,
        'msg': 'ok.'
    }
    
def stop_stable_diffusion():
    cmd = 'bash webui.sh'
    pid_name = 'stable_diffusion.pid'
    return kill_pid(pid_name, cmd)
    
if __name__ == '__main__':
    print(kill_pid('stable_diffusion.pid', 'bash webui.sh'))