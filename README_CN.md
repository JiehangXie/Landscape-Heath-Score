<h1 align="center">Landscape-Health Score</h1>

![功能介绍](https://github.com/JiehangXie/Landscape-Heath-Score/raw/main/docs/microsoft-edge-beta_test.gif)

# 简介
Landscape-Health Score（LHS）是一个基于百度Paddlepaddle深度学习框架搭建景观健康效益辅助评估工具，只需要简单的拖拽图片文件则可自动分析图像和生成简单的评价报告。目前支持的Bisenet和PSPNet模型可实现9种环境要素的识别和分割，并实时统计环境要素的比例，绿视率和快乐/放松/专注/社交/活力/压抑等6项心理指标的分数。
# 导航
- [简介](#简介)
- [导航](#导航)
- [功能介绍](#功能介绍)
  - [1.图像分割](#1图像分割)
  - [2.绿视率计算](#2绿视率计算)
  - [3.健康效益评估](#3健康效益评估)
- [快速开始](#快速开始)
  - [环境要求](#环境要求)
    - [基本环境](#基本环境)
    - [二次开发环境](#二次开发环境)
  - [1.Windows运行](#1windows运行)
  - [2.源代码运行](#2源代码运行)
    - [2.1 安装Python 3.7+](#21-安装python-37)
    - [2.2 安装依赖包](#22-安装依赖包)
    - [2.3 下载模型](#23-下载模型)
    - [2.4 运行](#24-运行)
  - [批量处理](#批量处理)
    - [接口说明](#接口说明)
    - [Curl](#curl)
    - [PHP](#php)
    - [Python](#python)
- [其他](#其他)
  - [文件目录架构](#文件目录架构)
  - [模型选择](#模型选择)
  - [开源协议](#开源协议)
  - [特别致谢](#特别致谢)

# 功能介绍

## 1.图像分割  
图像分割功能基于图像语义分割技术原理，利用深度学习技术与Cityscapes数据集训练模型，通过模型对像素进行识别分类和统计每种要素在图像上的面积比例。
目前支持识别的环境要素有：  
- [x] 天空
- [x] 树木/树篱/各种垂直植被
- [x] 草/各种水平植被
- [x] 围栏
- [x] 建筑
- [x] 独立的墙壁
- [x] 人行道
- [x] 马路
- [x] 柱/杆
- [ ] 水体（后续支持）
- [ ] 山体（后续支持）
## 2.绿视率计算  
绿视率是环境绿化评估的参考指标之一，传统绿视率通过利用图像像素RGB值的原理进行统计，受环境因素影响明显，统计数据误差较大，基于深度学习方法能够识别图像中绿色植物，排除其他干扰因素（如绿色的衣服/广告牌等），从而实现较精确的比例计算。
## 3.健康效益评估
支持针对输入图像进行快乐/放松/专注/社交/活力/压抑等6项心理维度的评估分析，目前该功能仍处于研究和测试阶段，算法之后会不断升级迭代。

# 快速开始
## 环境要求
### 基本环境
* Windows10(推荐)
* CPU Intel i5或AMD同等性能处理器
* GPU RTX1060 6G以上配置（可选）
### 二次开发环境
（一般不用管，可以跳过）
* npm >= 7.15
* Vite 2
* VUE 3.0
## 1.Windows运行
努力打包中，后续支持

## 2.源代码运行
### 2.1 安装Python 3.7+
### 2.2 安装依赖包
按下`Win+R`键，输入cmd，进入命令行窗口  
输入`cd LHS所在的文件夹目录`进入目录  
输入`pip install requirement.txt`  
耐心等待安装完成即可。
### 2.3 下载模型
前往[模型选择](#模型选择)下载任一模型的压缩包，并解压后将全部文件复制到model文件夹中。初次使用，推荐下载BiSeNetv2模型。
### 2.4 运行
按下`Win+R`键，输入cmd，进入命令行窗口  
输入`cd LHS所在的文件夹目录`进入目录  
输入`python app.py`  运行程序
打开除IE以外的任何浏览器，输入`http://127.0.0.1:5000`即可进入操作界面。

## 批量处理
为了满足批量处理图片的要求，我加入了http接口，可以在运行程序的情况下通过任何语言的代码发起POST请求。
### 接口说明
HTTP方法：POST  
请求地址：http://127.0.0.1:5000/api/v1/json  
Header:
| 参数         |               值 |
| :----------- | ---------------: |
| Content-Type | application/json |

请求参数:  
| 参数  |   类型 |                                       说明 |
| :---- | -----: | -----------------------------------------: |
| image | string | 图片信息，base64编码，bytes需要转换成utf-8 |

返回参数:
| 参数       |   类型 |                       说明 |
| :--------- | -----: | -------------------------: |
| image      | string | 切割后效果图像的base64编码 |
| glr        | double |                     绿视率 |
| proportion |   json |               环境要素占比 |
| score      |   json |            6项心理指标评分 |

下面提供curl/php和python三种请求案例。
### Curl
```
curl -i -k 'http://127.0.0.1:5000/api/v1/json' --data 'image=【图片Base64编码，需UrlEncode】' -H 'Content-Type:application/x-www-form-urlencoded'
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
    // 初始化curl
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
$img = file_get_contents('[本地文件路径]');
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
f = open('[本地文件路径]', 'rb')
img = base64.b64encode(f.read()).decode('utf-8')

params = {'image':img}
headers = {'content-type': 'application/json'}
response = requests.post(request_url, data=json.dumps(params), headers=headers)
if response:
    print (response.json())
```
# 其他
## 文件目录架构
```
* requirement.txt  --依赖文件列表
* app.py  --启动入口程序
* infer_api.py  --预测程序的主文件
* Qscore_algorithm.py  --评分模块文件
* dist --编译好的网页前端程序
* model --深度学习模型文件
* frontend  --基于Vite2 + VUE3.0写的前端源代码
```

## 模型选择
目前支持BiSeNetv2和PSPNet模型，BiSeNetv2模型体积小，预测运行速度快，适合纯CPU的运行环境，但效果精度较差。PSPNet模型对显卡要求较高，运行速度较慢，但精度较高。注：使用PSPNet需要先安装配置CUDA9.0+环境。
| 网络结构  | 模型大小 | 运行环境 | 下载地址 |
| :-------- | -------: | :------: | :------: |
| BiSeNetv2 |   8.4 MB |   CPU    |   http://www.gis.show/index/article/id/18   |
| PSPNet    | 307.7 MB |   GPU    |   http://www.gis.show/index/article/id/19   |


## 开源协议
本项目使用The GNU General Public License v3.0(GPL3.0)开源协议，基于项目的二次开发需要遵循GPL3.0协议中的内容，使用代码需要添加引用出处，不允许修改后和衍生的代码做为闭源的商业软件发布和销售。
## 特别致谢
百度飞桨 http://www.paddlepaddle.org.cn  
GT https://github.com/GT-ZhangAcer