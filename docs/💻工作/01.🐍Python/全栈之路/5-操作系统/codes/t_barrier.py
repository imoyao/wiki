#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2020/6/28 17:37
import threading
import time
import random

"""
https://www.cnblogs.com/ZXYloveFR/p/11300172.html

Barrier从字面理解是屏障的意思，主要是用作集合线程，然后再一起往下执行。再具体一点，在Barrier之前，若干个thread各自执行，然后到了Barrier的时候停下，等待规定数目的所有的其他线程到达这个Barrier，之后再一起通过这个Barrier各自干自己的事情。

这个概念特别像小时候集体活动的过程，大家从各自的家里到学校集合，待人数都到齐之后，之后再一起坐车出去，到达指定地点后一起行动或者各自行动。

而在计算机的世界里，Barrier可以解决的问题很多，比如，一个程序有若干个线程并发的从网站上下载一个大型xml文件，这个过程可以相互独立，因为一个文件的各个部分并不相关。而在处理这个文件的时候，可能需要一个完整的文件，所以，需要有一条虚拟的线让这些并发的部分集合一下从而可以拼接成为一个完整的文件，可能是为了后续处理也可能是为了计算hash值来验证文件的完整性。而后，再交由下一步处理。

本示例中模拟发车，按照上座率进行发车，只有等够3个人，才会发一次车，否则会一直等；在最后一次，剩余人数不够发车条件，直接发车。
"""


def worker(barrier):
    global NUM_THREADS
    print(threading.current_thread().name,
          'waiting for barrier with {} others'.format(
              barrier.n_waiting))
    pause_time = random.randint(1, 5) / 10
    time.sleep(pause_time)
    NUM_THREADS -= 1
    try:
        worker_id = barrier.wait()
    except threading.BrokenBarrierError:
        print(threading.current_thread().name, 'Aborting,there are {} left!'.format(NUM_THREADS))
    else:
        print('Sleep {} seconds,There just {} left!'.format(pause_time, NUM_THREADS))
        print(threading.current_thread().name, 'after barrier',
              worker_id)


NUM_THREADS_PARTIES = 3
NUM_THREADS = 11


def main():
    b = threading.Barrier(NUM_THREADS_PARTIES)
    for i in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(b,))
        t.start()
        time.sleep(.6)
    if NUM_THREADS <= 0:  # 没人了，不等了
        print('no left!=====just abort======')
        '''
        Barrier 的 abort() 方法会导致所有等待中的线程接收到一个 BrokenBarrierError。 我们可以使用此方法来告知那些被阻塞住的线程该结束了。
        '''
        b.abort()


if __name__ == '__main__':
    main()

'''
Thread-1 waiting for barrier with 0 others
Thread-2 waiting for barrier with 1 others
Thread-3 waiting for barrier with 2 others
Sleep 0.3 seconds,There just 8 left!
Thread-2 after barrierSleep 0.4 seconds,There just 8 left!
Thread-3 Sleep 0.1 seconds,There just 8 left!
Thread-1 1
after barrier  after barrier 0
2
Thread-4 waiting for barrier with 0 others
Thread-5 waiting for barrier with 1 others
Thread-6 waiting for barrier with 2 others
Sleep 0.5 seconds,There just 5 left!
Sleep 0.2 seconds,There just 5 left!
Thread-5 Sleep 0.5 seconds,There just 5 left!
Thread-4 Thread-6 after barrierafter barrierafter barrier 0  
2
1
Thread-7 waiting for barrier with 0 others
Thread-8 waiting for barrier with 1 others
Thread-9 waiting for barrier with 2 others
Sleep 0.1 seconds,There just 2 left!Sleep 0.3 seconds,There just 2 left!
Thread-9 after barrier
 2
Sleep 0.5 seconds,There just 2 left!Thread-7
Thread-8 after barrier after barrier 1 0
# 剩余两个，一车拉走
Thread-10 waiting for barrier with 0 others
Thread-11 waiting for barrier with 1 others
no left!=====just abort======
Thread-11 Aborting,there are 0 left!
Thread-10 Aborting,there are 0 left!

Process finished with exit code 0
'''
