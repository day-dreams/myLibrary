import Queue
import ThreadEntry
from time import sleep

q=Queue.Queue()
qq=Queue.Queue()

def produce():
    for i in range(10):
        sleep(1)
        q.put(i)

def consume():
    while True:
        num=q.get(timeout=3)
        qq.put(num)
        # print "[got number]: ",num

def consume_again():
    while True:
        num=qq.get(timeout=3)
        print "[got number]: ",num

def main():
    first_model=ThreadEntry.ProduceConsumerModel(produce,consume)
    second_model=ThreadEntry.ProduceConsumerModel(consume,consume_again)

    first_model.prepare()
    second_model.prepare()

    first_model.run()
    second_model.run()

    first_model.join()
    second_model.join()

if __name__=="__main__":
    main()
