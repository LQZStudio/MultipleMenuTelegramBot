#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:51:19 2019

@author: angelozinna
"""
#prova
import json
import config as cfg
def printReadableJson(path):
    data=readJsonFile(path)
    data=json.dumps(data, indent=4)  
    print(data)
    
def readJsonFile(path):
    with open(path) as json_file:  
        data = json.load(json_file)
        #print (data)
    return data
    
def writeJsonFile(path,data):
    with open(path, 'w+') as outfile:  
        json.dump(data, outfile)
def searchLangOfChatId(chat_id):
    chat_id=str(chat_id)
    data1=readJsonFile(cfg.PATH_PREF)
    for ids in data1.keys():
        if(ids == chat_id):
            return data1[chat_id]["language"]
    return None
           
def addUserJsonFile(chat_id,lang):
    chat_id=str(chat_id)
    flag=0
    data1=readJsonFile(cfg.PATH_PREF)
    for ids in data1.keys():
        if(ids == chat_id):
            flag=1
            if(data1[chat_id]["language"]!=lang):
                obj={"language": lang}
                data1[chat_id].update(obj)
                writeJsonFile(cfg.PATH_PREF,data1)
    
    if(flag==0):
        data1[chat_id]={}
        data1[chat_id]["language"]=lang
        writeJsonFile(cfg.PATH_PREF,data1)


def createCompactDictJson():
    data=readJsonFile(cfg.PATH_DICT_READABLE)
    writeJsonFile(cfg.PATH_DICT,data)
    
def getLanguageById(chat_id):
    data=readJsonFile(cfg.PATH_PREF)
    if chat_id in data.keys():
        return data[chat_id]["language"]
    else:
        return None
             
def getDictByLanguage(lang):
    data=readJsonFile(cfg.PATH_DICT)
    if lang in data.keys():
        return data[str(lang)]
    else:
        return None
    