## 训练过程

### 用法1:

#### 安装GPU版本MindSpore（这里可以使用官网安装教程，注意python<3.9这里用的是python3.8，mindspore使用版本1.8.1）

```bash
pip install mindspore-gpu==1.8.1
```

#### 下载和预处理数据

```bash
# download dataset
bash scripts/download_dataset.sh
# build dataset
bash scripts/build_dataset.sh [task_type]
# convert to mindrecord
bash scripts/convert_dataset.sh [task_type]
# task type: match, match_kn, match_kn_gene
# default: match_kn_gene
```

#### GPU处理器上运行训练（这里会训练模型，生成save_model文件夹，里面是生成的checkpoint）

```bash
bash scripts/run_train.sh [task_type]
# task type: match, match_kn, match_kn_gene
# default: match_kn_gene
```
#### GPU处理器上预测（利用上一步生成的模型进行预测，生成score.txt和predict.txt）
方法一：
```bash
bash scripts/run_predict.sh
# task type: match, match_kn, match_kn_gene
# default: match_kn_gene
```
方法二：
如果方法一无法直接运行，请尝试方法二：
1、新建一个output空文件夹；
2、一次运行scripts/run_predict.sh里面的每一条命令，需要注意的是load的模型需要换成训练生成的模型；
3、依次执行完后会得到score.txt和predict.txt。

### 用法1:
一、配置和用法一一样的环境和数据集；
二：执行jupyter.py即可得到predict.txt和score.txt.