import os
import sys
import subprocess
import shutil
import logging
import time
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from pathlib import Path
import threading
import argparse

parser = argparse.ArgumentParser(description='Audio Slicer Application')
parser.add_argument('--log', action='store_true', help='Enable logging to a file')
args = parser.parse_args()

log_file = Path(os.path.dirname(os.path.abspath(sys.argv[0]))) / 'slicer.log'

if args.log:
    if log_file.exists():
        log_file.unlink() 
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

application_dir = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
convert_dir = application_dir / 'convert'

if not convert_dir.exists():
    convert_dir = Path(filedialog.askdirectory(title="Select Source Folder for Audio Files"))
    if not convert_dir:
        messagebox.showerror("Error", "No folder selected. Exiting application.")
        sys.exit()

sliced_dir = application_dir / 'sliced'
sliced_dir.mkdir(exist_ok=True)
rsc_dir = Path(os.path.dirname(os.path.abspath(__file__))) / 'rsc'
ffmpeg_path = rsc_dir / 'ffmpeg'

supported_formats = ['*.mp3', '*.wav', '*.flac', '*.aac', '*.ogg', '*.m4a']

def log_message(message):
    if args.log:
        logging.info(message)
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, message + '\n')
    output_text.see(tk.END)
    output_text.config(state=tk.DISABLED)

def clear_sliced_directory():
    for item in sliced_dir.iterdir():
        shutil.rmtree(item) if item.is_dir() else item.unlink()

def slice_audio(file_path, current_file_index, total_files):
    base_name = file_path.stem
    song_dir = sliced_dir / base_name
    song_dir.mkdir(exist_ok=True)
    output_parts = []
    part_number = 1
    duration = 30
    result = subprocess.run([str(ffmpeg_path), '-i', str(file_path)], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    
    try:
        duration_line = result.stderr.split('Duration: ')[1].split(',')[0].strip()
        hours, minutes, seconds = map(float, duration_line.split(':'))
        total_seconds = int(hours * 3600 + minutes * 60 + seconds)
    except IndexError:
        log_message(f"Could not find duration in FFmpeg output for {file_path.name}.")
        return
    
    total_parts = (total_seconds // duration) + (1 if total_seconds % duration > 0 else 0)

    for start in range(0, total_seconds, duration):
        output_file = song_dir / f"{base_name}.part{part_number}.wav"
        ffmpeg_command = [str(ffmpeg_path), '-i', str(file_path), '-ss', str(start), '-t', str(duration), 
                          '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '1', str(output_file)]
        ffmpeg_result = subprocess.run(ffmpeg_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        log_message(f"Slicing file {current_file_index}/{total_files}, part {part_number} out of {total_parts} for {file_path.name}...")
        
        output_parts.append(output_file.name)
        part_number += 1
    
    with open(song_dir / f"{base_name}.parts", 'w') as f:
        f.write(f"{len(output_parts)}")

def run_slicing():
    clear_sliced_directory()
    audio_files = []
    for fmt in supported_formats:
        audio_files.extend(convert_dir.glob(fmt))
    
    total_files = len(audio_files)
    log_message(f"Found {total_files} supported audio files to slice.")

    for index, audio_file in enumerate(audio_files, start=1):
        slice_audio(audio_file, index, total_files)
        output_text.update_idletasks()
        time.sleep(1)
    
    log_message("Conversion complete. The window will close automatically in 10 seconds.")
    root.after(10000, root.destroy)

def start_slicing_thread():
    threading.Thread(target=run_slicing, daemon=True).start()  

root = tk.Tk()
root.title("LSL Slicer Output")
root.geometry("900x200")
root.minsize(900, 200)
root.resizable(False, False)

root.configure(bg='#2E2E2E') 
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg='#1E1E1E', fg='white', insertbackground='white')
output_text.pack(expand=True, fill='both')
output_text.config(state=tk.DISABLED)

log_message("Preparing conversion...")
root.after(5000, start_slicing_thread)
root.mainloop()