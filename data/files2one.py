import os
import sys

def merge_pcm_files(input_folder, output_file):
    # 获取输入文件夹中所有pcm文件的路径
    pcm_files = [f for f in os.listdir(input_folder) if f.endswith('.pcm')]
    
    with open(output_file, 'wb') as out_pcm:
        for pcm_file in pcm_files:
            input_path = os.path.join(input_folder, pcm_file)
            with open(input_path, 'rb') as in_pcm:
                # 读取每个pcm文件的内容并写入合并后的文件
                out_pcm.write(in_pcm.read())

if __name__ == "__main__":
    # 获取传递给Python脚本的文件路径参数
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    # 文件夹不存在则创建
    if not os.path.exists(input_file_path):
        os.makedirs(input_file_path)
    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)
        
    input_folder = input_file_path  # 输入文件夹路径
    output_file = output_file_path + "/output.pcm"  # 输出文件路径

    merge_pcm_files(input_folder, output_file)
