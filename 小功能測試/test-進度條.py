'''
測試交易
'''
import time
import sys
import os
import threading
from queue import Queue
from queue import Empty
from alive_progress import alive_bar



#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

def test_threading(q:Queue):
    try:
        get_value = q.get(timeout=1)
    except Empty:
        get_value = 0
    print("get_value =",get_value)
    
# Worker 類別，負責處理資料
class Progress_bar(threading.Thread):
    """_summary_
    用來顯示進度條
    Args:
        threading (_type_): 宣告種類
    """
    def __init__(self, queue:Queue, total_num:int):
        """_summary_
        宣告後立即會執行的東西
        Args:
            queue (Queue): 都進來的存列
            total_num (int): 總資料筆數
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.total_num = total_num

    def run(self):
        count = 0
        with alive_bar(self.total_num) as bar:
            while True:
                try:
                    print("hi")
                    get_value = self.queue.get(timeout=60)
                    bar(get_value)
                    count += get_value
                    if count >= self.total_num:
                        break
                except Empty:
                    break

            
    



if __name__ == "__main__":
    qq = Queue()
    #thread = threading.Thread(target=test_threading, args=(qq,))
    #thread.start()
    test_process_bar = Progress_bar(qq, 1000)
    test_process_bar.start()
    print("即將丟值")
    ii = 0
    while ii < 10:
        for i in range(3):
            #print(i,"s",end=" ;")
            time.sleep(1)
        qq.put(100)
        ii+= 1
    
    
    '''
    with alive_bar(100) as bar:	# 给 alive_bar 传入进度条总数目（这里是 100）
        for item in range(100):
            # 等待 1s
            time.sleep(1)
            #更新进度条，进度 +1
            bar()
    '''
