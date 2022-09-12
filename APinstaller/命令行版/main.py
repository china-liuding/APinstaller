from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import tqdm
import os

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }

def Split(filesize, file_chunk=10):
    step = filesize//file_chunk
    arr = list(range(0, filesize, step))
    result = []
    for i in range(len(arr)-1):
        pos1, pos2 = arr[i], arr[i+1]-1
        result.append([pos1, pos2])
    result[-1][-1] = filesize-1
    return result


def download(Save_name, s_pos, e_pos):
    headers = {"Range": f"bytes={s_pos}-{e_pos}"}
    res = requests.get(url, headers=headers, stream=True)
    with open(Save_name, "rb+") as f:
        f.seek(s_pos)
        for chunk in res.iter_content(chunk_size=64*1024):
            if chunk:
                f.write(chunk)
                Bar.update()


argv = input("请输入参数（可选）:")
url = input("请输入下载文件网址:")
if argv == "-d":
    file_name = os.path.basename(url)
    head = requests.head(url, headers=headers)
    file_size = head.headers.get('Content-Length')
    if file_size is not None:
        file_size = int(file_size)
    response = requests.get(url, headers=headers, stream=True)
    chunk_size = 1024
    bar = tqdm.tqdm(total=file_size, desc=f'下载文件 {file_name}')
    with open(file_name, mode='wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            bar.update(chunk_size)
    bar.close()
    print(f"下载完成，文件名为：{file_name}")
else:
    res = requests.head(url)
    save_name = os.path.basename(url)
    filesize = int(res.headers['Content-Length'])
    ranges = Split(filesize)
    print(f"分块数:{len(ranges)}")
    Bar = tqdm.tqdm(total=filesize, desc=f"下载文件{save_name}")

    with open(save_name, "wb") as f:
        pass
    with ThreadPoolExecutor() as t:
        futures = []
        for s_pos, z_pos in ranges:
            t.submit(download, save_name, s_pos, z_pos)
        as_completed(futures)
    print(f"下载完成，文件名为{save_name}")
