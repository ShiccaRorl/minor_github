import subprocess
import sys
import PySimpleGUI as sg

class GitGUI:
    def __init__(self):
        self.window = sg.Window("Git GUI", self.get_layout(), resizable=True, finalize=True)
        self.commit_index = 0
        self.commit_hashes = self.get_git_log()

    def get_layout(self):
<<<<<<< Updated upstream
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
    
=======
>>>>>>> Stashed changes
        layout = [
            [sg.Button("始める"), sg.Input("file name", key="-file_name-")],
            [sg.Button("←"), sg.Button("checkout"), sg.Button("→")],
            [sg.Text("", size=(50, 1), key="-STATUS-")]
        ]
        return layout

    def run_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Command failed: {command}\n{result.stderr}"
        return result.stdout

    def update_status(self, message):
        self.window['-STATUS-'].update(message)

    def get_git_log(self):
        log_output = self.run_command("git log --pretty=format:'%H'")
        commit_hashes = log_output.strip().split('\n')
        return commit_hashes

    def checkout_commit(self, commit_hash):
        response = sg.popup_yes_no("Checkout しますか？")
        if response == 'Yes':
            result = self.run_command(f"git checkout {commit_hash}")
            self.update_status(result)

    def get_events(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break

            if event == "始める":
                result = self.run_command("git stash")
                self.update_status(result)
            elif event == "←":
                if self.commit_index < len(self.commit_hashes) - 1:
                    self.commit_index += 1
                    commit_hash = self.commit_hashes[self.commit_index]
                    self.checkout_commit(commit_hash)
            elif event == "checkout":
                if "-file_name-" in values and values["-file_name-"]:
                    file_name = values["-file_name-"]
                    commit_hash = self.commit_hashes[self.commit_index]
                    add_result = self.run_command(f"git add {file_name}")
                    commit_result = self.run_command(f"git commit -m 'Revert {file_name} to previous state from commit {commit_hash}'")
                    self.update_status(f"Reverted {file_name} to previous state from commit {commit_hash}\n{add_result}\n{commit_result}")
            elif event == "→":
                if self.commit_index > 0:
                    self.commit_index -= 1
                    commit_hash = self.commit_hashes[self.commit_index]
                    self.checkout_commit(commit_hash)

        self.window.close()

if __name__ == "__main__":
    git_gui = GitGUI()
    git_gui.get_events()
