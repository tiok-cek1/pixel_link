set -x
set -e

TRAIN_DIR=${HOME}/models/pixel_link

#DATASET=synthtext
#DATASET_PATH=SynthText

DATASET=icdar2015
DATASET_DIR=${HOME}/dataset/pixel_link/ICDAR

python train_pixel_link.py \
            --train_dir=${TRAIN_DIR} \
            --learning_rate=1e-3\
            --train_image_width=512 \
            --train_image_height=512 \
            --batch_size=1\
            --dataset_dir=${DATASET_DIR} \
            --dataset_name=${DATASET} \
            --dataset_split_name=train \
            --max_number_of_steps=100\
            --checkpoint_path=${CKPT_PATH} \
            --using_moving_average=1

python train_pixel_link.py \
            --train_dir=${TRAIN_DIR} \
            --learning_rate=1e-2\
            --train_image_width=512 \
            --train_image_height=512 \
            --batch_size=1\
            --dataset_dir=${DATASET_DIR} \
            --dataset_name=${DATASET} \
            --dataset_split_name=train \
            --checkpoint_path=${CKPT_PATH} \
            --using_moving_average=1\
            2>&1 | tee -a ${TRAIN_DIR}/log.log                        

