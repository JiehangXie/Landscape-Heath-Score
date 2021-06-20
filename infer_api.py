# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import os
from collections import Counter
import yaml
from numpy import array,concatenate
import paddleseg.transforms as T
from paddle.inference import create_predictor, PrecisionType
from paddle.inference import Config as PredictConfig
from paddleseg.cvlibs import manager
from paddleseg.utils import get_sys_env, logger
from paddleseg.utils.visualize import get_pseudo_color_map
from cv2 import imread
from base64 import b64decode,b64encode
from io import BytesIO
import json
from Qscore_algorithm import cal_Q_score

#Initialization environment
env_info = get_sys_env()
use_gpu = True if env_info['Paddle compiled with cuda'] and env_info['GPUs used'] else False
batch_size = 1

class DeployConfig:
    def __init__(self, path):
        with codecs.open(path, 'r', 'utf-8') as file:
            self.dic = yaml.load(file, Loader=yaml.FullLoader)

        self._transforms = self._load_transforms(
            self.dic['Deploy']['transforms'])
        self._dir = os.path.dirname(path)

    @property
    def transforms(self):
        return self._transforms

    @property
    def model(self):
        return os.path.join(self._dir, self.dic['Deploy']['model'])

    @property
    def params(self):
        return os.path.join(self._dir, self.dic['Deploy']['params'])

    def _load_transforms(self, t_list):
        com = manager.TRANSFORMS
        transforms = []
        for t in t_list:
            ctype = t.pop('type')
            transforms.append(com[ctype](**t))

        return T.Compose(transforms)

class Predictor:
    def __init__(self):
        self.cfg = DeployConfig('model/deploy.yaml')
        #self.args = args

        pred_cfg = PredictConfig(self.cfg.model, self.cfg.params)
        pred_cfg.disable_glog_info()
        if use_gpu:
            pred_cfg.enable_use_gpu(100, 0)
            ptype = PrecisionType.Float32

        self.predictor = create_predictor(pred_cfg)

    def preprocess(self, img):
        return self.cfg.transforms(img)[0]

    def run(self, imgs):
        if not isinstance(imgs, (list, tuple)):
            imgs = [imgs]

        num = len(imgs)
        input_names = self.predictor.get_input_names()
        input_handle = self.predictor.get_input_handle(input_names[0])
        results = []

        for i in range(0, num, batch_size):
            data = array([
                self.preprocess(img) for img in imgs[i:i + batch_size]
            ])
            input_handle.reshape(data.shape)
            input_handle.copy_from_cpu(data)
            self.predictor.run()

            output_names = self.predictor.get_output_names()
            output_handle = self.predictor.get_output_handle(output_names[0])
            results.append(output_handle.copy_to_cpu())

        result = self.postprocess(results, imgs)
        return result

    def postprocess(self, results, imgs):

        results = concatenate(results, axis=0)
        for i in range(results.shape[0]):
            result = results[i]

            #统计像素比例
            pix_count = dict(Counter(result.flatten()))
            pix_sum = sum(pix_count.values())

            cityscape_class = ['road','sidewalk','building',
                                'wall','fence','pole','traffic light',
                                'traffic sign','vegetation','terrain',
                                'sky','person','rider','car','truck',
                                'bus','train','motorcycle','bicycle']
            element_percentage = {
                'sky':0,
                'terrain':0,
                'vegetation':0,
                'pole':0,
                'fence':0,
                'wall':0,
                'building':0,
                'sidewalk':0,
                'road':0,
                'others':0
            }
            for c in range(0,len(cityscape_class)):
                try:
                    if element_percentage.__contains__(cityscape_class[c]):
                        element_percentage[cityscape_class[c]]=pix_count[c]/pix_sum
                    else:
                        element_percentage['others'] += pix_count[c]/pix_sum
                except:pass
            
            #Green index
            GLR = round(element_percentage['vegetation']+element_percentage['terrain'],2)
            #Q_score
            Q_score = json.dumps(cal_Q_score(element_percentage))
            #dict2json
            element_percentage = json.dumps(element_percentage)
            #Generating color
            result = get_pseudo_color_map(result)
            result = result.convert('RGB')
            #Save pictures temporarily
            buffered = BytesIO()
            result.save(buffered, format="JPEG")
            result = b64encode(buffered.getvalue()).decode('utf-8')

            return element_percentage,result,Q_score,GLR

def get_images(image_path, support_ext=".jpg|.jpeg|.png"):
    if not os.path.exists(image_path):
        raise Exception(f"Image path {image_path} invalid")

    if os.path.isfile(image_path):
        return [image_path]

    imgs = []
    for item in os.listdir(image_path):
        ext = os.path.splitext(item)[1][1:].strip().lower()
        if (len(ext) > 0 and ext in support_ext):
            item_path = os.path.join(image_path, item)
            imgs.append(item_path)
    return imgs

def seg_photo(image_path):
    predictor = Predictor()
    result = predictor.run(get_images(image_path))
    return result

def seg_api(image_base64):
    image_post = b64decode(image_base64)

    if not os.path.exists('./tmp'): os.mkdir('./tmp')
    tmp_file = './tmp/tmp.jpg'
    with open(tmp_file,'wb') as f:
        f.write(image_post)
    seg_result = seg_photo(tmp_file)
    os.unlink(tmp_file)
    return seg_result