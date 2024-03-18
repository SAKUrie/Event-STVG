import os
import subprocess
import time
from tqdm import tqdm

# 获取当前目录及子目录下所有的mkv文件
mkv_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".mkv"):
            mkv_files.append(os.path.join(root, file))

# 初始化进度条
pbar = tqdm(total=len(mkv_files), unit="file", desc="Converting MKV to MP4")

# 开始转换前的时间
start_time = time.time()

# 遍历所有mkv文件进行转换
for mkv_path in mkv_files:
    mp4_path = os.path.splitext(mkv_path)[0] + ".mp4"

    # 使用ffmpeg命令行工具进行转换，使用ultrafast预设，并设置日志级别为error，自动覆盖已存在的文件
    subprocess.run([
        "ffmpeg", "-i", mkv_path,
        "-preset", "ultrafast",
        "-loglevel", "error",
        "-y",  # 自动覆盖输出文件
        mp4_path
    ])

    # 更新进度条
    pbar.update(1)

# 完成进度条
pbar.close()

# 结束转换后的时间
end_time = time.time()

# 计算并输出总耗时
total_time = end_time - start_time
print(f"转换完成。总耗时: {total_time:.2f} 秒")