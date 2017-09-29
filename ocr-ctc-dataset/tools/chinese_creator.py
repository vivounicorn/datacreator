#coding:utf-8
import Image, ImageDraw, ImageFont
import random
import os
import codecs
import time
import tools.terminal_color as tc
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class parameterWrap:
    font_name = ""
    font = object()
    csvfile = object()
    image_path = ""
    outputFilePath = ""
   
    def __init__(self, n, f, i, o, c):
        self.font_name = n
        self.font = f 
        self.image_path = i
        self.outputFilePath = o
        self.csvfile = c

def fontsCount(path):
    
    fonts = 0
    font_dir = os.walk(path)

    for root, dirs, files in font_dir:
        for f in files:
            fonts = fonts + 1

    print "fonts",fonts
    return fonts

def dumpDict(dic, fname):
    os.remove(fname)
    if not os.path.isfile(fname):
        os.system(r'touch %s' % fname)
    if not os.path.isfile(fname+".reverse"):
        os.system(r'touch %s' % fname+".reverse")
   
    itms = sorted(dic.items(), key=lambda d: d[1])  
    with codecs.open(fname, 'w', encoding='utf-8') as f:
        for (k,v) in itms:
            if not isinstance(k, str) or not isinstance(v, int):
                if debug == True:
                    print tc.UseStyle("[WARN] key or value of dictionary is invalid.key=%s,value=%s" % (k, str(v)), fore='red')
                continue
            f.write('%s%d\n' % (k.decode('utf-8'), v))
    with codecs.open(fname+".reverse", 'w', encoding='utf-8') as f:
        for (k,v) in itms:
            if not isinstance(k, str) or not isinstance(v, int):
                if debug == True:
                    print tc.UseStyle("[WARN] key or value of dictionary is invalid.key=%s,value=%s" % (k, str(v)), fore='red')
                continue
            f.write('%d%s\n' % (v, k.decode('utf-8')))

def loadDict(fname):
    if not os.path.isfile(fname):
        print tc.UseStyle("[ERROR] the dictionary file is not exists.", fore='red')
        return False
    dic = {}
    with codecs.open(fname, 'r') as f:
        for line in f:
            sline = line.split('')
            if len(sline) <> 2: 
                if debug == True:
                    print tc.UseStyle("[WARN] length of dictionary item is invalid.", fore='red')
                continue
            try:
                key = sline[0].encode('utf-8')
                value = int(sline[1])
            except:
                if debug == True:
                    print tc.UseStyle("[WARN] the format of dictionary item is invalid.", fore='red')
                continue
            if dic.has_key(key):
                if debug == True:
                    print tc.UseStyle("[WARN] dictionary key is conflict. key=%s, old value=%s, new value" % (key, dic[key], value), fore='red')
                continue
            dic[key] = value

    return dic

def stringDicCoding(dic, line):
    # the coding of line is utf-8.
    if len(dic) == 0:
        print tc.UseStyle("[ERROR] the dictionary is empty.", fore='red')
        return False, ""
    
    lst = []
    for i in list(line.decode('utf-8')):
        if not dic.has_key(i.encode('utf-8')):
            if debug == True:
                print tc.UseStyle("[WARN] the key is not exist.key=%s" % i, fore='yellow')
            lst.append(0)

        lst.append(dic[i.encode('utf-8')])
  
    return True, ','.join(str(v) for v in lst)


