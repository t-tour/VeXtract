from datetime import datetime
from functools import wraps
import logging
import os.path


class Logger():
    def __init__(self, name):
        self.log_adapter = logging.getLogger(name)
        self.set_level()
        format = '%(asctime)-15s %(name)s [%(levelname)s] %(message)s'
        formatter = logging.Formatter(format)
        self.file_handler = logging.FileHandler(
            './log/log-{}.log'.format(datetime.now().strftime('%Y-%m-%d')),
            mode='a', encoding='utf-8')
        self.file_handler.setFormatter(formatter)
        self.log_adapter.addHandler(self.file_handler)

    def set_level(self, level='d'):
        if level == 'd':
            self.log_adapter.setLevel(logging.DEBUG)
        elif level == 'i':
            self.log_adapter.setLevel(logging.INFO)
        elif level == 'e':
            self.log_adapter.setLevel(logging.ERROR)

    def d(self, msg, *args):
        self.log('{} {}'.format(msg, ' '.join(args)), 'd')

    def i(self, msg, *args):
        self.log('{} {}'.format(msg, ' '.join(args)), 'i')

    def e(self, msg, *args):
        self.log('{} {}'.format(msg, ' '.join(args)), 'e')

    def log(self, msg, level):
        if level == 'd':
            self.log_adapter.debug(msg)
        elif level == 'i':
            self.log_adapter.info(msg)
        elif level == 'e':
            self.log_adapter.error(msg)

    def logit(self, func, *args, **kwargs):

        @wraps(func)
        def wapper(*args, **kwargs):
            
            self.i("calling func {} with {}, {}".format(func.__name__, str(args[1:]), kwargs))
            return func(*args, **kwargs)

        return wapper
