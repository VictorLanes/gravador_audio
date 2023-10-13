import cv2
import keyboard
import pyautogui
import numpy as np
import tkinter as tk
from tkinter import filedialog
from time import time, strftime, localtime
import threading
import pyaudio

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravador de Tela com Áudio")

        self.recording = False
        self.video = None
        self.audio_stream = None
        self.audio_frames = []
        self.start_time = 0
        self.play_speed = 1  # Velocidade de reprodução inicial

        self.start_button = tk.Button(root, text="Iniciar Gravação", command=self.start_recording)
        self.stop_button = tk.Button(root, text="Parar Gravação", command=self.stop_recording)
        self.save_button = tk.Button(root, text="Salvar Gravação", command=self.save_recording)
        self.display_label = tk.Label(root, text="Tempo de gravação: 00:00:00", font=("Helvetica", 16))
        self.speed_label = tk.Label(root, text="Velocidade: 1x")
        self.change_format_button = tk.Button(root, text="Alterar Formato", command=self.toggle_format)

        self.start_button.pack()
        self.stop_button.pack()
        self.save_button.pack()
        self.display_label.pack()
        self.speed_label.pack()
        self.change_format_button.pack()
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)

        self.video_format = "avi"  # Formato inicial

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.start_time = 0  # Começa o tempo do zero
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.DISABLED)
            self.video = cv2.VideoWriter("video." + self.video_format, cv2.VideoWriter_fourcc(*"XVID"), 30, pyautogui.size())
            self.audio_frames = []
            self.audio_stream = self.setup_audio_stream()
            self.root.after(100, self.update_time)
            self.record_thread = threading.Thread(target=self.record_screen)
            self.record_thread.start()

    def setup_audio_stream(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, output=True, frames_per_buffer=1024)
        return stream

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.NORMAL)
            self.video.release()
            self.display_label.config(text="Tempo de gravação: 00:00:00")
            self.play_speed = 1
            self.speed_label.config(text="Velocidade: 1x")
            self.audio_stream.stop_stream()
            self.audio_stream.close()

    def record_screen(self):
        while self.recording:
            frame = pyautogui.screenshot()
            frame = np.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.video.write(frame)
            audio_data = self.audio_stream.read(1024)
            self.audio_frames.append(audio_data)
            if keyboard.is_pressed("esc"):
                self.stop_recording()
        cv2.destroyAllWindows()

    def update_time(self):
        if self.recording:
            current_time = time() - self.start_time
            formatted_time = strftime("%H:%M:%S", localtime(current_time))
            self.display_label.config(text="Tempo de gravação: " + formatted_time)
            self.root.after(1000, self.update_time)

    def save_recording(self):
        if self.video is not None:
            save_path = filedialog.asksaveasfilename(defaultextension="." + self.video_format, filetypes=[("Arquivos " + self.video_format.upper(), "*." + self.video_format)])
            if save_path:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
                self.combine_audio_video(save_path)
                self.save_button.config(state=tk.DISABLED)

    def combine_audio_video(self, output_path):
        audio_data = b''.join(self.audio_frames)
        audio_len = len(audio_data) // 4
        cap = cv2.VideoCapture("video." + self.video_format)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4)))

        for i in range(audio_len):
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                out.write(np.frombuffer(audio_data, dtype='int16', count=2))
            else:
                break

        cap.release()
        out.release()

    def toggle_format(self):
        if self.video_format == "avi":
            self.video_format = "mp4"
        else:
            self.video_format = "avi"
        self.change_format_button.config(text="Formato: " + self.video_format.upper())

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
