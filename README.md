<h1 align="center">Landscape-Health Score</h1>

![Functions](https://github.com/JiehangXie/Landscape-Heath-Score/raw/main/docs/microsoft-edge-beta_test.gif)

<h3 align="center"><a href="https://github.com/JiehangXie/Landscape-Heath-Score">English</a>  |  <a href="https://gitee.com/xiejiehang/Landscape-Heath-Score">简体中文</a></h3>

# Introduction
Landscape-Health Score (LHS) is an auxiliary evaluation tool based on Paddlepaddle framework. You can simply drag and drop image files to automatically analyze images and generate simple evaluation reports. The currently supported Bisenet and PSPNet models can realize the identification and segmentation of 9 kinds of environmental elements, and real-time statistics of the proportion of environmental elements, the green vision rate and the scores of 6 psychological indicators such as happy / relaxed / depressive / social / motivated / focused. 
# Navigation
- [Introduction](#introduction)
- [Navigation](#navigation)
- [Functions](#functions)
  - [1.Image segmentation](#1image-segmentation)
  - [2.Green vision rate calculation](#2green-vision-rate-calculation)
  - [3.Health benefit evaluation](#3health-benefit-evaluation)
- [Quick start](#quick-start)
  - [Requirements](#requirements)
    - [Basic requirement](#basic-requirement)
    - [Development environment](#development-environment)
  - [1.Run on Windows](#1run-on-windows)
  - [2.Run on Source Code](#2run-on-source-code)
    - [2.1 Install Python 3.7+](#21-install-python-37)
    - [2.2 Install Dependency Package](#22-install-dependency-package)
    - [2.3 Download Model](#23-download-model)
    - [2.4 Run](#24-run)
  - [Batch Processing](#batch-processing)
    - [API Description](#api-description)
    - [Curl](#curl)
    - [PHP](#php)
    - [Python](#python)
- [Others](#others)
  - [Structure](#structure)
  - [Model List](#model-list)
  - [License](#license)
  - [About us](#about-us)
  - [Thanks](#thanks)

# Functions

## 1.Image segmentation  
The image segmentation function is based on the principle of image semantic segmentation technology, using deep learning technology and Cityscapes data set training model, through the model to identify and classify pixels and count the area ratio of each element on the image.  
Currently, the environmental elements that support identification are：  
- [x] sky
- [x] terrain
- [x] vegetation
- [x] pole
- [x] fence
- [x] wall
- [x] building
- [x] sidewalk
- [x] road
- [ ] water
- [ ] hill/mountain
## 2.Green vision rate calculation
Green vision rate is one of the reference indicators of environmental greening evaluation. Traditional green vision rate is counted by using the principle of RGB value of image pixels, which is obviously affected by environmental factors. Based on deep learning technology, green plants in the image can be identified, and other interference factors (such as green clothes / billboards, etc.) can be eliminated, so as to achieve more accurate proportion calculation.
## 3.Health benefit evaluation
It supports the evaluation and analysis of six psychological dimensions such as happy / relaxed / depressive / social / motivated / focused for the input image. At present, the function is still in the research and testing stage, and the algorithm will continue to upgrade and iterate.  

# Quick start
## Requirements
### Basic requirement
* Windows10(Recommended)
* CPU Intel i5 or AMD equivalent processor 
* GPU RTX1060 6G and above configuration (optional) 
### Development environment 
* npm >= 7.15
* Vite 2
* VUE 3.0
## 1.Run on Windows
2021.08.03 - The stable version v1.0.1 optimized for windows has been released, [click here to download](https://github.com/JiehangXie/Landscape-Heath-Score/releases/tag/1.0.1)
> Usage: unzip directly, and then run "启动程序.exe" or "使用兼容模式运行.cmd". Bisenetv2 model is included by default.

## 2.Run on Source Code
### 2.1 Install Python 3.7+
### 2.2 Install Dependency Package
Press `Win+R` , enter `cmd`  
Enter `cd [LHS folder]`  
Enter `pip install -r requirement.txt`  
Wait patiently for the installation to complete.
### 2.3 Download Model
Go to [Model List](#model-list) to download and decompress package of the model,and copy all the files to the folder named `model`.We recommend downloading `BiSeNetv2` model.
### 2.4 Run
Press `Win+R`,enter `cmd`
Enter `cd [LHS folder]`  
Enter `python app.py` to run the program  
Open any browser except IE and enter`http://127.0.0.1:5000` to the operation interface.

## Batch Processing
In order to meet the requirements for batch processing of images, I added a http API, which can initiate POST requests through any codes while running the program.
### API Description
HTTP Method：POST  
Request URL：http://127.0.0.1:5000/api/v1/json  
Header:
|   Parameter   |   Value   |
|   :-----------   |   ---------------:   |
|   Content-Type   |   application/json   |

Request  Parameter:
|   Parameter   |   Type   |   Description   |
|   :----   |   -----:   |   -----------------------------------------:   |
| image | string | Image information, Base64 encoding, bytes type need to be converted to UTF-8 |

Return Parameter:
|   Parameter   |   Type  |   Description   |
| :--------- |   -----:   |   -------------------------:    |
| image      | string |   Base64 coding of image segmentation   |
| gvr        | double |   Green vision rate   |
| proportion |   json |   Proportion of environmental elements   |
| score      |   json | 6 dimensions of psychological index score  |

The following three request cases are provided: curl / PHP and python:  
### Curl
```
curl -i -k 'http://127.0.0.1:5000/api/v1/json' --data 'image=[Image Base64 encoding, need URLEncode]' -H 'Content-Type:application/x-www-form-urlencoded'
```
### PHP
```
<?php
function request_post($url = '', $param = '')
{
    if (empty($url) || empty($param)) {
        return false;
    }
    $postUrl = $url;
    $curlPost = $param;
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $postUrl);
    curl_setopt($curl, CURLOPT_HEADER, 0);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($curl, CURLOPT_POST, 1);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $curlPost);
    $data = curl_exec($curl);
    curl_close($curl);

    return $data;
}

$url = 'http://127.0.0.1:5000/api/v1/json';
$img = file_get_contents('[Image filepath]');
$img = base64_encode($img);
$bodys = array(
    'image' => $img
);
$res = request_post($url, $bodys);

var_dump($res);
```
### Python
```
import requests
import base64
import json

request_url = "http://127.0.0.1:5000/api/v1/json"
f = open('[Image filepath]', 'rb')
img = base64.b64encode(f.read()).decode('utf-8')

params = {'image':img}
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=json.dumps(params), headers=headers)
if response:
    print (response.json())
```
# Others
## Structure 
```
* requirement.txt  --list of dependent files
* app.py  --main program for app
* infer_api.py  --program for inference
* Qscore_algorithm.py  --program for calculating health scores
* dist --front-end program (compiled)
* model --deep learning model 
* frontend  --front-end program (source code)
```

## Model List
Currently, the BiSeNetv2 and PSPNet models are supported. The BiSeNetv2 model is small in size, has a fast predictive operation speed, and is suitable for a CPU operating environment, but the accuracy is poor. The PSPNet model has higher requirements for GPU, slower running speed, but higher accuracy. Note: Before using PSPNet, you need to install and configure the CUDA9.0+ .   
| Network Structure  | Size | Requirement | Download Link |
| :-------- | -------: | :------: | :------: |
| BiSeNetv2 |   8.4 MB |   CPU    |   http://www.gis.show/index/article/id/18   |
| PSPNet    | 307.7 MB |   GPU    |   http://www.gis.show/index/article/id/19   |


## License
This project uses The GNU General Public License v3.0 (GPL3.0). Any program using this project needs to follow the content of the GPL3.0 and add citation sources.
## About us
SCULAB https://www.scurbanlab.com/
## Citation
If you find our project useful in your research, please consider citing: 

```latex
@article{CHEN2021151605,
        title = {Predicting the effect of street environment on residents' mood states in large urban areas using machine learning and street view images},
        journal = {Science of The Total Environment},
        pages = {151605},
        year = {2021},
        issn = {0048-9697},
        doi = {https://doi.org/10.1016/j.scitotenv.2021.151605},
        author = {Chongxian Chen and Haiwei Li and Weijing Luo and Jiehang Xie and Jing Yao and Longfeng Wu and Yu Xia}
}
```
## Thanks
Paddlepaddle http://www.paddlepaddle.org.cn  
GT https://github.com/GT-ZhangAcer