import tensorflow as tf
import os
from PIL import Image
import numpy as np
import cv2

model_path = "./model/model.pb"
labels_path = "./model/labels.txt"
model_output_layer = 'loss:0'
model_input_node = 'Placeholder:0'


def convert_to_opencv(image):
    # RGB -> BGR
    image = image.convert('RGB')
    r,g,b = np.array(image).T
    opencv_image = np.array([b,g,r]).transpose()
    return opencv_image

def crop_center(img,cropx,cropy):
    h, w = img.shape[:2]
    startx = w//2-(cropx//2)
    starty = h//2-(cropy//2)
    return img[starty:starty+cropy, startx:startx+cropx]

def resize_down_to_1600_max_dim(image):
    h, w = image.shape[:2]
    if (h < 1600 and w < 1600):
        return image

    new_size = (1600 * w // h, 1600) if (h > w) else (1600, 1600 * h // w)
    return cv2.resize(image, new_size, interpolation = cv2.INTER_LINEAR)

def resize_to_256_square(image):
    h, w = image.shape[:2]
    return cv2.resize(image, (256, 256), interpolation = cv2.INTER_LINEAR)

def update_orientation(image):
    exif_orientation_tag = 0x0112
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if (exif != None and exif_orientation_tag in exif):
            orientation = exif.get(exif_orientation_tag, 1)
            # orientation is 1 based, shift to zero based and flip/transpose based on 0-based values
            orientation -= 1
            if orientation >= 4:
                image = image.transpose(Image.TRANSPOSE)
            if orientation == 2 or orientation == 3 or orientation == 6 or orientation == 7:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            if orientation == 1 or orientation == 2 or orientation == 5 or orientation == 6:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return image



def classify_image(image):
    graph_def = tf.compat.v1.GraphDef()
    labels = []

    # Import the TF graph
    with tf.io.gfile.GFile(model_path, 'rb') as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    # Create a list of labels.
    with open(labels_path, 'rt') as lf:
        for l in lf:
            labels.append(l.strip())

    # Update orientation based on EXIF tags, if the file has orientation info.
    image = update_orientation(image)

    image = convert_to_opencv(image)
    image = resize_down_to_1600_max_dim(image) 
    # We next get the largest center square
    h, w = image.shape[:2]
    min_dim = min(w,h)
    max_square_image = crop_center(image, min_dim, min_dim)
    augmented_image = resize_to_256_square(max_square_image)
    # Get the input size of the model
    with tf.compat.v1.Session() as sess:
        input_tensor_shape = sess.graph.get_tensor_by_name('Placeholder:0').shape.as_list()
    network_input_size = input_tensor_shape[1]

    # Crop the center for the specified network_input_Size
    augmented_image = crop_center(augmented_image, network_input_size, network_input_size)

    with tf.compat.v1.Session() as sess:
        try:
            prob_tensor = sess.graph.get_tensor_by_name(model_output_layer)
            predictions = sess.run(prob_tensor, {model_input_node: [augmented_image] })
        except KeyError:
            print ("Couldn't find classification output layer: " + model_output_layer + ".")
            print ("Verify this a model exported from an Object Detection project.")
            exit(-1)

        #highest_probability_index = np.argmax(predictions)
        #print('Classified as: ' + labels[highest_probability_index])
        #print()

        # Or you can print out all of the results mapping labels to probabilities.
        label_index = 0

        return dict(zip([l.lower() for l in labels], [np.float64(np.round(p,3)) for p in predictions[0]])) 