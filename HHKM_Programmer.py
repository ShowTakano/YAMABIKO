import tkinter as tk
from tkinter import messagebox as mb
import time

# pip install pyserial
import serial
from serial.tools import list_ports

import webbrowser

from icons.icon import GuiIcon

"""
pyinstaller               4.5.1
pyinstaller HHKM_Programmer.py --onefile --noconsole --icon=icons/ico.ico
"""

class SerialDevice():
    def __init__(self):
        self.serial = serial.Serial()
        self.baudrate = 9600
        self.timeout = 0.1
        self.device = "COM3"
        self.port = self.device
        self.send_msg = bytes([])

    def get_list_ports(self):
        ports = list_ports.comports()
        dst = []
        for port in ports:
            print(port.device)
            dst.append(port.device)
        return dst

    def set_baudrate(self, baudrate):
        print("set baudrate", baudrate)
        self.baudrate = baudrate

    def set_timeout(self, timeout):
        print("set timeout", timeout)
        self.timeout = timeout

    def set_device(self, COMx):
        print("set device", COMx)
        self.device = COMx
        self.port = self.device

    def open(self):
        self.serial.baudrate = self.baudrate
        self.serial.timeout = self.timeout
        self.serial.port = self.port
        self.serial.open()
        print("successsly opend your device.")

    def write_str(self, str):
        print("write_str", str)
        self.serial.write(str.encode(encoding="utf-8"))


