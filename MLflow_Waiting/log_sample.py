"""
這是用來當作Logging 的範本
"""
import os
import logging

#路徑獲取
cur_dir = os.path.abspath(__file__).rsplit("/",1)[0]
log_path = os.path.join(cur_dir, "example.log")

# encoding='utf-8'





logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

#set two hadlers
log_file = "{}.log".format(__file__)

#rm_file(log_file)
fileHandler = logging.FileHandler(os.path.join(cur_dir, log_file), mode = 'w')
fileHandler.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

#set format
formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

# add
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)


if __name__ =="__main__":
    logger.info("test")
    logger.info("test")
    logger.info("test")
    logger.info("test")
    logger.debug("213")
    print("123")