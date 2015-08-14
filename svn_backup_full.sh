#!/bin/sh

# SVN BACKUP Ver 0
# DailyフルDump version
# 日付変更タイミングで配列内のリポジトリをリビジョン指定なしでDumpして、S3にアップ

# /backup/svn/dump ディレクトリが必要です。
# /backup/svn/tool/log ディレクトリにLogをはきます。
# /opt/svn配下のリポジトリが対象です。

# 処理対象リポジトリ
arr_repos=(
    "test"
)
yesterday=`date -d '1 days ago' '+%Y%m%d'`

##########################################################
### functions
### end function
##########################################################

echo "##########################################################"
echo "実施日 ${date}"
echo "##########################################################"

for (( I = 0; I < ${#arr_repos[@]}; ++I ))
do
    echo "バックアップ対象リポジトリ ${arr_repos[$I]}"
done

for (( I = 0; I < ${#arr_repos[@]}; ++I ))
do
    repos=${arr_repos[$I]}
    dumpfile="/backup/svn/dump/${repos}_${yesterday}.dump"
    zipfile="/backup/svn/dump/${repos}_${yesterday}.zip"
    echo $dumpfile

    # dump 実行
    dumpcmd="svnadmin dump /opt/svn/${repos} > ${dumpfile}" 
    eval "date"
    echo $dumpcmd
    eval ${dumpcmd}
    eval "date"


    #echo ${arr_repos[$I]}
    #svndump ${arr_repos[$I]} $yesterday  

    # 圧縮 -jでディレクトリ情報外す
    zipcmd="zip -j ${zipfile} ${dumpfile}"
    echo $zipcmd
    eval ${zipcmd}
    eval "date"

    # S3にアップロード
    s3cmd='aws s3 cp ${zipfile} s3://backup backet/svn/'
    echo $s3cmd
    eval ${s3cmd}
    eval "date"


    # Upしたらdumpファイル削除
    echo "dumpFile, zipFile removing.."
    eval "rm -f ${dumpfile} "
    eval "rm -f ${zipfile} "
    eval "date"

done


echo "バックアップ終了"
echo "##########################################################"