class Tk():
    def __init__(self):
        # serial
        self.mydevice = SerialDevice()

        # 画面初期化
        self.root = tk.Tk()
        self.root.title("HHKM Programmer")
        self.root.geometry("640x480")
        
        # icon画像
        guiicon = GuiIcon()
        self.img = tk.PhotoImage(data=guiicon.data)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.img)

        self.click = "<Button-1>"

        # 接続するデバイスを選択するオプションメニュー
        self.ports = ["None"]
        self.port_selected = tk.StringVar()
        self.port_selected.set(self.ports[0])
        self.port_opt_menu = tk.OptionMenu(self.root, self.port_selected, *self.ports)

        # デバイス接続 open結果描画用テキストボックス
        self.txt_open = tk.Text(width=13, height=1)

        # コマンド一覧　オプションメニュー選択文字 : 送信文字
        self.all_commands_dict = {
            "None":                         "None", 
            "Mouse left-click":             "mouse-left-click", 
            "Mouse right-click":            "mouse-right-click", 
            "Mouse move":                   "mouse-move", 
            "Key up":                       "key-up",  # KEY_UP_ARROW
            "Key down":                     "key-down",  # KEY_DOWN_ARROW
            "Key left":                     "key-left",  # KEY_LEFT_ARROW
            "Key right":                    "key-right",  # KEY_RIGHT_ARROW
            "Key Tab":                      "key-tab",  # KEY_TAB
            "Key Esc":                      "key-ecs",  # KEY_ESC
            "Key F2":                       "key-f2",  # KEY_F2
            "Key F5":                       "key-f5",  # KEY_F5
            "Key PrintScreen":              "key-psc",  # #define KEY_PRINTSCREEN 0xCE 「printscreen」で検索し、「PrintScreenキーを使用して画面の領域の切り取りを起動する」から、「プリントスクリーンのショートカット」の「PrtScnボタンを使用して画面領域切り取りを開く」をオンに。「ピクチャ」の「スクリーンショット」に画像が保存される
            "Key Windows":                  "key-gui",  # KEY_LEFT_GUI
            "Key command (OSX)":            "key-gui",  # KEY_LEFT_GUI
            "Key command (Linux)":          "key-gui",  # KEY_LEFT_GUI
            "Key Enter":                    "key-enter",  # KEY_RETURN
            "Key Shift (keep)":             "key-shift-keep",  # KEY_LEFT_SHIFT
            "Key Ctrl (keep)":              "key-ctrl-keep",  # KEY_LEFT_CTRL
            "Key Alt (keep)":               "key-alt-keep",  # KEY_LEFT_ALT
            "Key Del (keep)":               "key-del-keep",  # KEY_DELETE
            "Key command (OSX) (keep)":     "key-gui-keep",  # KEY_LEFT_GUI
            "Key release-all":              "key-release",
            "Type":                         "type",
            "Command-prompt(Win)":          "terminal-win",  # (KEY_LEFT_GUI cmd enter)
            "Terminal(OSX)":                "terminal-osx",  # (KEY_LEFT_GUI-N)
            "Terminal(Linux)":              "terminal-linux",  # (ctrl-alt-t)
            "Log-out(Win)":                 "log-out-win",  # (ctrl-alt-del down down enter)
            "Log-out(OSX)":                 "log-out-osx",  # (KEY_LEFT_GUI-Shift-Q enter)
            "Log-out(Linux)":               "log-out-linux",  # (ctrl-alt-del enter)
        }

        # コマンド数
        self.NUM_COMMAND = 10

        # コマンドリスト
        self.cmd_list = []
        for k in self.all_commands_dict.keys():
            self.cmd_list.append(k)

        # 登録リスト
        self.cmd_selected_list = []
        self.opt_list = []
        self.spn_selected_list = []
        self.spn_box_list = []
        self.int_or_once_selected_list = []
        self.int_or_once_opt_list = []
        self.entry_type_list_list = []
        self.entry_type_var_list = []


    def _search_ports(self, event):
        # portを探索する。探索した結果をオプションメニューの選択肢に反映する。
        # https://stackoverflow.com/questions/17580218/changing-the-options-of-a-optionmenu-when-clicking-a-button
        ports = self.mydevice.get_list_ports()
        msg = ""
        for port in ports:
            self.ports.append(port)
            msg = msg + port + "\n"
        print(msg)
        # Refrech self.port_opt_menu
        self.port_selected.set("")
        self.port_opt_menu["menu"].delete(0, "end")
        for port in self.ports:
            self.port_opt_menu["menu"].add_command(label=port, command=tk._setit(self.port_selected, port))


    def _connect_device(self, event):
        comx = self.port_selected.get()
        self.mydevice.set_baudrate(int(self.mydevice.baudrate))
        self.mydevice.set_timeout(float(self.mydevice.timeout))
        self.mydevice.set_device(comx)
        self.txt_open.delete("1.0", "end")
        try:
            self.mydevice.open()
            self.txt_open.insert(tk.END, "Open succeed")
        except:
            self.txt_open.insert(tk.END, "Open failed")


    def _open_helppage(self, event):
        # ヘルプページを表示
        webbrowser.open("https://www.makuake.com/project/narrativelab")

    def _open_adpage(self, event):
        # 広告ページを表示
        webbrowser.open("https://www.makuake.com/project/narrativelab")


    def _get_selected_states(self):
        cmds = []
        for i in range(self.NUM_COMMAND):
            command = self.cmd_selected_list[i].get()
            if command != "None":  # Noneはデフォルト。コマンドセットしない
                if command == "Type":
                    _cmd = self.all_commands_dict[command]  # type
                    _str = self.entry_type_var_list[i].get()  # 入力されている文字列
                    # Type 禁止文字チェック
                    if any(word in _str for word in [";", ":", ","]):
                        print("Do not use ;:,")
                        mb.showinfo("Type Error", "[Type] Do not use ; : ,")
                        _str = _str.replace(";", "").replace(":", "").replace(",", "")
                    # Type 文字数上限チェック
                    if len(_str) > 64:
                        print("Maximun length is 64.")
                        mb.showinfo("Type Error", "[Type] Maximun length is 64.")
                        _str = _str[:64]
                    _cmd = _cmd + ":" + _str
                else:
                    _cmd = self.all_commands_dict[command]
                interval_sec = self.spn_selected_list[i].get()
                # スピンボックス 誤入力チェック
                try:
                    _ = int(interval_sec)
                except:
                    print("sec must be numbers")
                    mb.showinfo("sec Error", "[sec] (sec) must be numbers")
                    interval_sec = "32400"
                # スピンボックス 上限秒チェック
                if int(interval_sec) > 32400:
                    print("Maximun sec if 32400")
                    mb.showinfo("sec Error", "[sec] Maximun (sec) is 32400.")
                    interval_sec = "32400"
                interval_or_once = self.int_or_once_selected_list[i].get()
                cmd = _cmd + "," + interval_sec + "," + interval_or_once + ";"
                cmds.append(cmd)
        return cmds


    def _write_command(self, event):
        # 現在のオプションメニュー選択状況をコマンドにセット
        cmds = self._get_selected_states()
        try:
            # デバイスにメッセージを書き込み
            for cmd in cmds:
                self.mydevice.write_str(cmd)
                time.sleep(0.5)
            # 書き込み終了メッセージ
            self.mydevice.write_str("end;")
            time.sleep(0.5)
            mb.showinfo("Success", "Writing successful !!")
        except:
            mb.showinfo("Write Error", "Writing failed !! Device may not be connected.")


    def _stop_command(self, event):
        try:
            # 書き込み終了メッセージだけを送ることで、デバイス側のコマンドがすべてクリアされ、stop状態になる
            self.mydevice.write_str("end;")
            time.sleep(0.5)
            mb.showinfo("Success", "Stopping !!")
        except:
            mb.showinfo("Write Error", "Writing failed !! Device may not be connected.")


    def _set_command(self):
        # オプションメニューを作成しリストに登録する
        for _ in range(self.NUM_COMMAND):
            # 実行コマンドオプションメニュー
            cmd_selected = tk.StringVar()
            cmd_selected.set(self.cmd_list[0])
            opt = tk.OptionMenu(self.root, cmd_selected, *self.cmd_list)
            # 取得 cmd_selected.get()

            # 実行時間スピンボックス
            spn_selected = tk.StringVar()
            spn_selected.set("0")  # self.spn_selectedは文字列型
            spn_box = tk.Spinbox(self.root, textvariable=spn_selected, from_=0, to=32400, increment=1, width=10)
            # 取得 spn_selected.get()  # return str.

            # interval実行かonce実行かを選ぶオプションメニュー
            int_or_once = ["interval", "once"]
            int_or_once_selected = tk.StringVar()
            int_or_once_selected.set(int_or_once[0])
            int_or_once_opt = tk.OptionMenu(self.root, int_or_once_selected, *int_or_once)

            # Typeコマンドの時にだけ有効な文字列用エントリー
            entry_type_var = tk.StringVar()
            entry_type = tk.Entry(textvariable=entry_type_var, width=32)
            entry_type.insert(tk.END, "")
            # 取得 entry_type_var.get()

            # リストに登録
            self.cmd_selected_list.append(cmd_selected)
            self.opt_list.append(opt)
            self.spn_selected_list.append(spn_selected)
            self.spn_box_list.append(spn_box)
            self.int_or_once_selected_list.append(int_or_once_selected)
            self.int_or_once_opt_list.append(int_or_once_opt)
            self.entry_type_list_list.append(entry_type)
            self.entry_type_var_list.append(entry_type_var)


    def page(self):
        tk.Label(self.root, text="Initialize").grid(row=0)
        # ポート探索用ボタン
        self.btn_sp = tk.Button(text="Search ports")
        self.btn_sp.bind(self.click, self._search_ports)

        # 選択されたポートのデバイスと接続するボタン
        self.btn_connect = tk.Button(text="Connect")
        self.btn_connect.bind(self.click, self._connect_device)

        # イニシャライズのボタン表示
        self.btn_sp.grid(row=1, column=0)
        self.port_opt_menu.grid(row=1, column=1)
        self.btn_connect.grid(row=1, column=2)
        self.txt_open.grid(row=1, column=3)

        # 実行コマンド選択オプションメニュー作成
        self._set_command()

        # リストに登録されているインスタンスを表示
        tk.Label(self.root, text="Settings").grid(row=2)
        for i in range(self.NUM_COMMAND):
            self.opt_list[i].grid(row=3 + i, column=0)
            self.spn_box_list[i].grid(row=3 + i, column=1)
            tk.Label(self.root, text='sec').grid(row=3 + i, column=2)
            self.int_or_once_opt_list[i].grid(row=3 + i, column=3)
            self.entry_type_list_list[i].grid(row=3 + i, column=4)

        # 書き込みボタン
        self.btn_wc = tk.Button(text="Write")
        self.btn_wc.bind(self.click, self._write_command)
        self.btn_wc.grid(row=4 + self.NUM_COMMAND, columnspan=2, column=0)
        
        # ストップボタン
        self.btn_st = tk.Button(text="Stop")
        self.btn_st.bind(self.click, self._stop_command)
        self.btn_st.grid(row=4 + self.NUM_COMMAND, columnspan=2, column=1)

        # ウェブページ表示ボタン
        tk.Label(self.root, text="Web").grid(row=5 + self.NUM_COMMAND)
        # サンプルレシピボタン
        # スクリーンセーバーやログアウトを防ぐ
        # ログインを打つのが面倒
        # ログアウトされて保存していなかったファイルが失われる
        # 長時間のダウンロードが、止まってしまう
        # リモートデスクトップ接続が切れる
        # F5再読み込みマウスクリック
        # ログオフ
        # 電源切る
        # 上を押し続けてパスワードエンターでログイン
        # マウスクリックして画面スクショ保存
        # メール送信ボタン押す
        # メモを記入して名前を付けて保存
        self.btn_help = tk.Button(text="help")
        self.btn_help.bind(self.click, self._open_helppage)
        self.btn_ad = tk.Button(text="AD")
        self.btn_ad.bind(self.click, self._open_adpage)
        self.btn_help.grid(row=6 + self.NUM_COMMAND, column=0, columnspan=5)
        self.btn_ad.grid(row=6 + self.NUM_COMMAND, column=1, columnspan=5)


    def show(self):
        self.root.mainloop()


def main():

    tk = Tk()
    tk.page()
    tk.show()


if __name__ == "__main__":
    main()
