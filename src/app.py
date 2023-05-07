from flask import Flask, request
import logging as log
import multiprocessing
import traceback

from .config import *
from .tasks import *

electric = Flask('electric')

def call_global_function(name):
    global_namespace = globals()
    function_to_call = global_namespace.get(name)
    result = None
    if callable(function_to_call):
        print('开始调用函数：{}...'.format(name))
        try:
            result = function_to_call()
        except Exception as e:
            print(traceback.format_exc())
            result = {
                'result': False,
                'msg': '执行异常：{}'.format(e)
            }
        print('函数调用结束：{}...'.format(name))
    else:
        print('未找到可调用函数：{}'.format(name))
        result = {
            'result': False,
            'msg': '未找到可调用函数：{}'.format(name)
        }
    return result

@electric.route('/create_task', methods=['POST'])
def create_task():
    print(request.json)
    params = request.json
    task = params['task']
    result = call_global_function(task)
    return result

if __name__ == '__main__':
   electric.run(port=port)
