from datetime import datetime
import logging
import os.path


class Logger():
    def __init__(self, name):
        self.log_adapter = logging.getLogger(name)
        self.set_level()
        format = '%(asctime)-15s %(message)s'
        formatter = logging.Formatter(format)
        self.file_handler = logging.FileHandler(
            './logger/logger-{}.log'.format(datetime.now().strftime('%Y-%m-%d')), 'a')
        self.file_handler.setFormatter(formatter)
        self.log_adapter.addHandler(self.file_handler)

    def set_level(self, level='d'):
        if level == 'd':
            self.log_adapter.setLevel(logging.DEBUG)
        elif level == 'i':
            self.log_adapter.setLevel(logging.INFO)
        elif level == 'e':
            self.log_adapter.setLevel(logging.ERROR)

    def d(self, msg):
        self.log_adapter.debug(msg)

    def i(self, msg):
        self.log_adapter.info(msg)

    def e(self, msg):
        self.log_adapter.error(msg)


log = Logger('main')
log.i('log a info')
log.d('just for test12312')
