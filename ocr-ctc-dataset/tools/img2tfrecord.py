import tensorflow as tf

import os
import sys
import glob
from utils import _get_output_filename,int64_feature,bytes_feature
import tools.terminal_color as tc 


def img2tfrecord(image_dir, label_path, output_path, debug=False):
    """

    :param image_dir: image_dir just like "****/****/*.jpg"
    :param label_path: image pathlabeltext
    :param output_path: output path
    :return: NULL
    """

    tf_filename = _get_output_filename(output_path)
    labels = []
    indexs = []
    imgLists = os.listdir(image_dir)
    with open(label_path) as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            sline = line.split('')
            if len(sline) <> 3:
                if debug == True:
                    print tc.UseStyle("[WARN] length of label file is invalid.length=%d" % (len(sline)), fore='red')
                continue
            indexs.append(sline[0])
            labels.append(sline[1])

    image_format = b'JPEG'
    with tf.python_io.TFRecordWriter(tf_filename) as tfrecord_writer:
        for i, filename in enumerate(indexs):
            sys.stdout.write('\r>> Converting image %d/%d' % (i + 1, len(imgLists)))
            sys.stdout.flush()
            image_data = tf.gfile.FastGFile(image_dir + "/" + filename, 'rb').read()

            example = tf.train.Example(features=tf.train.Features(feature={"label": bytes_feature(labels[i]),
                                                                           "image/encoded": bytes_feature(image_data),
                                                                           'image/format': bytes_feature(image_format)}))
            tfrecord_writer.write(example.SerializeToString())
    print('\nFinished converting the dataset!')
