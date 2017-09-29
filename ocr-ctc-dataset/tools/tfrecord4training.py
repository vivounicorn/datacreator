#coding=utf-8
import tensorflow as tf
from PIL import Image
import numpy as np

def read_and_decode(filename, hresize=0, wresize=0, num_epochs=1):  # read iris_contact.tfrecords
    filename_queue = tf.train.string_input_producer(
        [filename], num_epochs=num_epochs)
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)  # return file_name and file
    
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           "label": tf.FixedLenFeature([], tf.string),
                                           "label_length": tf.FixedLenFeature([], tf.int64),
                                           "image_width": tf.FixedLenFeature([], tf.int64),
                                           "image_height": tf.FixedLenFeature([], tf.int64),
                                           "image_raw": tf.FixedLenFeature([], tf.string)
                                       })  # return image and label


    width = tf.cast(features['image_width'], tf.int32)
    height = tf.cast(features['image_height'], tf.int32)

    img = tf.decode_raw(features['image_raw'], tf.uint8)
    img = tf.reshape(img, [height, width, 3]) 
    #img = tf.cast(img, tf.float32) * (1. / 255) - 0.5  # throw img tensor
    label = features['label']  # throw label tensor
    length = tf.cast(features["label_length"], tf.int64)
   
    if hresize <> 0 or wresize <> 0: 
        if hresize <> 0 and wresize <> 0:
            wresize = tf.fill([], value=wresize)
            hresize = tf.fill([], value=hresize)
        elif hresize <> 0 and  wresize == 0:
            hresize = tf.fill([], value=hresize)
            wresize = width
        elif wresize <> 0 and hresize == 0:
            wresize = tf.fill([], value=wresize)
            hresize = height
         
        resized_image = tf.image.resize_images(img,(hresize,wresize),method=3)#tf.image.resize_image_with_crop_or_pad(img,hresize,wresize)
        #resized_image = tf.image.resize_image_with_crop_or_pad(img,hresize,wresize)
        #img = tf.cast(img, tf.float32) * (1. / 255) - 0.5  # throw img tensor
        return wresize, hresize, label, length, resized_image
    else:
        return width, height, label, length, img

def batch_inputs(filename, hresize=0, wresize=0, num_epochs=1):
    if not num_epochs: 
        num_epochs = None

    img_width, img_height, img_label, img_label_len, img_raw = read_and_decode(filename,hresize, wresize, num_epochs)
    init_op = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())

    with tf.Session() as sess:
        sess.run(init_op)
        coord=tf.train.Coordinator()
        threads=tf.train.start_queue_runners(coord=coord)
        
        for i in xrange(20):
            width, height, label, label_len, image_raw = sess.run([img_width, img_height, img_label, img_label_len, img_raw])
            print image_raw[:,:,:].shape
            print type(image_raw),image_raw.astype(np.uint8) 
            imm=Image.fromarray(image_raw.astype(np.uint8))
            imm.save('tmp/'+str(i) + '1.jpg')

        coord.request_stop()
        coord.join(threads)
        
def inputs(batch_size, num_epochs, filename):
    if not num_epochs: num_epochs = None
    with tf.name_scope('input'):
        # Even when reading in multiple threads, share the filename
        # queue.
        img, label, length = read_and_decode(filename, num_epochs)

        # Shuffle the examples and collect them into batch_size batches.
        # (Internally uses a RandomShuffleQueue.)
        # We run this in two threads to avoid being a bottleneck.
        sh_images, sh_labels, sh_length = tf.train.shuffle_batch(
            [img, label, length], batch_size=batch_size, num_threads=2,
            capacity=1000 + 3 * batch_size,
            # Ensures a minimum amount of shuffling of examples.
            min_after_dequeue=100)

        return sh_images, sh_labels, sh_length

def preprocess_for_train(image,label ,scope='crnn_preprocessing_train'):
    """Preprocesses the given image for training.
    """
    with tf.name_scope(scope, 'ssd_preprocessing_train', [image]):
        if image.get_shape().ndims != 3:
            raise ValueError('Input must be of size [height, width, C>0]')
        if image.dtype != tf.float32:
            image = tf.image.convert_image_dtype(image, dtype=tf.float32)# convert image as a tf.float32 tensor
            image_s = tf.expand_dims(image, 0)
            tf.summary.image("image",image_s)

        image = tf.image.rgb_to_grayscale(image)
        tf.summary.image("gray",image)
        return image, label
