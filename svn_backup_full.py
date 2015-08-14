#!/usr/bin/env python
# -*- coding:utf-8 -*- 


'''
指定リポジトリを/backup/svn/dumpに出力、
圧縮してS3にアップロード、
アップ後、同一リポジトリが複数ある場合、2つ残してふるいの削除

'''   

import os, sys, datetime, commands
import config_svnbackup as config 
import lib.util as util 
import boto3


s3 = boto3.resource('s3')

class SvnBackup:
    LIST_REPOS=[
        "reponame",
    ]
    #reload(util)
    logger = util.getLogger()
    logger.debug("debug test") 

    util.loggingLine()
    logger.info("実施日 {0} ".format( datetime.datetime.today()))
    util.loggingLine()

    yesterday = datetime.date.today() + datetime.timedelta(days=-1)
    logger.info(yesterday)


    for repos in LIST_REPOS:
        util.loggingLine()
        logger.info(repos)

        dumpfile = "/backup/svn/dump/{repos}_{yesterday}.dump".format(repos=repos, yesterday=yesterday)
        zipfile = "/backup/svn/dump/{repos}_{yesterday}.zip".format(repos=repos, yesterday=yesterday.strftime("%Y%m%d"))

        # dump 実行
        dumpcmd="svnadmin dump /opt/svn/{repos} > {dumpfile}".format(repos=repos, dumpfile=dumpfile)
        #dumpcmd = [ "svnadmin", "dump", "/opt/svn/{0}".format(repos), "> {0}".format(dumpfile)  ]
        logger.info("{0}".format( datetime.datetime.today()))
        logger.info("{0}".format(dumpcmd))

        try:
            #r = os.system(dumpcmd)
            r = commands.getoutput(dumpcmd)
            logger.info("r : {0}".format( r ))
        except:
            logger.error("svnadmin dump failed {0} : {1}, {2}".format(dumpcmd, str(sys.exc_info()[0]), str(sys.exc_info()[1]) ))
            continue
        logger.info("{0}".format( datetime.datetime.today()))


        # 圧縮 -jでディレクトリ情報外す
        zipcmd="zip -j {zipfile} {dumpfile}".format(zipfile=zipfile, dumpfile=dumpfile)
        logger.info("{0}".format( datetime.datetime.today()))
        logger.info("{0}".format(zipcmd))
        try:
            r = commands.getoutput(zipcmd)
            logger.info("r : {0}".format( r ))
        except:
            logger.error("dumpfile zipping failed {0} : {1}, {2}".format(dumpcmd, str(sys.exc_info()[0]), str(sys.exc_info()[1]) ))
            continue
        logger.info("{0}".format( datetime.datetime.today()))

        # S3にアップロード
        s3upcmd='aws s3 cp {zipfile} s3://backet name/svn/'.format(zipfile=zipfile)
        logger.info("{0}".format( datetime.datetime.today()))
        logger.info("{0}".format( s3upcmd))
        try:
            r = commands.getoutput(s3upcmd)
            logger.info("r : {0}".format( r ))
        except:
            logger.error("S3 Upload failed {0} : {1}, {2}".format(dumpcmd, str(sys.exc_info()[0]), str(sys.exc_info()[1]) ))
            continue
        logger.info("{0}".format( datetime.datetime.today()))

        # S3
        try:
            zips = [] # これにS3のzipファイル名を突っ込む
            s3 = boto3.client('s3')
            my_bucket =s3.list_objects(Bucket='src-backup-im',  Prefix='svn/{0}'.format(repos))
            for object in my_bucket["Contents"]:
                #util.logger.debug(type(object))
                util.logger.debug("zipfile {0}".format(object["Key"]))
                zips.append(object["Key"])
            zips.sort(reverse=True)
            #util.logger.info(zips)

            if len(zips) > 2:
                util.logger.info("バックアップ数2以上。削除ファイル有")
                for zipfile in zips[2:]: 
                    util.logger.info("DELETE FILE:{0}".format(zipfile))
                    res = s3.delete_object(Bucket='src-backup-im',  Key=zipfile)
                    util.logger.info("DELETE RESULT:{0}".format(res))
        except:
            logger.error("S3 FILE DELETE failed {0} : {1}, {2}".format(dumpcmd, str(sys.exc_info()[0]), str(sys.exc_info()[1]) ))
            continue

        # Local の使用ファイル削除
        logger.info("{0}, {1} removing..".format(dumpfile, zipfile))
        try:
            r = commands.getoutput("rm -f {dumpfile} ".format(dumpfile=dumpfile))
            logger.info("r : {0}".format( r ))
            r = commands.getoutput("rm -f {zipfile} ".format(zipfile=zipfile))
            logger.info("r : {0}".format( r ))
        except:
            logger.error("Local File Delte failed {0} : {1}, {2}".format(dumpcmd, str(sys.exc_info()[0]), str(sys.exc_info()[1]) ))
            continue

        logger.info("{0} backup.".format(repos))
        util.loggingLine()

if __name__ == "__main__":
    SvnBackup()



