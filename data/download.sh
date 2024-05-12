#!/bin/bash

# 下载噪声文件并重命名
wget -c "https://zenodo.org/records/1227121/files/DLIVING_48k.zip?download=1" -O noise.zip

# 下载纯净语言文件并重命名
wget -c "https://www.openslr.org/resources/30/si_lk.tar.gz" -O speech.tar.gz
