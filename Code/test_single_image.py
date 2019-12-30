# coding: utf-8

from __future__ import division, print_function
## ------------------------ ##

'''
export PATH="/home/kaochula/anaconda3/bin:$PATH"
source activate python3

python train.py --checkpoint_path=weights/GCN_Attention
python train.py 

export PATH="/home/kaochula/anaconda3/bin:$PATH"
source activate python3
cd '/home/kaochula/Music/MY_PROJECT/main/tf_slim_v2_september_19-2018' 
python train.py 

'''
#from __future__ import print_function

import tensorflow as tf
import numpy as np
import argparse
import cv2

from utils.misc_utils import parse_anchors, read_class_names
from utils.nms_utils import gpu_nms
from utils.plot_utils import get_color_table, plot_one_box
from utils.data_aug import letterbox_resize

from model import yolov3

parser = argparse.ArgumentParser(description="YOLO-V3 test single image test procedure.")
parser.add_argument("input_image", type=str,
                    help="The path of the input image.")
parser.add_argument("--anchor_path", type=str, default="./data/yolo_anchors.txt",
                    help="The path of the anchor txt file.")
parser.add_argument("--new_size", nargs='*', type=int, default=[416, 416],
                    help="Resize the input image with `new_size`, size format: [width, height]")
parser.add_argument("--letterbox_resize", type=lambda x: (str(x).lower() == 'true'), default=True,
                    help="Whether to use the letterbox resize.")
parser.add_argument("--class_name_path", type=str, default="./data/coco.names",
                    help="The path of the class names.")
parser.add_argument("--restore_path", type=str, default="./data/darknet_weights/yolov3.ckpt",
                    help="The path of the weights to restore.")
args = parser.parse_args()

args.anchors = parse_anchors(args.anchor_path)
args.classes = read_class_names(args.class_name_path)
args.num_class = len(args.classes)

color_table = get_color_table(args.num_class)

n = args.input_image

img_ori = cv2.imread(args.input_image)
name_input_img = str(args.input_image)
if args.letterbox_resize:
    img, resize_ratio, dw, dh = letterbox_resize(img_ori, args.new_size[0], args.new_size[1])
else:
    height_ori, width_ori = img_ori.shape[:2]
    img = cv2.resize(img_ori, tuple(args.new_size))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = np.asarray(img, np.float32)
img = img[np.newaxis, :] / 255.

with tf.Session() as sess:
    input_data = tf.placeholder(tf.float32, [1, args.new_size[1], args.new_size[0], 3], name='input_data')
    yolo_model = yolov3(args.num_class, args.anchors)
    with tf.variable_scope('yolov3'):
        pred_feature_maps = yolo_model.forward(input_data, False)
    pred_boxes, pred_confs, pred_probs = yolo_model.predict(pred_feature_maps)

    pred_scores = pred_confs * pred_probs

    boxes, scores, labels = gpu_nms(pred_boxes, pred_scores, args.num_class, max_boxes=200, score_thresh=0.3, nms_thresh=0.45)

    saver = tf.train.Saver()
    saver.restore(sess, args.restore_path)

    boxes_, scores_, labels_ = sess.run([boxes, scores, labels], feed_dict={input_data: img})

    # rescale the coordinates to the original image
    if args.letterbox_resize:
        boxes_[:, [0, 2]] = (boxes_[:, [0, 2]] - dw) / resize_ratio
        boxes_[:, [1, 3]] = (boxes_[:, [1, 3]] - dh) / resize_ratio
    else:
        boxes_[:, [0, 2]] *= (width_ori/float(args.new_size[0]))
        boxes_[:, [1, 3]] *= (height_ori/float(args.new_size[1]))

    print("box coords:")
    print(boxes_)
    print('*' * 30)
    print("scores:")
    print(scores_)
    print('*' * 30)
    print("labels:")
    print(labels_)

    l_results = []

    for i in range(len(boxes_)):
        x0, y0, x1, y1 = boxes_[i]
        plot_one_box(img_ori, [x0, y0, x1, y1], label=args.classes[labels_[i]] + ', {:.2f}%'.format(scores_[i] * 100), color=color_table[labels_[i]])
        l_results.append(args.classes[labels_[i]])

    #print("car",l_results.count('car'), "truck",l_results.count('truck'), "person",l_results.count('person'), "motorbike",l_results.count('motorbike'))

    # print("car, truck, person, motorbike")
    # print(l_results.count('car'),",",l_results.count('truck'),",",l_results.count('person'),",",l_results.count('motorbike'))

    #cv2.imshow('Detection result', img_ori)
    print("Save as >>", './results/result_'+str(name_input_img[13:]))
    cv2.imwrite('./results/result_'+str(name_input_img[13:]), img_ori)
    print("Done")

print("id, car, truck, person, motorbike")
print(n,",", l_results.count('car'),",",l_results.count('truck'),",",l_results.count('person'),",",l_results.count('motorbike'))

re = str(n)+","+str(l_results.count('car'))+","+str(l_results.count('truck'))+","+str(l_results.count('person'))+","+str(l_results.count('motorbike'))

f = open('result_detection_csv_v1.csv','a')
f.write(str(re)+"\n") #Give your csv text here.
f.close()
    #cv2.imwrite("detected-boxes.jpg", img)
    #cv2.waitKey(0)
