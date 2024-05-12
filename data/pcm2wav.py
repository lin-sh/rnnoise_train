import os
import wave
import sys

def wav_to_pcm(input_folder, output_folder):
    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中所有.wav文件的路径
    wav_files = [f for f in os.listdir(input_folder) if f.endswith('.wav')]

    for wav_file in wav_files:
        # 不是wav文件则跳过
        if not wav_file.endswith('.wav'):
            continue
        # 构造输入和输出文件的完整路径
        input_path = os.path.join(input_folder, wav_file)
        output_path = os.path.join(output_folder, os.path.splitext(wav_file)[0] + '.pcm')

        # 打开.wav文件
        with wave.open(input_path, 'rb') as wav:
            # 读取.wav文件的参数
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            frame_rate = wav.getframerate()

            # 打开输出文件
            with open(output_path, 'wb') as pcm:
                # 读取.wav文件中的音频数据并写入输出文件
                while True:
                    frames = wav.readframes(1024)
                    if not frames:
                        break
                    pcm.write(frames)
        # 删除原始的.wav文件
        os.remove(input_path)

if __name__ == "__main__":
    # 获取传递给Python脚本的文件路径参数
    file_path = sys.argv[1]
    # 文件夹不存在则创建
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    input_folder = file_path  # 输入文件夹路径
    output_folder = file_path  # 输出文件夹路径

    wav_to_pcm(input_folder, output_folder)
