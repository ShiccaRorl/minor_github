import PySimpleGUI as sg
import subprocess
import datetime
import glob
import os
import platform

class Minor_Github:
    def __init__(self, project_directory):
        self.project_directory = project_directory

    def get_changed_files(self):
        # 現在のディレクトリをプロジェクトディレクトリに変更
        os.chdir(self.project_directory)

        # 変更されたファイルのリストを取得
        status_result = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if status_result.returncode != 0:
            print(f"Error in git status: {status_result.stderr.decode('utf-8')}")
            return []

        changed_files = [line[3:] for line in status_result.stdout.decode('utf-8').splitlines()]
        return changed_files

    def commit_all(self, message=""):
        changed_files = self.get_changed_files()
        if not changed_files:
            print("No changes to commit.")
            return

        # 変更されたファイルをステージング
        for file in changed_files:
            add_result = subprocess.run(["git", "add", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if add_result.returncode != 0:
                print(f"Error in git add {file}: {add_result.stderr.decode('utf-8')}")
                return

        # コミットメッセージを作成
        commit_message = "commit " + datetime.datetime.now().strftime("%Y/%m/%d_%H:%M:%S") + "\n" + message
        commit_result = subprocess.run(["git", "commit", "-m", commit_message], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if commit_result.returncode != 0:
            print(f"Error in git commit: {commit_result.stderr.decode('utf-8')}")
            return

        # プッシュ
        push_result = subprocess.run(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if push_result.returncode != 0:
            print(f"Error in git push: {push_result.stderr.decode('utf-8')}")
            return

        print("All changes committed and pushed successfully.")

    def commit_one_by_one(self, message=""):
        changed_files = self.get_changed_files()
        if not changed_files:
            print("No changes to commit.")
            return

        # 変更されたファイルを一つずつコミット
        for file in changed_files:
            add_result = subprocess.run(["git", "add", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if add_result.returncode != 0:
                print(f"Error in git add {file}: {add_result.stderr.decode('utf-8')}")
                continue

            # コミットメッセージを作成
            commit_message = "commit " + datetime.datetime.now().strftime("%Y/%m/%d_%H:%M:%S") + "\n" + message + "\nFile: " + file
            commit_result = subprocess.run(["git", "commit", "-m", commit_message], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if commit_result.returncode != 0:
                print(f"Error in git commit {file}: {commit_result.stderr.decode('utf-8')}")
                continue

            # プッシュ
            push_result = subprocess.run(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if push_result.returncode != 0:
                print(f"Error in git push: {push_result.stderr.decode('utf-8')}")
                continue

            print(f"File {file} committed and pushed successfully.")

class OS_Kantei:
    def get_os(self):
        system = platform.system()
        if system == "Windows":
            return "Windows"
        elif system == "Linux":
            return "Linux"
        else:
            return "Unknown"

class ProjectManager:
    def __init__(self):
        self.project_directory = ""
        self.config_file = "config.txt"
        self.project_directory = self.load_project_directory(0)
        self.ms_visual_windows = self.load_project_directory(1)
        self.ms_visual_linux = self.load_project_directory(2)
    
    def load_project_directory(self, line_num):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                lines = file.read().split("\n")
                if len(lines) > line_num:
                    return lines[line_num].strip()
        return ""

    def save_project_directory(self, project_directory, ms_visual_windows, ms_visual_linux):
        with open(self.config_file, "w") as file:
            file.write(project_directory + "\n")
            file.write(ms_visual_windows + "\n")
            file.write(ms_visual_linux + "\n")

    def get_project(self):
        if self.project_directory:
            project_directory = glob.glob(f"{self.project_directory}/*")
            return project_directory
        return []
    
    def get_layout(self):
        # Create separate list boxes for each layout to avoid reusing elements
        project_list_main = [
            [sg.Listbox(self.get_project(), size=(50, 20), key="-プロジェクト_MAIN-")]
        ]
        
        project_list_setup = [
            [sg.Listbox(self.get_project(), size=(50, 20), key="-プロジェクト_SETUP-")]
        ]

        setup = [
            [sg.Text("プロジェクトディレクトリ")],
            [sg.InputText(self.project_directory, key="-プロジェクトディレクトリ-"), sg.FolderBrowse()]
        ]
    
        ms_visual_windows = [
            [sg.Text("MSVisual Studio Code Windows")],
            [sg.InputText(self.ms_visual_windows, key="-ms_visual_windows-"), sg.FolderBrowse()]
        ]
    
        ms_visual_linux = [
            [sg.Text("MSVisual Studio Code Linux")],
            [sg.InputText(self.ms_visual_linux, key="-ms_visual_linux-"), sg.FolderBrowse()]
        ]
    
        setup_layout = [
            *project_list_setup,
            [sg.Column(setup)],
            [sg.Column(ms_visual_windows)],
            [sg.Column(ms_visual_linux)],
        ]
    
        main_run_layout = [
            [sg.Text("Main Run Placeholder")],
            *project_list_main,
            [sg.Button("開く")],
        ]
    
        github_layout = [
            [sg.Text("GitHub Placeholder")],
            [sg.Text(f"{self.file_name}", key="--")],
        ]
    
        layout = [
            [sg.TabGroup([[sg.Tab('main_run', main_run_layout), sg.Tab('Github', github_layout), sg.Tab('設定', setup_layout)]])],
            [sg.Button('OK'), sg.Button('Cancel')]
        ]
    
        return layout

if __name__ == "__main__":
    pm = ProjectManager()
    layout = pm.get_layout()
    window = sg.Window("Project Manager", layout)
    OSs = OS_Kantei().get_os()
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "OK":
            project_directory = values["-プロジェクトディレクトリ-"]
            ms_visual_windows = values["-ms_visual_windows-"]
            ms_visual_linux = values["-ms_visual_linux-"]
            
            pm.save_project_directory(project_directory, ms_visual_windows, ms_visual_linux)
        
        elif event == "開く":
            selected_project = values["-プロジェクト_MAIN-"]
            ms_visual_windows = values["-ms_visual_windows-"]
            ms_visual_linux = values["-ms_visual_linux-"]
            if selected_project:
                project_path = selected_project[0]
                if OSs == "Windows":
                    subprocess.run([ms_visual_windows, project_path])
                elif OSs == "Linux":
                    subprocess.run([ms_visual_linux, project_path])
                else:
                    print("OS不明です")
                
    window.close()
    
project_directory = "/home/ban/ドキュメント/GitHub/"
mg = Minor_Github(project_directory)
    
# すべての変更を一度にコミット
mg.commit_all("全体の変更をコミット")

# 変更されたファイルを一つずつコミット
mg.commit_one_by_one("ファイルごとの変更をコミット")