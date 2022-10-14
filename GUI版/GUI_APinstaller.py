import tkinter.ttk
import multitasking
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import os
import socket

root = tkinter.Tk()
root.title("APinstaller 1.0.0 EAP")
root.geometry("400x200+750+400")

headers = {
        'Accept-Encoding': 'identity',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
Label3_text = tkinter.StringVar()
Label3_text.set("当前没有下载任务")


def Split(url):
    res = requests.head(url, headers=headers)
    length = res.headers.get('Content-Length')
    result = 1024 / int(length) * 100
    return result

def Split_file(filesize, chuck=10):
    step = filesize//chuck
    arr = list(range(0, filesize, step))
    result = []
    for i in range(len(arr)-1):
        s_pos, e_pos = arr[i], arr[i+1]-1
        result.append([s_pos, e_pos])
    result[-1][-1] = filesize-1
    return result

def Get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


ips = Get_ip()
ip_list = {"ip": ips}


@multitasking.task
def download(url, save_name=""):
    global Label3_text
    size = Split(url)
    print(size)

    if save_name == "":
        save_name = os.path.basename(url)
    file = requests.get(url, headers=headers, proxies=ip_list, stream=True, allow_redirects=True)
    with open(save_name, 'rb+') as f:
        for chunk in file.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                Progressbar1["value"] += size
                root.update()

    multitasking.wait_for_tasks()
    f.close()
    Label3_text.set("下载完成")


def _command_():
    global Label3_text
    Progressbar1["value"] = 0
    Label3_text.set("下载中")
    download(URL_Entry1.get())


Label1 = tkinter.Label(root, text="要下载的文件的网址：")
Label1.grid(row=0, column=0)

Label2 = tkinter.Label(root, text="下载进度：")
Label2.grid(row=1, column=0)

Label3 = tkinter.Label(root, text="当前没有下载任务", textvariable=Label3_text)
Label3.grid(row=2, column=1)

URL_Entry1 = tkinter.Entry(root, width=30)
URL_Entry1.grid(row=0, column=1)

Download_Button = tkinter.Button(root, text="下载", command=_command_)
Download_Button.grid(row=0, column=2)

Progressbar1 = tkinter.ttk.Progressbar(root, length=215, mode="determinate")
Progressbar1.grid(row=1, column=1)
Progressbar1["value"] = 0
Progressbar1["maximum"] = 100

root.mainloop()
