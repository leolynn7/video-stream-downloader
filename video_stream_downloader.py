import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import re
from datetime import datetime

class VideoStreamDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Stream Downloader")
        self.root.geometry("750x650")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(True, True)
        
        # Theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.secondary_bg = "#2d2d30"
        self.entry_bg = "#3e3e42"
        self.button_bg = "#0e639c"
        self.creator_color = "#00bcd4"
        self.clear_button_color = "#d32f2f"
        
        # Variables
        self.url_var = tk.StringVar()
        self.filename_var = tk.StringVar(value="output")
        self.output_path_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.is_downloading = False
        self.process = None
        self.total_duration = None
        self.start_time = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title Section
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(pady=(0, 10))
        
        title_label = tk.Label(
            title_frame, 
            text="Video Stream Downloader", 
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        # Creator label
        creator_label = tk.Label(
            title_frame,
            text="Created by Leo Lynn",
            font=("Segoe UI", 10, "italic"),
            bg=self.bg_color,
            fg=self.creator_color
        )
        creator_label.pack()
        
        # URL Section
        url_frame = tk.Frame(main_frame, bg=self.bg_color)
        url_frame.pack(fill="x", pady=(10, 15))
        
        url_label = tk.Label(
            url_frame,
            text="Video Stream URL:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        url_label.pack(anchor="w", pady=(0, 5))
        
        # URL entry with buttons frame
        url_entry_frame = tk.Frame(url_frame, bg=self.bg_color)
        url_entry_frame.pack(fill="x", pady=(0, 10))
        
        # URL entry
        url_entry = tk.Entry(
            url_entry_frame,
            textvariable=self.url_var,
            font=("Segoe UI", 10),
            bg=self.entry_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat"
        )
        url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        url_entry.bind("<Return>", lambda e: self.start_download())
        
        # Buttons frame for Paste and Clear
        url_buttons_frame = tk.Frame(url_entry_frame, bg=self.bg_color)
        url_buttons_frame.pack(side="right")
        
        # Paste URL button
        paste_btn = tk.Button(
            url_buttons_frame,
            text="📋 Paste URL",
            command=self.paste_url,
            font=("Segoe UI", 9),
            bg=self.button_bg,
            fg=self.fg_color,
            activebackground="#1177bb",
            activeforeground=self.fg_color,
            relief="flat",
            cursor="hand2",
            width=12
        )
        paste_btn.pack(side="left", padx=(0, 5))
        
        # Clear button
        clear_btn = tk.Button(
            url_buttons_frame,
            text="🗑️ Clear",
            command=self.clear_fields,
            font=("Segoe UI", 9),
            bg=self.clear_button_color,
            fg=self.fg_color,
            activebackground="#b71c1c",
            activeforeground=self.fg_color,
            relief="flat",
            cursor="hand2",
            width=8
        )
        clear_btn.pack(side="left")
        
        # Filename Section
        filename_frame = tk.Frame(main_frame, bg=self.bg_color)
        filename_frame.pack(fill="x", pady=(0, 15))
        
        filename_label = tk.Label(
            filename_frame,
            text="Output Filename (without extension):",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        filename_label.pack(anchor="w", pady=(0, 5))
        
        filename_entry_frame = tk.Frame(filename_frame, bg=self.bg_color)
        filename_entry_frame.pack(fill="x")
        
        filename_entry = tk.Entry(
            filename_entry_frame,
            textvariable=self.filename_var,
            font=("Segoe UI", 10),
            bg=self.entry_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat"
        )
        filename_entry.pack(side="left", fill="x", expand=True)
        
        ext_label = tk.Label(
            filename_entry_frame,
            text=".mp4",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        ext_label.pack(side="left", padx=(5, 0))
        
        # Output Path Section
        path_frame = tk.Frame(main_frame, bg=self.bg_color)
        path_frame.pack(fill="x", pady=(0, 15))
        
        path_label = tk.Label(
            path_frame,
            text="Save Location:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        path_label.pack(anchor="w", pady=(0, 5))
        
        path_entry_frame = tk.Frame(path_frame, bg=self.bg_color)
        path_entry_frame.pack(fill="x")
        
        path_entry = tk.Entry(
            path_entry_frame,
            textvariable=self.output_path_var,
            font=("Segoe UI", 10),
            bg=self.entry_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat"
        )
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            path_entry_frame,
            text="📁 Browse",
            command=self.browse_output_path,
            font=("Segoe UI", 9),
            bg=self.button_bg,
            fg=self.fg_color,
            activebackground="#1177bb",
            activeforeground=self.fg_color,
            relief="flat",
            cursor="hand2",
            width=10
        )
        browse_btn.pack(side="left")
        
        # Progress Section
        progress_frame = tk.Frame(main_frame, bg=self.bg_color)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to download",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg="#cccccc"
        )
        self.progress_label.pack(anchor="w", pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=100
        )
        self.progress_bar.pack(fill="x", pady=(0, 5))
        self.progress_bar["value"] = 0
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar",
                        thickness=20,
                        background=self.accent_color,
                        troughcolor=self.secondary_bg,
                        bordercolor=self.bg_color,
                        lightcolor=self.accent_color,
                        darkcolor=self.accent_color)
        
        # Progress percentage label
        self.progress_percent_label = tk.Label(
            progress_frame,
            text="Progress: 0%",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.progress_percent_label.pack(anchor="w")
        
        # Download Button
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill="x", pady=(10, 20))
        
        self.download_btn = tk.Button(
            button_frame,
            text="⬇️ Download Video",
            command=self.start_download,
            font=("Segoe UI", 12, "bold"),
            bg=self.button_bg,
            fg=self.fg_color,
            activebackground="#1177bb",
            activeforeground=self.fg_color,
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.download_btn.pack()
        
        # Status Display
        status_frame = tk.Frame(main_frame, bg=self.secondary_bg, relief="flat", height=150)
        status_frame.pack(fill="both", expand=True, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        # Status label
        status_label = tk.Label(
            status_frame,
            text="Download Log:",
            font=("Segoe UI", 10, "bold"),
            bg=self.secondary_bg,
            fg="#cccccc"
        )
        status_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Text widget for status with scrollbar
        text_frame = tk.Frame(status_frame, bg=self.secondary_bg)
        text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.status_text = tk.Text(
            text_frame,
            bg="#252526",
            fg="#cccccc",
            font=("Consolas", 9),
            wrap="word",
            relief="flat",
            height=8
        )
        self.status_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for status text
        scrollbar = tk.Scrollbar(text_frame, command=self.status_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.status_text.config(yscrollcommand=scrollbar.set)
        
    def paste_url(self):
        # Paste URL from clipboard
        try:
            # Get clipboard content
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                self.url_var.set(clipboard_text)
                self.update_status("URL pasted from clipboard")
        except tk.TclError:
            messagebox.showwarning("Clipboard Error", "Cannot access clipboard or clipboard is empty")
    
    def clear_fields(self):
        # Clear all input fields
        self.url_var.set("")
        self.filename_var.set("output")
        self.output_path_var.set(os.path.expanduser("~/Downloads"))
        self.status_text.delete(1.0, tk.END)
        self.progress_bar["value"] = 0
        self.progress_percent_label.config(text="Progress: 0%")
        self.progress_label.config(text="Ready to download")
        self.update_status("All fields cleared")
        
    def browse_output_path(self):
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_path_var.get()
        )
        if directory:
            self.output_path_var.set(directory)
    
    def update_status(self, message):
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
        self.root.update_idletasks()
    
    def extract_filename_from_url(self, url):
        # Extract filename from URL
        try:
            match = re.search(r'/([^/?]+)\.(m3u8|mp4|mkv|avi)', url)
            if match:
                filename = match.group(1)
                filename = re.sub(r'[^\w\-_]', '_', filename)
                return filename[:50]
        except:
            pass
        return "output"
    
    def parse_duration(self, duration_str):
        # Parse duration string to seconds
        try:
            parts = duration_str.split(':')
            if len(parts) == 3:
                hours = float(parts[0])
                minutes = float(parts[1])
                seconds = float(parts[2])
                return hours * 3600 + minutes * 60 + seconds
        except:
            pass
        return None
    
    def update_progress(self, current_time_str, duration_str):
        # Update progress bar and percentage
        try:
            current_seconds = self.parse_duration(current_time_str)
            total_seconds = self.parse_duration(duration_str)
            
            if current_seconds is not None and total_seconds is not None and total_seconds > 0:
                progress_percent = (current_seconds / total_seconds) * 100
                
                # Cap at 100%
                if progress_percent > 100:
                    progress_percent = 100
                
                # Update progress bar
                self.progress_bar["value"] = progress_percent
                
                # Update percentage label
                self.progress_percent_label.config(
                    text=f"Progress: {progress_percent:.1f}%"
                )
                
                # Force UI update
                self.root.update_idletasks()
                
        except Exception as e:
            print(f"Progress update error: {e}")
    
    def extract_progress_info(self, line):
        # Extract progress information from FFmpeg output
        time_match = re.search(r'time=(\d+:\d+:\d+\.\d+)', line)
        duration_match = re.search(r'Duration: (\d+:\d+:\d+\.\d+)', line)
        
        if duration_match:
            self.total_duration = duration_match.group(1)
        
        if time_match and self.total_duration:
            current_time = time_match.group(1)
            self.update_progress(current_time, self.total_duration)
    
    def start_download(self):
        if self.is_downloading:
            messagebox.showwarning("Warning", "A download is already in progress!")
            return
            
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL!")
            return
        
        # Auto-extract filename from URL
        if self.filename_var.get() == "output" and url:
            extracted_name = self.extract_filename_from_url(url)
            if extracted_name != "output":
                self.filename_var.set(extracted_name)
        
        output_dir = self.output_path_var.get()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except:
                messagebox.showerror("Error", "Cannot create output directory!")
                return
        
        filename = self.filename_var.get().strip()
        if not filename:
            filename = "output"
        
        # Add .mp4 extension if not present
        if not filename.lower().endswith('.mp4'):
            filename += '.mp4'
        
        output_file = os.path.join(output_dir, filename)
        
        # Check if file already exists
        if os.path.exists(output_file):
            response = messagebox.askyesno(
                "File Exists", 
                f"'{filename}' already exists. Overwrite?"
            )
            if not response:
                return
        
        # Reset progress
        self.progress_bar["value"] = 0
        self.progress_percent_label.config(text="Progress: 0%")
        self.total_duration = None
        self.start_time = None
        
        # Start download
        self.is_downloading = True
        self.download_btn.config(text="Downloading...", state="disabled")
        self.progress_label.config(text=f"Downloading: {filename}")
        self.update_status(f"Starting download: {filename}")
        self.update_status(f"URL: {url[:80]}...")
        self.update_status(f"Output: {output_file}")
        self.update_status("-" * 50)
        
        # Start download thread
        thread = threading.Thread(
            target=self.download_video,
            args=(url, output_file),
            daemon=True
        )
        thread.start()
    
    def download_video(self, url, output_file):
        try:
            # Create FFmpeg command
            command = [
                'ffmpeg',
                '-i', url,
                '-c', 'copy',
                '-y',
                output_file
            ]
            
            self.update_status(f"Command: {' '.join(command)}")
            self.update_status("Download started...")
            
            # Start process
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output in real-time
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    line = line.strip()
                    self.update_status(line)
                    self.extract_progress_info(line)
            
            # Wait for process to complete
            self.process.wait()
            
            if self.process.returncode == 0:
                self.update_status("Download completed successfully!")
                self.progress_bar["value"] = 100
                self.progress_percent_label.config(text="Progress: 100%")
                self.progress_label.config(text=f"Download completed: {os.path.basename(output_file)}")
                messagebox.showinfo("Success", f"Video downloaded successfully!\nSaved to: {output_file}")
            else:
                self.update_status(f"Download failed with error code: {self.process.returncode}")
                self.progress_label.config(text="Download failed")
                messagebox.showerror("Error", "Download failed. Check the status log for details.")
                
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.is_downloading = False
            self.process = None
            self.download_btn.config(text="⬇️ Download Video", state="normal")
    
    def on_closing(self):
        if self.is_downloading and self.process:
            response = messagebox.askyesno(
                "Confirm Exit", 
                "A download is in progress. Are you sure you want to exit?"
            )
            if response:
                try:
                    self.process.terminate()
                except:
                    pass
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = VideoStreamDownloader(root)
    
    # Set window icon if available
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()