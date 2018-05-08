#!/usr/bin/env bash

usage(){
    echo "USAGE:"
    echo "sh setup.sh [CMD] [OPTIONS]"
    echo "CMD:"
    echo "makeskin            make skin"
    echo "copyres             copy res"
}



# 参数个数不够，就打印usage并退出
if [ $# -lt 1 ]
then
    usage
    exit 0
fi

# 子命令
cmd=$1
echo $cmd


basepath=$(cd `dirname $0`; pwd)

echo $basepath

if [ $cmd == 'makeskin' ]
then
    sh $basepath/scripts/makeskin.sh $2 $3

elif [ $cmd == 'copyres' ]
then
    sh $basepath/scripts/copyres.sh

fi





