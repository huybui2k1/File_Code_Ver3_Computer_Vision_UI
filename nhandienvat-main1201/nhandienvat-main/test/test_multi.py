import time
import threading
import multiprocessing as mp

def taolao(result_queue):
    print("time:1",time.time())
    time.sleep(2)
    print("Done sleep1")
    # a = 1
    # b = 2
    # c = 3
    # result_queue.append((a,b,c))
    # return a


def taolao2(result_queue):
    print("time:2",time.time())
    time.sleep(1)
    print("Done sleep2")
    # a = 4
    # b = 5
    # c = 6
    # result_queue.append((a,b,c))
    # return a

if __name__ == '__main__':
    result_queue = []

    start_time = time.perf_counter()


    # thread
    p1 = threading.Thread(target=taolao, args=(result_queue,))
    p2 = threading.Thread(target=taolao2, args=(result_queue,))
    
    p1.start()
    p2.start()

    p1.join()

    p2.join()

    #multiprocessing
    p1 = mp.Process(target=taolao, args=(result_queue,))
    p2 = mp.Process(target=taolao2, args=(result_queue,))

    p1.start()
    p2.start()

    p1.join()

    p2.join()

    # taolao(result_queue)
    # taolao2(result_queue)

    # Lấy kết quả từ hàng đợi


    end_time = time.perf_counter()
    print("result_queue: ",result_queue)
    print("time excute: ", end_time - start_time)
