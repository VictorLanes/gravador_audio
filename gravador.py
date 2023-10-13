import pyaudio
import wave
import tkinter as tk
from tkinter import filedialog
import threading

class AudioRecorder:
    def __init__(self, root):
        # Inicialização da classe AudioRecorder
        self.audio = pyaudio.PyAudio()  # Inicializa o PyAudio para lidar com áudio
        self.frames = []  # Armazenará os quadros de áudio
        self.recording = False  # Variável para controlar o estado da gravação

        # Configuração da janela principal
        root.title("Gravador de Áudio")
        root.geometry("300x200")

        # Botão para iniciar a gravação
        self.start_button = tk.Button(root, text="Iniciar Gravação", command=self.start_recording)
        self.start_button.pack(pady=20)

        # Botão para parar a gravação
        self.stop_button = tk.Button(root, text="Parar Gravação", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        # Botão para salvar a gravação
        self.save_button = tk.Button(root, text="Salvar", command=self.save_audio, state=tk.DISABLED)
        self.save_button.pack(pady=20)

    def start_recording(self):
        # Iniciar a gravação
        self.frames = []  # Limpa os frames anteriores
        self.recording = True

        # Atualiza o estado dos botões
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)

        # Inicia o fluxo de áudio com as configurações especificadas
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44000,
            input=True,
            frames_per_buffer=1024
        )

        # Inicia uma thread para gravar áudio em segundo plano
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.start()

    def record_audio(self):
        # Função que grava áudio enquanto a gravação estiver ativa
        while self.recording:
            bloco = self.stream.read(1024)
            self.frames.append(bloco)

    def stop_recording(self):
        # Parar a gravação
        self.recording = False
        self.recording_thread.join()  # Espera até que a gravação seja concluída

        # Atualiza o estado dos botões
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

        # Encerra o fluxo de áudio
        self.stream.stop_stream()
        self.stream.close()

    def save_audio(self):
        # Salva a gravação de áudio em um arquivo WAV
        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Arquivos WAV", "*.wav")])
        if file_path:
            arquivo_final = wave.open(file_path, "wb")
            arquivo_final.setnchannels(1)
            arquivo_final.setframerate(44000)
            arquivo_final.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            arquivo_final.writeframes(b"".join(self.frames))
            arquivo_final.close()

if __name__ == "__main__":
    # Cria uma instância da classe AudioRecorder e inicia a interface gráfica
    root = tk.Tk()
    app = AudioRecorder(root)
    root.mainloop()
