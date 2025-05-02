import tkinter as tk
import subprocess
import os
import shutil
from tkinter import filedialog, ttk

# Create the main window
root = tk.Tk()

# Set the size of the window to 800x600
root.geometry('800x600')

# Set the background color to black
root.configure(bg='black')

# Create a label with the text "MOVESYNC"
label = tk.Label(root, text="MOVESYNC", font=('Times New Roman', 32), fg='white', bg='black')
label.pack()

# Create a StringVar to store the selected output folder
output_folder = tk.StringVar()

# Create a button that selects an output folder
def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder.set(folder_path)
        output_folder_label.config(text=f'Selected folder: {folder_path}')
        process_video_button.config(state='normal')

output_folder_button = tk.Button(root, text="Select output folder", command=select_output_folder, bg='white', font=('Arial', 18), relief='solid', bd=2, highlightbackground='black', activebackground='gray', padx=10, pady=10, borderwidth=5, cursor='hand2')
output_folder_button.pack(pady=20)

# Create a label to display the selected output folder
output_folder_label = tk.Label(root, text='', font=('Arial', 24), fg='white', bg='black')
output_folder_label.pack()

# Create a StringVar to store the selected video file
video_file = tk.StringVar()

# Create a button that opens a file dialog to select a video file
def select_video_file():
    file_path = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4 *.avi *.mkv')])
    if file_path:
        video_file.set(file_path)
        video_file_label.config(text=f'Selected file: {file_path}')
        process_video_button.config(state='normal')

video_file_button = tk.Button(root, text="Select video file", command=select_video_file, bg='white', font=('Arial', 18), relief='solid', bd=2, highlightbackground='black', activebackground='gray', padx=10, pady=10, borderwidth=5, cursor='hand2')
video_file_button.pack(pady=20)

# Create a label to display the selected video file name
video_file_label = tk.Label(root, text='', font=('Arial', 24), fg='white', bg='black')
video_file_label.pack()

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
progress_bar.pack(pady=20)

# Create a button that processes the selected video file
def process_video_file():
    video_file_path = video_file.get()
    output_folder_path = output_folder.get()
    output_path = os.path.join(output_folder_path, 'output.mp4')
    command = f"romp --mode=video --calc_smpl --render_mesh -i={video_file_path} -o={output_path} --save_video -t -sc=3"
    try:
        progress_bar.config(mode='indeterminate')
        progress_bar.start()
        subprocess.check_call(command, shell=True)
        progress_bar.stop()
        progress_bar.config(mode='determinate')
        progress_bar['value'] = 100
        output_video_file_label.config(text=f'Processed file: {output_path}')
        # Delete frames folder and files less than 9MB
        for root_dir, dirs,files in os.walk(output_folder_path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                if os.path.getsize(file_path) < 6 * 1024 * 1024:
                    os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root_dir, dir)
                if dir == 'frames':
                    shutil.rmtree(dir_path)
    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        print(f'Error: {e.output}')
        output_video_file_label.config(text='')
        process_video_button.config(state='normal')

process_video_button = tk.Button(root, text="Process video", command=process_video_file, bg='white', font=('Arial', 18), relief='solid', bd=2, highlightbackground='black', activebackground='gray', padx=10, pady=10, borderwidth=5, cursor='hand2', state='disabled')
process_video_button.pack(pady=20)

# Create a label to display the processed video file name
output_video_file_label = tk.Label(root, text='', font=('Arial', 24), fg='white', bg='black')
output_video_file_label.pack()

# Start the tkinter main loop
root.mainloop()