def drawText(dic, split_str, index, prs, mode="n", debug=False): 
    ttfont = prs.font
    image_path = prs.image_path
    outputFilePath = prs.outputFilePath

    im = Image.open(image_path).convert('RGB')
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    filename = ""
    draw = ImageDraw.Draw(im)
    if split_str == "":
        print tc.UseStyle("[ERROR] string is empty.", fore='red')
        return filename
    if not isinstance(index, list) or len(index) != 1 or not isinstance(index[0], int):
        print tc.UseStyle("[ERROR] index type of length is invalid.", fore='red')
        return filename
    if debug == True:
        print tc.UseStyle("mode=%s, new text=%s, color of it = (%s, %s, %s)" % (mode, split_str, r, g, b), fore='green')
    if mode == "n":
        try:
            draw.text((12, 14), split_str.decode('utf-8'), fill=(r, g, b), font=ttfont)
            t_width, t_height = draw.textsize(unicode(split_str, 'utf-8'), font=ttfont)

            rX = 16 + t_width
            rY = 24 + t_height
 
            box = (8, 12, rX, rY)
            alpha = random.randint(20, 160)
        except:
            import chardet
            print tc.UseStyle("[ERROR]:original string:%s, coding:%s" % (split_str, chardet.detect(split_str)), fore='red')
            return filename
    if mode == "v":
        try:
            draw.text((50, 50), split_str.decode('utf-8'), fill=(r, g, b), font=ttfont)
            t_width, t_height = draw.textsize(unicode(split_str, 'utf-8'), font=ttfont)

            rX = 58 + t_width
            rY = 67 + t_height
            vwidth = random.randint(-10, 10);
            vheight = random.randint(-10, 10);

            box = (39+vwidth, 40+vheight, rX+vwidth, rY+vheight)
        except:
            import chardet
            print tc.UseStyle("[ERROR]:original string:%s, coding:%s" % (split_str, chardet.detect(split_str)), fore='red')
            return filename
 
    if mode == "w":
        try:
            watermark = Image.new("RGBA", im.size)
            draw = ImageDraw.ImageDraw(watermark, "RGBA")
            draw.text((12, 12), split_str.decode('utf-8'), fill=(r, g, b), font=ttfont)
            t_width, t_height = draw.textsize(unicode(split_str, 'utf-8'), font=ttfont)

            rX = 16 + t_width
            rY = 24 + t_height

            box = (8, 12, rX, rY)
            alpha = random.randint(20, 160)

            watermask = watermark.convert("L").point(lambda x: min(x, alpha))
            watermark.putalpha(watermask)

            im.paste(watermark, None, watermark)
        except:
            import chardet
            print tc.UseStyle("[ERROR]:original string:%s, coding:%s" % (split_str, chardet.detect(split_str)), fore='red')
            return filename

    region = im.crop(box)
   
    filename = 'image-' + str(index[0]) + '-' + str(int(time.time())) + '-' + prs.font_name + '.jpg'
    region.save(outputFilePath+"/"+filename)

    index[0] = index[0] + 1
    try:
        flag, conv = stringDicCoding(dic, split_str)
        if not flag:
            print tc.UseStyle("[ERROR]:dictionary is empty.", fore='red')
            return filename

        prs.csvfile.write('%s%s%s\n' % (filename, conv, split_str.decode('utf-8') ))
    except Exception, e:
        print repr(e)
        import chardet
        print tc.UseStyle("[ERROR]:csvfile riginal string:%s, coding:%s" % (split_str, chardet.detect(split_str)), fore='red')

    return filename
 
