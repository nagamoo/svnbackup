#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
指定リポジトリを/backup/svn/dumpに出力、
圧縮してS3にアップロード、
アップ後、同一リポジトリが複数ある場合、2つ残してふるいの削除

'''


import logging,sys,os
sys.path.append(os.pardir)
import config_svnbackup as config


logger = None

def configtest():
    logging.error(config)
    logging.error(config.LOG_DIR)

def getLogger():
    global logger
    #logging.error("Call getLogger")

    #logging.setLevel(logging.DEBUG)
    #logging.error("    ERROR get Logger      ")
    #logging.debug("    DEBUG get Logger      ")
    #logging.info("     INFO get Logger      ")

    logging.error("##############################################")

    if isinstance(logger, type(None)):
        logging.error(" LOGGER None Type")

    if isinstance(logger, type(None)) == False:
        logger.error("util.py  LOGGER EXITS")
        #logger.error(type(logger))
        return logger

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


    #sys.stderrへ出力するハンドラーを定義
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)

    #log.txtというファイルに出力するハンドラーを定義
    #levelはERROR
    fh = logging.FileHandler(filename= config.LOG_DIR + "/log.txt")
    #fh.setLevel(logging.ERROR)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    #ロガーにハンドラーを登録する
    #logger.addHandler(sh)
    logger.removeHandler(fh)    # なんか複数handlerが登録されちゃうのでしょうがなく・・・・・
    logger.addHandler(fh)

    #logger.debug("CREATE LOGGER")
    #logging.error("TEST2")
    #logging.error(type(logger))
    return logger

def loggingLine():
    logger.info('#############################################')

def loggingError(e):
    logger.error('#####################################')
    logger.error('type:' + str(type(e)))
    logger.error('args:' + str(e.args))
    logger.error('message:' + e.message)
    logger.error('e:' + str(e))




############################################################################################
def convToUTF8List(convlist):
    for index, item in enumerate(convlist):
        if isinstance(item, basestring):
            convitem = item.encode('utf-8')
            convlist[index] = convitem
            #loggingLine()
            #logger.info(index)
            #logger.info(convitem)
            #logger.info(convlist[index])
    return convlist
    


def exec_cmd_unix(self, cmd, output=None, printerr=False):
    try:
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=False)
    except:
        return (256, "", "Popen failed (%s ...):\n  %s" % (cmd[0],
                str(sys.exc_info()[1])))
    stdout = proc.stdout
    stderr = proc.stderr
    self.set_nonblock(stdout)
    self.set_nonblock(stderr)
    readfds = [ stdout, stderr ]
    selres = select.select(readfds, [], [])
    bufout = ""
    buferr = ""
    while len(selres[0]) > 0:
        for fd in selres[0]:
            buf = fd.read(16384)
            if len(buf) == 0:
                readfds.remove(fd)
            elif fd == stdout:
                if output:
                    #output.write(buf)
                    output.info(buf)
                else:
                    bufout += buf
            else:
                if printerr:
                    sys.stdout.write("%s " % buf)
                else:
                    buferr += buf
        if len(readfds) == 0:
            break
        selres = select.select(readfds, [], [])
    rc = proc.wait()
    if printerr:
        print("")
    return (rc, bufout, buferr)


