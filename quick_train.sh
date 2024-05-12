#!/bin/bash

# 噪声文件夹路径
noise_dir="./data/noise"
# 纯净语音文件夹路径
speech_dir="./data/speech"

# 合并为一条音频的噪声文件夹路径
noise_single_dir="./data/one_noise"
# 合并为一条音频的纯净语音文件夹路径
speech_single_dir="./data/one_speech"
# 特征个数
count=10000


####################
######数据准备######
####################
# 调用pcm2wav.py并传参，将噪声文件夹下的pcm文件转为wav文件
# 打印
echo "Converting noise files to wav..."
python data/pcm2wav.py $noise_dir

# 调用pcm2wav.py并传参，将纯净语音文件夹下的pcm文件转为wav文件
echo "Converting speech files to wav..."
python data/pcm2wav.py $speech_dir

# 调用data/files2one.py并传参，将噪声文件夹下的多个音频合并为一条音频
echo "Converting noise files to one..."
python data/files2one.py $noise_dir $noise_single_dir

# 调用data/files2one.py并传参，将纯净语音文件夹下的多个音频合并为一条音频
echo "Converting speech files to one..."
python data/files2one.py $speech_dir $speech_single_dir


####################
######特征提取######
####################
cd src
source compile.sh

# 调用denoise_training并传参，提取特征
echo "Extracting features..."
./denoise_training ../data/one_speech/output.pcm ../data/one_noise/output.pcm $count > ../training/output.f32

# 调用bin2hdf5.py并传参，将特征转为h5文件
echo "Converting features to h5..."
cd ../training
python bin2hdf5.py output.f32 $count 87 training.h5

####################
######模型训练######
####################
echo "Training model..."
python rnn_train.py

# 获取权重参数
echo "Dumping weights..."
python dump_rnn.py weights.hdf5 ../src/rnn_data.c ../src/rnn_data orig

# 完成
echo "Done."