Code for the AAAI18 paper [PixelLink: Detecting Scene Text via Instance Segmentation](https://arxiv.org/abs/1801.01315), by Dan Deng, Haifeng Liu, Xuelong Li, and Deng Cai.

# Pixel Link python 3.6

Python 3.6 using 2to3-3.6 with some modifications.   
Used pip instead of conda

Note: this code still has a problem with optimization, loss can suddenly shoot to **nan**.   
Working with 2 GPUs, batch size per GPU 4. batch_size = 8
```
bash scripts/train.sh 0,1 4 &
```   
pixel conf = 0.8, link conf = 0.8, width = 512, height = 512 (training, based on paper)   
pixel conf = 0.5, link conf = 0.5, width = 512, height = 512 (inference)   
Training 8000 global steps: test some images, **no bbox found** (4001 - 8000 loss between 1.5 ~ 0.9).   
Training 12000 global steps: some bboxes appear (8001 - 12000 loss between 1.1 ~ 0.7).   
Training 16000 global steps: more bboxes appear, improved (12001 - 16000 loss between 1.1 ~ 0.6).   
During training, simply ignore this warning "Bounding box (148,1161,172,1224) is completely outside the image and will not be drawn."

Change config.py `oriented_bbox = True` to default (paper) bbox, `False` to straight bbox.

## Installation
### Clone the repo
```
git clone --recursive git@github.com:ZJULearning/pixel_link.git
```

Denote the root directory path of pixel_link by `${pixel_link_root}`. 

Add the path of `${pixel_link_root}/pylib/src` to your `PYTHONPATH`:
```
export PYTHONPATH=${pixel_link_root}/pylib/src:$PYTHONPATH
```

### Prerequisites
```
pip install -r requirements.txt
```

## Testing
### Download the pretrained model
* PixelLink + VGG16 4s [Baidu Netdisk](https://pan.baidu.com/s/1jsOc-cutC4GyF-wMMyj5-w) | [GoogleDrive](https://drive.google.com/file/d/19mlX5W8OBalSjhf5oTTS6qEq2eAU8Tg9/view?usp=sharing), trained on IC15
* PixelLink + VGG16 2s [Baidu Netdisk](https://pan.baidu.com/s/1asSFsRSgviU2GnvGt2lAUw) | [GoogleDrive](https://drive.google.com/file/d/1QleZxu_6PSI733G7wzbqeFtc8A3-LmWW/view?usp=sharing), trained on IC15

Unzip the downloaded model. It contains 4 files:

* config.py
* model.ckpt-xxx.data-00000-of-00001
* model.ckpt-xxx.index  
* model.ckpt-xxx.meta
Note: need to convert config.py to python 3.6

Denote their parent directory as `${model_path}`.

### Test on ICDAR2015
The reported results on ICDAR2015  are:

|Model|Recall|Precision|F-mean|
|---|---|---|---|
|PixelLink+VGG16 2s|82.0|85.5|83.7|
|PixelLink+VGG16 4s|81.7|82.9|82.3|

Suppose you have downloaded the [ICDAR2015 dataset](http://rrc.cvc.uab.es/?ch=4&com=downloads), execute the following commands to test the model on ICDAR2015:
```
cd ${pixel_link_root}
./scripts/test.sh ${GPU_ID} ${model_path}/model.ckpt-xxx ${path_to_icdar2015}/ch4_test_images
```
For example:
```
./scripts/test.sh 3 ~/temp/conv3_3/model.ckpt-38055 ~/dataset/ICDAR2015/Challenge4/ch4_test_images
```

The program will create a zip file of  detection results, which can be submitted to the ICDAR2015 server directly.
The detection results can be visualized via `scripts/vis.sh`.

Here are some samples:
![./samples/img_333_pred.jpg](./samples/img_333_pred.jpg)
![./samples/img_249_pred.jpg](./samples/img_249_pred.jpg)


### Test on any images
Put the images to be tested in a single directory, i.e., `${image_dir}`. Then:
```
cd ${pixel_link_root}
./scripts/test_any.sh ${GPU_ID} ${model_path}/model.ckpt-xxx ${image_dir}
./scripts/cpu.sh ${model_path}/model.ckpt-xxx ${image_dir}
```
For example:
```
 ./scripts/test_any.sh 3 ~/temp/conv3_3/model.ckpt-38055 ~/dataset/ICDAR2015/Challenge4/ch4_training_images
```

The program will visualize the detection results directly on images.   If the detection result is not satisfying, try to:

1. Adjust the inference parameters like `eval_image_width`, `eval_image_height`, `pixel_conf_threshold`, `link_conf_threshold`.
2. Or train your own model.

## Training
### Converting the dataset to tfrecords files
Scripts for converting ICDAR2015 and SynthText datasets have been provided in the `datasets` directory.
 It not hard to write a converting script  for your own dataset.

### Train your own model

* Modify `scripts/train.sh` to configure your dataset name and dataset path like:
```
DATASET=icdar2015
DATASET_DIR=$HOME/dataset/pixel_link/icdar2015
```
* Start training
```
./scripts/train.sh ${GPU_IDs} ${IMG_PER_GPU}
```
For example, `./scripts/train.sh 0,1,2 8`. 

The existing training strategy in `scripts/train.sh` is configured for icdar2015, modify it if necessary.  A lot of training or model options  are available in `config.py`, try it yourself if you are interested.

## Acknowlegement
![](http://www.cad.zju.edu.cn/templets/default/imgzd/logo.jpg)
![](http://www.cvte.com/images/logo.png)
