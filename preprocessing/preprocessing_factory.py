# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Contains a factory for building various models."""





import tensorflow as tf

from preprocessing import ssd_vgg_preprocessing

slim = tf.contrib.slim


def get_preprocessing(is_training=False):
    """Returns preprocessing_fn(image, height, width, **kwargs).

    Args:
      name: The name of the preprocessing function.
      is_training: `True` if the model is being used for training.

    Returns:
      preprocessing_fn: A function that preprocessing a single image (pre-batch).
        It has the following signature:
          image = preprocessing_fn(image, output_height, output_width, ...).

    Raises:
      ValueError: If Preprocessing `name` is not recognized.
    """


    def preprocessing_fn(image, labels, bboxes, xs, ys, 
                         out_shape, data_format='NHWC', **kwargs):
        return ssd_vgg_preprocessing.preprocess_image(
            image, labels, bboxes, out_shape, xs, ys, data_format=data_format,
            is_training=is_training, **kwargs)
    return preprocessing_fn
