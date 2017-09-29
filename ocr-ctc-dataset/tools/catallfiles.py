
import os
import codecs
import chardet

font_dir = os.walk('../data')

with codecs.open('a.files', 'w', encoding='utf-8') as af:
    for root, dirs, files in font_dir:
        for f in files:
            print root+"/"+f
            fname = root+"/"+f

            with codecs.open(fname, 'r') as f:
                try: 
                    for line in f:
                        af.write(line.decode('utf-8'))
                except:
                    print "coding=%s,filename=%s" %(str(chardet.detect(line)), fname)


