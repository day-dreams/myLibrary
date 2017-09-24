#! coding:utf-8

"""
    日志类
"""
import sys
import datetime
import threading


FATAL = 4
ERROR = 3
INFO = 2
DEBUG = 1


class Logger:
    """
        线程安全的日志类,默认行为将日志信息输出到文件
    """
    handler = []
    filename = "log.txt"
    fileopen = False
    handleready = False
    filelock = threading.Lock()
    printlock = threading.Lock()
    initlock = threading.Lock()

    def __init__(self, default_level=DEBUG):
        Logger.initlock.acquire()
        if not Logger.fileopen:
            self.file = open(Logger.filename, mode='a')
            Logger.fileopen = True
        if not Logger.handleready:
            Logger.handler.append(self._print_to_file)
            Logger.handleready = True
        Logger.initlock.release()
        self.default_level = default_level

    def _print_to_file(self, record):
        Logger.filelock.acquire()
        self.file.write(record + '\n')
        Logger.filelock.release()

    def _get_current_frame(self):
        """
            获取当前调用栈
        """
        try:
            raise Exception
        except:
            return sys.exc_info()[2].tb_frame.f_back

    def _generate_frame_info(self, framelevel=2):
        """
            获取调用栈信息
        """
        frame = self._get_current_frame()
        for _ in range(framelevel):
            frame = frame.f_back  # 倒退两级调用栈
        code = frame.f_code
        return (code.co_filename, frame.f_lineno)

    def _generate_date_info(self):
        """
            获取日期字符串
        """
        return datetime.datetime.now().strftime("%Y.%m.%d:%H%m%S")

    def _get_level(self, levelcode):
        """
            获取日志等级字符串
        """
        if levelcode == DEBUG:
            return "DEBUG"
        if levelcode == INFO:
            return "INFO "
        if levelcode == ERROR:
            return "ERROR"
        if levelcode == FATAL:
            return "FATAL"

    def log(self, details, levelcode=INFO, need_print=True):
        """
            处理日志记录
        """
        if levelcode < self.default_level:
            return

        date = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        frameinfo = self._generate_frame_info()
        record = date + " " + \
            frameinfo[0] + "," + str(frameinfo[1]) + " " + \
            self._get_level(levelcode) + " : " + details

        if need_print:
            Logger.printlock.acquire()
            print record
            Logger.printlock.release()

        for handler in Logger.handler:
            handler(record)

    @staticmethod
    def add_handler(handler):
        """
            添加日志记录处理handler,可用于日志redis化等用途
        """
        Logger.handler.append(handler)


if __name__ == "__main__":
    # examples
    logger = Logger()
    logger.log("hello")
