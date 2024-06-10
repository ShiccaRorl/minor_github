
# やりたいこと
#   プロジェクト管理
#   マニアックで覚えられそうにない、おっさん向けコマンドを使えられるようにする
#   後、インストールとかを自動化する。タブで分けて使う   

import PySimpleGUI as sg
import subprocess
import datetime

class minor_github:
    def __init__(self):
        self.update = ""
        
    def commit(self, file_name, message=""):
        self.update = self.update + "commit" + " " + datetime.datetime.now().strftime("%Y/%m/%d_%H:%M:%S") + "\n"
        self.update = self.update + f"{message}" + "\n"
        self.update = subprocess.run(["git", "add", f"{file_name}"], stdout=subprocess.PIPE)
        self.update = subprocess.run(["git", "commit", "-m", f"{self.update}"], stdout=subprocess.PIPE)
        self.update = subprocess.run(["git", "push"], stdout=subprocess.PIPE)
        
        
    def get_layout():
        sg.Listbox([], size=(100, 50), key="-プロジェクト-")
        
    def get_events():
        pass