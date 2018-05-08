#!/usr/bin/env bash

# 生成皮肤，在players/publish/

usage(){
    echo "USAGE:"
    echo "makeskin hallpath skinname"
    echo "OPTIONS:"
    echo "hallpath            hall path"
    echo "skinname             skin name"
}

# 参数个数不够，就打印usage并退出
if [ $# -lt 2 ]
then
    usage
    exit 0
fi

hallpath=$1
skinname=$2

basepath=$(cd `dirname $0`; pwd)

echo $basepath

skin_path=$(cd $basepath; cd ..; pwd)


echo $skin_path


#echo $0 $1 $2 $3


rm -rf $skin_path/publish
sh $hallpath/makeskin.sh $skinname all $skin_path



