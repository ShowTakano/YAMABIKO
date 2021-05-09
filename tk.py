import tkinter as tk

# pip install pyserial
import serial
from serial.tools import list_ports

import webbrowser


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

    def set_send_msg(self, send_msg):
        self.send_msg = bytes([send_msg])
        print("self.send_msg is ", self.send_msg)

    def write_send_msg(self):
        print("sending msg")
        self.serial.write(self.send_msg)
        print("send succeed", self.send_msg)

    def read_msg(self):
        print("read msg")
        incomming_str = self.serial.read()
        incomming_int = int.from_bytes(incomming_str, "big")
        print("incomming data", incomming_int, type(incomming_int))
        self.received_msg = incomming_int


class Tk():
    def __init__(self):
        # arduino
        self.arduino = SerialDevice()

        # 画面初期化
        self.root = tk.Tk()
        self.root.title("Arduino")
        self.root.geometry("640x480")

        self.click = "<Button-1>"

    def _search_devices(self, event):
        ports = self.arduino.get_list_ports()
        msg = ""
        for port in ports:
            msg = msg + port + "\n"
        print(msg)
        self.txt_sd.insert(tk.END, msg)

    def _search_devices_delete(self, event):
        self.txt_sd.delete("1.0", "end")

    def _open_device(self, event):
        comx = self.entry_comx_var.get()
        baudrate = self.entry_baudrate_var.get()
        timeout = self.entry_timeout_var.get()
        print(comx, baudrate, timeout)
        self.arduino.set_baudrate(int(baudrate))
        self.arduino.set_timeout(float(timeout))
        self.arduino.set_device(comx)
        self.txt_open.delete("1.0", "end")
        try:
            self.arduino.open()
            self.txt_open.insert(tk.END, "open succeed")
        except:
            self.txt_open.insert(tk.END, "open failed")

    def _set_serial_msg(self, event):
        if self.check_1_var.get() is True:
            print("self.check_1_var is True")
            self.arduino.set_send_msg(1)
        elif self.check_2_var.get() is True:
            print("self.check_2_var is True")
            self.arduino.set_send_msg(2)
        elif self.check_3_var.get() is True:
            print("self.check_3_var is True")
            self.arduino.set_send_msg(3)
        elif self.check_4_var.get() is True:
            print("self.check_4_var is True")
            self.arduino.set_send_msg(4)
        elif self.check_5_var.get() is True:
            print("self.check_5_var is True")
            self.arduino.set_send_msg(5)
        else:
            print("All self.check_x_var are False")

    def _write_serial_msg(self, event):
        self.arduino.write_send_msg()

    def _read_serial_msg(self, event):
        self.arduino.read_msg()

    def _open_webpage(self, event):
        webbrowser.open("https://www.makuake.com/project/narrativelab")

    def page(self):
        # デバイス探索結果描画用テキストボックス
        self.txt_sd = tk.Text(width=40, height=2)
        # デバイス探索ボタン
        self.btn_sd = tk.Button(text="search devices")
        self.btn_sd.bind(self.click, self._search_devices)
        # デバイス探索結果削除ボタン
        self.btn_sd_delete = tk.Button(text="clear")
        self.btn_sd_delete.bind(self.click, self._search_devices_delete)
        # COM用エントリー
        self.entry_comx_var = tk.StringVar()
        self.entry_comx = tk.Entry(textvariable=self.entry_comx_var)
        self.entry_comx.insert(tk.END, "COMx")
        # ボーレート用エントリー
        self.entry_baudrate_var = tk.StringVar()
        self.entry_baudrate = tk.Entry(textvariable=self.entry_baudrate_var)
        self.entry_baudrate.insert(tk.END, self.arduino.baudrate)
        # timeout用エントリー
        self.entry_timeout_var = tk.StringVar()
        self.entry_timeout = tk.Entry(textvariable=self.entry_timeout_var)
        self.entry_timeout.insert(tk.END, self.arduino.timeout)
        # デバイスopen結果描画用テキストボックス
        self.txt_open = tk.Text(width=40, height=1)
        # デバイスopenボタン
        self.btn_open = tk.Button(text="open")
        self.btn_open.bind(self.click, self._open_device)
        # チェックボタン
        self.check_1_var = tk.BooleanVar()
        self.check_1_var.set(False)
        self.check_1 = tk.Checkbutton(text="1", variable=self.check_1_var)
        # チェックボタン
        self.check_2_var = tk.BooleanVar()
        self.check_2_var.set(False)
        self.check_2 = tk.Checkbutton(text="2", variable=self.check_2_var)
        # チェックボタン
        self.check_3_var = tk.BooleanVar()
        self.check_3_var.set(False)
        self.check_3 = tk.Checkbutton(text="3", variable=self.check_3_var)
        # チェックボタン
        self.check_4_var = tk.BooleanVar()
        self.check_4_var.set(False)
        self.check_4 = tk.Checkbutton(text="4", variable=self.check_4_var)
        # チェックボタン
        self.check_5_var = tk.BooleanVar()
        self.check_5_var.set(False)
        self.check_5 = tk.Checkbutton(text="5", variable=self.check_5_var)
        # チェックボタン値取得
        self.btn_set = tk.Button(text="set")
        self.btn_set.bind(self.click, self._set_serial_msg)
        # 送信
        self.btn_send_msg = tk.Button(text="send")
        self.btn_send_msg.bind(self.click, self._write_serial_msg)
        # 受信
        self.btn_read_msg = tk.Button(text="read")
        self.btn_read_msg.bind(self.click, self._read_serial_msg)
        # ウェブ
        self.btn_web = tk.Button(text="web")
        self.btn_web.bind(self.click, self._open_webpage)

        # 表示順序
        self.btn_sd.pack()
        self.txt_sd.pack()
        self.btn_sd_delete.pack()
        self.entry_comx.pack()
        self.entry_baudrate.pack()
        self.entry_timeout.pack()
        self.btn_open.pack()
        self.txt_open.pack()
        self.check_1.pack()
        self.check_2.pack()
        self.check_3.pack()
        self.check_4.pack()
        self.check_5.pack()
        self.btn_set.pack()
        self.btn_send_msg.pack()
        self.btn_read_msg.pack()
        self.btn_web.pack()

    def show(self):
        self.root.mainloop()


def main():

    tk = Tk()
    tk.page()
    tk.show()


if __name__ == "__main__":
    main()
