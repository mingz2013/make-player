# -*- coding: UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os
import json
import shutil
import uuid

CUR_DIR=''

"""
    player_utils功能说明:
    初始化player
    makeskin
"""
#移除文件夹
def removeFodler(folderPath):
    if (os.path.exists(folderPath)):
        shutil.rmtree(folderPath, onerror=readonly_handler);

def readonly_handler(func, path, execinfo):
    os.chmod(path, 128)  # or os.chmod(path, stat.S_IWRITE) from "stat" module
    func(path)

#拷贝文件夹
def copyFodler(srcFolder, destFodler):
    if(os.path.exists(srcFolder)):
         shutil.copytree(srcFolder, destFodler);
         # print 'copy foler from ' + srcFolder + ' to '+destFodler

def replaceFolder(srcFolder,destFolder):
    removeFodler(destFolder);
    copyFodler(srcFolder, destFolder);

def getMacAddress():
    """获取本机mac地址
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def dumpPrettyJson(jsonObj):
    return json.dumps(jsonObj, ensure_ascii=False, indent=4).encode('utf-8')


def modifyPlayerConfig(configPath,index,config):
    """修改player相关配置
    """
    configJson = json.load(file(configPath))

    # 修改mac地址
    macAddr = getMacAddress()
    if index == -1:
        print "do not set playerAddr"
    elif index < 10:
        configJson["playerAddr"] = macAddr[:-2] + "0" + str(index)
    else:
        configJson["playerAddr"] = macAddr[:-2] + str(index)

    configJson["playerPath"]=config["playerPath"]
    configJson["hallPath"]=config["hallPath"]
    configJson["screenHeight"]=config["screenHeight"]
    configJson["screenWidth"]=config["screenWidth"]
    configJson["windowName"]="player"+str(index)
    with open(configPath, 'w') as f:
        f.write(dumpPrettyJson(configJson));

def makePlayer(config):
    """player初始化
    """
    dstPath = config["playerPath"]
    checkPath(dstPath)
    print 'player path='+dstPath

    playerNum = 4
    if not os.path.isdir(dstPath):
        cmd = "mkdir -p " + dstPath
        os.system(cmd)
    for i in xrange(1, playerNum + 1):
        dstPlayerPath = os.path.join(dstPath, "player" + str(i) + ".app")
        if os.path.exists(dstPlayerPath):
            shutil.rmtree(dstPlayerPath)

        print 'initialize player%s.app ...' % i
        shutil.copytree(os.path.join(dstPath, "player.app"), dstPlayerPath)
        dstPlayerConfig = os.path.join(dstPlayerPath, "Contents", "Resources", "player", "player_config.json")
        modifyPlayerConfig(dstPlayerConfig, i,config)
    print 'done'

def makeSkin(_skinPath,config):
    skinName = os.path.basename(_skinPath)
    skinPath = os.path.dirname(_skinPath)
    cmd = 'sh '+skinPath+'/makeskin.sh '+skinName+' all '+CUR_DIR
    print 'makeskin ' + skinPath
    os.system(cmd)

def copyRes(config):
    # copy
    fromPath = CUR_DIR+'/publish'
    checkPath(fromPath)
    print 'publish path='+fromPath
    print 'copy res to games/hall'
    hallPath = config['hallPath']
    if os.path.exists(CUR_DIR+'/games/hall'):
        shutil.rmtree(CUR_DIR+'/games/hall')

    if  os.path.exists(fromPath):
        replaceFolder(fromPath+'/common',CUR_DIR+'/games/common')
        replaceFolder(fromPath+'/hall/ccbi',hallPath+'ccbi')
        replaceFolder(fromPath+'/hall/img',hallPath+'img')

    cpcmd = 'cp '+fromPath+'/hall/config/hall_ui_config.json '+hallPath+'/config/hall_ui_config.json'
    os.system(cpcmd)

    print 'copy res to player'
    shutil.copytree(hallPath, CUR_DIR+'/games/hall')
    playerGamePath = os.path.join(CUR_DIR, "player.app", "Contents", "Resources", "games")
    if os.path.exists(playerGamePath+"/hall"):
        shutil.rmtree(playerGamePath+"/hall")
    shutil.copytree(hallPath, playerGamePath+"/hall")
    if os.path.exists(playerGamePath+"/common"):
        shutil.rmtree(playerGamePath+"/common")
    shutil.copytree(fromPath+'/common', playerGamePath+"/common")

def checkPath(cPath):
    if not os.path.exists(cPath):
        print cPath, ' not exists, please check.....'
        # 结束进程
        sys.exit()

def work(curPath,skinPath):

    configPath = os.path.join(curPath, "player_config.json")
    config = json.load(file(configPath))
    # fixPathInConfig(curPath, config)

    print "playerPath", config['playerPath']

    if os.path.exists(skinPath):
        makeSkin(skinPath,config)

    copyRes(config)
    # makePlayer(config)

def fixPathInConfig(CUR_DIR, config):
    """修复配置中的路径
    """
    # playerPath
    if not os.path.isabs(config['playerPath']):
        config['playerPath'] = os.path.realpath(os.path.join(CUR_DIR, config['playerPath']))
        print config['playerPath']


def printUsage():
    """输出用法
    """
    print "用法:"
    print "python player_utils.py <skin-full-path>"
    print "skin-full-path: 皮肤路径"


if __name__ == '__main__':
    curFilePath = os.path.realpath(__file__)
    CUR_DIR = os.path.dirname(curFilePath)
    print "CUR_DIR", CUR_DIR

    skinPath = ''
    if len(sys.argv) >= 2:
        skinPath = sys.argv[1]
        print 'skin  path: '+skinPath

    work(CUR_DIR,skinPath)
