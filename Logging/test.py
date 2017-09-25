import Logger
import threading


def log(num):
    logger = Logger.Logger()
    for _ in range(10000):
        logger.log("hello from " + str(num))


def main():
    t = []
    t.append(threading.Thread(target=(lambda: log(1))))
    t.append(threading.Thread(target=(lambda: log(2))))
    t.append(threading.Thread(target=(lambda: log(3))))
    t.append(threading.Thread(target=(lambda: log(4))))
    t.append(threading.Thread(target=(lambda: log(5))))
    for td in t:
        td.start()
    for td in t:
        td.join()


if __name__ == "__main__":
    main()
