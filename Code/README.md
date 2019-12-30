#  Transportation Mobility Factor Extraction Using Image Recognition Techniques 

## Our paper: https://saki.siit.tu.ac.th/stud2019/uploads_final/115__7a3d1d8a58b34f2425f394556c789d6a/Transportation-Mobility-Kantavat.pdf

## Citing

If you find this repository useful, please consider citing it using a link to the repo :)

### Original Code from (Credited to) https://github.com/wizyoung/YOLOv3_TensorFlow

### 1. Requirements

This project has the following dependencies:

- Numpy `sudo pip install numpy`

- OpenCV Python `sudo apt-get install python-opencv`

- TensorFlow `sudo pip install --upgrade tensorflow-gpu (>=1.8.0)`

### 2. How to run (Running demos)

```shell
python test_single_image.py ../CorpusBS/image_43_0065.jpg
python test_single_image.py ../CorpusBS/image_43_0373.jpg
```

### 2. Weights Convertion

The pretrained darknet weights file can be downloaded [here](https://pjreddie.com/media/files/yolov3.weights). Place this weights file under directory `./data/darknet_weights/` and then run:

```shell
python convert_weight.py
```

Then the converted TensorFlow checkpoint file will be saved to `./data/darknet_weights/` directory.

You can also download the converted TensorFlow checkpoint file by me via [[Google Drive link](https://drive.google.com/drive/folders/1mXbNgNxyXPi7JNsnBaxEv1-nWr7SVoQt?usp=sharing)] or [[Github Release](https://github.com/wizyoung/YOLOv3_TensorFlow/releases/)] and then place it to the same directory.

### 3. Model architecture

For better understanding of the model architecture, you can refer to the following picture. With great thanks to [Levio](https://blog.csdn.net/leviopku/article/details/82660381) for your excellent work!

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/docs/yolo_v3_architecture.png?raw=true)

### 4. Results

These are some **sample results** form our data set.

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/data/demo_data/results/dog.jpg?raw=true)

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/data/demo_data/results/messi.jpg?raw=true)

![](https://github.com/wizyoung/YOLOv3_TensorFlow/blob/master/data/demo_data/results/kite.jpg?raw=true)
