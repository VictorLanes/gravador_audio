import pyaudio
import wave
import tkinter as tk
from tkinter import filedialog
import threading

class AudioRecorder:
    def __init__(self, root):
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.recording = False

        root.title("Gravador de Áudio")
        root.geometry("300x200")

        self.start_button = tk.Button(root, text="Iniciar Gravação", command=self.start_recording)
        self.start_button.pack(pady=20)

        self.stop_button = tk.Button(root, text="Parar Gravação", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        self.save_button = tk.Button(root, text="Salvar", command=self.save_audio, state=tk.DISABLED)
        self.save_button.pack(pady=20)

    def start_recording(self):
        self.frames = []  # Limpa os frames anteriores
        self.recording = True

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44000,
            input=True,
            frames_per_buffer=1024
        )

        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def record_audio(self):
        while self.recording:
            bloco = self.stream.read(1024)
            self.frames.append(bloco)

    def stop_recording(self):
        self.recording = False
        self.recording_thread.join()  # Espera até que a gravação seja concluída

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

        self.stream.stop_stream()
        self.stream.close()

    def save_audio(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Arquivos WAV", "*.wav")])
        if file_path:
            arquivo_final = wave.open(file_path, "wb")
            arquivo_final.setnchannels(1)
            arquivo_final.setframerate(44000)
            arquivo_final.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            arquivo_final.writeframes(b"".join(self.frames))
            arquivo_final.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioRecorder(root)
    root.mainloop()
