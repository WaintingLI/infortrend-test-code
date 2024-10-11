"""
該文件是用來配置顯示訊息的相關文件
當前會有三總文件:
Total.log記錄所有輸出訊息
sys.argv[0]個別檔案的Log(預設層級為DEBUG)
終端機 的輸出(預設層級為DEBUG)
"""
import logging
import platform
import os
import sys





# 路径获取
if platform.system().lower()=='windows':
    cur_dir_test = os.path.abspath(__file__).rsplit("\\", 1)[0]
else:
    cur_dir_test = os.path.abspath(__file__).rsplit("/", 1)[0]
cur_dir = os.path.dirname(sys.argv[0])
print("cur_dir =", cur_dir_test)
log_path = os.path.join(cur_dir, "Total.log")

# encoding='utf-8'
logging.basicConfig(filename=log_path, level=logging.DEBUG,
    filemode = 'w', format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S')

#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')
#logging.error('And non-ASCII stuff, too, like? resund and Malm?')
#logging.critical("critical")


#層級說明:
#Debug > info > warning > error > critical
#如果SetLevel.DEBUG會顯示出所有層級;
#如果SetLevel.WARNING則會顯示warning、error、critical這三個層級

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# set two handlers
#LOG_FILE = f"{__file__}.log"
get_log_name = os.path.basename(sys.argv[0]).replace(".py","")
LOG_FILE = f"{get_log_name}.log"

# rm_file(log_file)
fileHandler = logging.FileHandler(os.path.join(cur_dir, LOG_FILE), mode = 'w')
fileHandler.setLevel(logging.DEBUG)
#fileHandler.setLevel(logging.CRITICAL)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)


# set formatter
formatter = logging.Formatter(
    '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S')
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

# add
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)


def debug(input_string:str="") -> None:
    """用來輸出debug層級的資訊

    Args:
        input_string (str, optional): 輸出資訊. Defaults to "".
    """
    logger.debug(input_string)

def info(input_string:str="") -> None:
    """用來輸出info層級的資訊

    Args:
        input_string (str, optional): 輸出資訊. Defaults to "".
    """
    logger.info(input_string)

def warning(input_string:str="") -> None:
    """用來輸出warning層級的資訊

    Args:
        input_string (str, optional): 輸出資訊. Defaults to "".
    """
    logger.warning(input_string)

def error(input_string:str="") -> None:
    """用來輸出error層級的資訊

    Args:
        input_string (str, optional): 輸出資訊. Defaults to "".
    """
    logger.error(input_string)

def critical(input_string:str="") -> None:
    """用來輸出critical層級的資訊

    Args:
        input_string (str, optional): 輸出資訊. Defaults to "".
    """
    logger.critical(input_string)

def set_consolehandler_level(set_level:str="DEBUG") -> None:
    """設定輸出至終端機(Terminal)的層級,預設為DEBUG會輸出所有類型的訊息
    Args:
        set_level (str, optional): 設定錯誤層級可為DEBUG 、 INFO 、 WARNING 、 ERROR 、 CRITICAL.
        Defaults to "DEBUG".
    """
    #Debug > info > warning > error > critical
    if set_level == "DEBUG":
        consoleHandler.setLevel(logging.DEBUG)
    elif set_level == "INFO":
        consoleHandler.setLevel(logging.INFO)
    elif set_level == "WARNING":
        consoleHandler.setLevel(logging.WARNING)
    elif set_level == "ERROR":
        consoleHandler.setLevel(logging.ERROR)
    elif set_level == "CRITICAL":
        consoleHandler.setLevel(logging.CRITICAL)
    else:
        print("輸入(",set_level,")字串並非Debug 、 info 、 warning 、 error 、 critical")
        print("故沒有設定consoleHandler_level")

def set_filehandler_level(set_level:str="DEBUG") -> None:
    """設定輸出至檔案__file__的層級,預設為DEBUG會輸出所有類型的訊息
    Args:
        set_level (str, optional):  設定錯誤層級可為DEBUG 、 INFO 、 WARNING 、 ERROR 、 CRITICAL.
        Defaults to "DEBUG".
    """
    #Debug > info > warning > error > critical
    if set_level == "DEBUG":
        fileHandler.setLevel(logging.DEBUG)
    elif set_level == "INFO":
        fileHandler.setLevel(logging.INFO)
    elif set_level == "WARNING":
        fileHandler.setLevel(logging.WARNING)
    elif set_level == "ERROR":
        fileHandler.setLevel(logging.ERROR)
    elif set_level == "CRITICAL":
        fileHandler.setLevel(logging.CRITICAL)
    else:
        print("輸入(",set_level,")字串並非Debug 、 info 、 warning 、 error 、 critical")
        print("故沒有設定consoleHandler_level")

if __name__ == "__main__":
    logger.info("test")
    logger.debug("debug test")
    set_filehandler_level("WARNING")
    #set_consolehandler_level("WARNING")
    debug("test debug function")
    debug("test CRITICAL function")