def generateNormalWords(dictPath='',
                        fontsPath='',
                        backgroundFilePath='', 
                        csvFilename='none.csv', 
                        textFilePath='', 
                        outputFilePath='none', 
                        iterators=100,
                        debug=False):
    '''
        Create text image with text files.

        ARGS:
            dictPath		: the path of dictionary
            fontsPath		: the path of fonts file
            backgroundFilePath	: the path of background image
	    csvFilename		: mapping file of text and image
	    textFilePath	: the path of text file for generating image
            outputFilePath	: the path of gennerated image		 
            debug		: whether debug
    '''
    if not os.path.isfile(dictPath):
        os.system(r'touch %s' % dictPath)
        print tc.UseStyle("[WARN]the path of dictionary file is not exists.", fore='yellow')
    if not os.path.isdir(fontsPath):
        print tc.UseStyle("the path of fonts file is not exists.path=%s" % fontsPath, fore='red')
        return False
    if not os.path.isdir(backgroundFilePath):
        print tc.UseStyle("the path of background image is not exists.path=%s" % backgroundFilePath, fore='red')
        return False
    if not os.path.isdir(textFilePath):
        print tc.UseStyle("the path of text file for generating image is not exist.path=%s" % textFilePath, fore='red')
        return False
    if not os.path.isdir(outputFilePath):
        os.mkdir(outputFilePath)  
        print tc.UseStyle("the path of gennerated image is created:%s." % (outputFilePath), fore='yellow')

    index = [0]
    idx = 1
    fonts = fontsCount(fontsPath)
    dic = loadDict(dictPath)

    with codecs.open(csvFilename, 'w', encoding='utf-8') as csvfile:
        csvfile.write('%s%s%s\n' % ('image', 'label', 'text'))
        cnt = 0
        while (cnt < iterators):
            cnt = cnt + 1
            list_dir = os.walk(backgroundFilePath)
            for back_root, _, back_fs in list_dir:
                for file in back_fs:
                    image_path = os.path.join(back_root, file)
                    print "background image path = %s." % (image_path)
                    im = Image.open(image_path)
                    width, height = im.size
                    print "background image info: im.size=%s, width=%s, height=%s, im.mode=%s." % (im.size, width, height, im.mode)
                    imgString = ''
                    font = random.randint(1, fonts)
                    font_select = 1
                    font_dir = os.walk(fontsPath)

                    path = ""
                    fname = ""

                    for font_root, _, files in font_dir:
                        for f in files:
                            if(font_select == font):
                                path = os.path.join(font_root, f)
                                fname = f
                                print "font=%s, path=%s" % (font, path)
                                break
                            font_select = font_select + 1
  
                    ttfont = ImageFont.truetype(path, 30)

                    prs = parameterWrap(fname[:fname.find('.')], ttfont, image_path, outputFilePath, csvfile) 
                    text_dir = os.walk(textFilePath)
                    for text_root, _, files in text_dir:
                        for sfile in files:
                            spath = text_root + "/" + sfile
                            with open(spath) as f:
                                for line in f:
                                    sline = line.strip()
                                    try:
                                        seed = len(sline.decode('utf-8'))
                                        # to build dictionary, do not deal with multi-thread.
                                        for i in list(sline.decode('utf-8')):
                                            if dic.has_key(i.encode('utf-8')):
                                                if debug == True:
                                                    print tc.UseStyle("[INFO] the key has exist. key=%s" % (i.encode('utf-8')), fore='yellow')
                                                continue
                                            dic[i.encode('utf-8')] = idx
                                            idx = idx + 1
                                    except:
                                        import chardet
                                        print tc.UseStyle("[ERROR] line string:%s, coding:%s" % (sline, chardet.detect(sline)), fore='red')
                                        seed = 0
                                    
                                    length = random.randint(1,30)
                                    while length < seed:
                                        myline = sline.decode('utf-8')[0:length].encode('utf-8')
                                        sline = sline.decode('utf-8')[length:].encode('utf-8')
                                        seed = len(sline.decode('utf-8'))
                                        length = random.randint(1,30)
                                        if index[0] % 1000 >= 2 and index[0] % 1000 <= 5:
                                            print tc.UseStyle("[INFO] We have creating %d images and dumpping dictionary at path=%s" % (index[0], dictPath), fore='green')
                                            dumpDict(dic, dictPath)

					drawText(dic, myline, index, prs, mode='w')
                                        drawText(dic, myline, index, prs, mode='v')
                                        drawText(dic, myline, index, prs, mode='n')
                                        
                                    if length >= seed:
                                        drawText(dic, sline, index, prs, mode="w")
                                        drawText(dic, sline, index, prs, mode='v')
                                        drawText(dic, sline, index, prs, mode='n')
                  
                                    
    dumpDict(dic, dictPath)

