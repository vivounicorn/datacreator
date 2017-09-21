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

def drawText(split_str, index, prs, mode="n"): 
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
        prs.csvfile.write('%s %s\n' % (filename, split_str.decode('utf-8')))
    except:
        import chardet
        print tc.UseStyle("[ERROR]:csvfile riginal string:%s, coding:%s" % (split_str, chardet.detect(split_str)), fore='red')

    return filename
 
def generateNormalWords(fontsPath='',
                        backgroundFilePath='', 
                        csvFilename='none.csv', 
                        textFilePath='', 
                        outputFilePath='none', 
                        iterators=100):
    '''
        Create text image with text files.

        ARGS:
            fontsPath		: the path of fonts file
            backgroundFilePath	: the path of background image
	    csvFilename		: mapping file of text and image
	    textFilePath	: the path of text file for generating image
            outputFilePath	: the path of gennerated image		 
    '''

    if not os.path.isdir(fontsPath):
        print "the path of fonts file is not exists."
        return False
    if not os.path.isdir(backgroundFilePath):
        print "the path of background image is not exists."
        return False
    if not os.path.isdir(textFilePath):
        print "the path of text file for generating image is not exist."
        return False
    if not os.path.isdir(outputFilePath):
        os.mkdir(outputFilePath)  
        print "the path of gennerated image is created:%s." % (outputFilePath)

    index = [0]
    fonts = fontsCount(fontsPath)

    with codecs.open(csvFilename, 'w', encoding='utf-8') as csvfile:
        csvfile.write('%s %s\n' % ('image', 'label'))
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
                                    except:
                                        import chardet
                                        print tc.UseStyle("[ERROR] line string:%s, coding:%s" % (sline, chardet.detect(sline)), fore='red')
                                        seed = 0

                                    if seed > 1:
                                        choice = random.randint(1, seed - 1)
                                        left_str = sline.decode('utf-8')[0:choice].encode('utf-8')
                                        right_str = sline.decode('utf-8')[choice:].encode('utf-8') 

                                        drawText(left_str, index, prs, mode="w")
                                        drawText(right_str, index, prs, mode='v')
                                        drawText(right_str, index, prs, mode='n')
                                    else:
					drawText(sline, index, prs, mode='w')
                                        drawText(sline, index, prs, mode='v')
                                        drawText(sline, index, prs, mode='n')

