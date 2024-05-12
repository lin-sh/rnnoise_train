# Rnnoise训练指南

## 依赖安装

整个训练过程会用C语言环境和python环境

```shell
apt-get install build-essential
apt-get install autoconf libtool
```

python相关依赖在rnnoise/training/requirements.txt中，推荐python>=3.8

## 代码准备

```sh
git clone https://github.com/xiph/rnnoise.git -chekcout master
```

代码是基于master分支

## 快速开发

```sh
source rnnoise/quick_train.sh
```

给该sh文件足够的权限，然后运行即可一键训练。训练完成后，可跳转到编译和运行章节进行效果验证。

> rnnoise/data/download.sh

运行该文件会自动下载两个小的数据集进行验证

## 数据集准备

准备两个数据集，一个噪声数据集，一个纯净语言数据集。音频格式要求：48K采用，16bit。训练真正使用的是pcm格式的音频。如果有pcm的可以跳过下面音频格式转化这一步。但是现有很多数据集都提供的是wav格式，所有需要转化为pcm格式。

#### wav转pcm

> rnnoise/data/pcm2wav.py

该python文件提供了音频格式转换的功能

```python
input_folder = "/home/aec/rnnoise/data/noise" 
```

修改文件路径为自己主机的数据集所在路径，他会自动将wav格式转为pcm格式(不是wav格式会自动跳过，防止报错)，并删除原有的wav格式音频，防止数据冗余。（详细步骤可见代码注释）

#### 数据集文件位置

噪声数据集存放于

> rnnoise/data/noise/

纯净语言数据集存放于

> rnnoise/data/speech/

#### 数据集合并

我们需要将数据集中的数据合并为一条数据，原因有两点：

- 为了方便知道我们馈入给模型的数据具体听起来是什么
- 特征提取阶段需要对一条数据进行操作

> rnnoise/data/pcm2wav.py

运行该python文件，修改路径为本机路径

```python
input_folder = "/home/aec/rnnoise/data/speech"  # 输入文件夹路径
output_file = "/home/aec/rnnoise/data/one_speech/output.pcm"  # 输出文件路径
```

转换后的数据默认保存在rnnoise/data/one_noise和rnnoise/data/one_speech文件夹下，各有一条output.pcm。

## 特征提取

进入src文件夹

> rnnoise/src/

运行

```sh
/compile.sh
```

执行后会生成文件denoise_training.它有三个入参，第一个是干净的说话语音，第二个是加噪的说话语音，第三个是生成的特征个数（官方推荐越大越好，至少≥10000）。

```sh
./denoise_training clean_speech.pcm noise_background.pcm 10000 > output.f32

```

提取出来的特征会保存到rnnoise/src/output.f32文件中，如要保存到其他地方，修改output.f32为自己的路径即可。

然后进入

> rnnoise/training/

运行

```sh
python bin2hdf5.py output.f32 10000 87 training.h5
```

将上一步提取出来的特征转化为.h5文件，用于后续模型训练。

10000和上一步的特征个数要一致，87是默认的特征维度，不用修改，output.f32是上一步文件的保存路径，training.h5是新生成的文件。

## 模型训练

```sh
python rnn_train.py
```

默认是读取/training文件夹内的training.h5，运行后即可开始模型训练。

## 获取权重参数

```sh
python dump_rnn.py weights.hdf5 ../src/rnn_data.c ../src/rnn_data orig
```

运行命令将训练好的模型转换为C语言可以识别的参数，该命令会自动替换rnn_data.c文件，rnn_data.h文件不用替换

## 编译和运行

返回到rnnoise目录下

```sh
./autogen.sh
./configure
make
```

如果是第一次编译，运行上述所有命令

```sh
make clean
make
```

如果是非第一次编译，运行这两行即可

进入examples目录下

```sh
./rnnoise_demo noisy.pcm denoise.pcm
```

noisy.pcm为含噪音频，denoise.pcm为增强后音频，具体代码可查看rnnoise_demo.c文件