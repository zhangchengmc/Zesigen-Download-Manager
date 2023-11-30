import requests
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import os
import threading

def get_filename_from_url(url):
    # 从下载链接中提取文件名.
    return os.path.basename(url)

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    with open(save_path, 'wb') as file:
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
        progress_bar.close()

def download_ftp_file(url, save_path):
    with open(save_path, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

def choose_save_location(file_name):
    root = tk.Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(defaultextension='.*', initialfile=file_name)
    return save_path

def is_html_file(file_path):
    # 检测文件扩展名是否是.html或.htm的文件名
    _, file_ext = os.path.splitext(file_path)
    return file_ext.lower() in ['.html', '.htm']

def download_single_file(url, save_path):
    if url.startswith('ftp'):
        download_ftp_file(url, save_path)
    else:
        download_file(url, save_path)

    print(f"下载完成: {url}")

def download():
    urls = []

    # 输入多个链接，以空行结束输入
    print("请输入下载链接（每行一个链接）：")
    while True:
        url = input()
        if url:
            urls.append(url)
        else:
            break

    print("开始下载...")
    threads = []

    for url in urls:
        save_path = choose_save_location(get_filename_from_url(url))
        thread = threading.Thread(target=download_single_file, args=(url, save_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("所有文件下载完成！")

if __name__ == '__main__':
    download()
