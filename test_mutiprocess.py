import time
from multiprocessing import Process, Manager, Pool
manager = Manager()
d1 = {'a': 'aa'} 
d = manager.dict()
d.update(d1)


def f(l):
    for item in l:
        d[str(item)] = int(item)
    time.sleep(3)
        

if __name__ == '__main__':

    len_l = 11
    gap = 2
    l = range(len_l)
    split_l = [l[x * gap: (x + 1) * gap] for x in range( (len_l - 1) / gap + 1) ]

    print split_l
    # p = Process(target=f, args=(d, l))
    # p.start()
    # p.join()
    p = Pool(len(split_l))
    p.map(f, split_l)

    print d
