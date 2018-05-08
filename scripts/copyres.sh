#!/usr/bin/env bash


basepath=$(cd `dirname $0`; pwd)

echo $basepath
cd $basepath/../


hall_path=$(cat $basepath/../player_config.json | grep 'hallPath' | awk -F '"' '{print $4}')
#hall_path=$(echo $hall_path'hall.json')
echo $hall_path

# 组装games
cp publish/common games/ -rf
cp publish/hall games/ -rf
cp $(echo $hall_path'hall.json') games/hall/
cp $(echo $hall_path'config/*') games/hall/config/


# 放到player.app
cp games/common player.app/Contents/Resources/games/ -rf
cp games/hall player.app/Contents/Resources/games/ -rf


# copy player

count=4
while(( $count>= 0 ))
do
    dstapp=$(echo player$count.app)

    echo $dstapp

    rm $dstapp -rf

    cp player.app $dstapp -rf

    config_path=$dstapp/Contents/Resources/player/player_config.json

    cp player_config.json $config_path

    python $basepath/modify_player_config.py $config_path $count

    let "count--"
done