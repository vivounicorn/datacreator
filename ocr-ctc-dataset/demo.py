#coding:utf-8
import tools.chinese_creator as cc 
import time
import os

def dict_creator():
    base_dir = "./mapping-out/"
    sub_dir = str(int(time.time())) + "/"
    csvfile = "label.csv"
    dictfile = "encoding.dict"
  
    if not os.path.isdir(base_dir):
        os.mkdir(base_dir)
    if not os.path.isdir(base_dir + sub_dir):    
        os.mkdir(base_dir + sub_dir)
    if not os.path.isdir(base_dir + sub_dir + "image"):    
        os.mkdir(base_dir + sub_dir + "image") 
    return base_dir + sub_dir + "image", base_dir + sub_dir + csvfile, base_dir + sub_dir + dictfile 

if __name__ == '__main__':
    outputFilePath, csvFilename, dictFileName  = dict_creator() 
    font_path = "./fonts_chinese"
    background_path = "./background" 
    textFilePath ="./base-corpus"
    cc.generateNormalWords(dictFileName, font_path, background_path, csvFilename, textFilePath, outputFilePath, 10) 
