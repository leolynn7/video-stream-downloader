# Video Stream Downloader GUI 🎥

A modern, user-friendly Python GUI application for downloading video streams (m3u8, mp4, etc.) directly to your computer. This tool wraps the power of FFmpeg in a sleek interface to handle downloads efficiently.

## ✨ Features

* **Modern UI:** Dark theme interface built with Tkinter.
* **Easy to Use:** Paste URL, choose a filename, and download.
* **Real-time Progress:** Visual progress bar and percentage indicator.
* **Log Viewer:** Live output logs from FFmpeg to troubleshoot issues.
* **Smart Parsing:** Auto-detects filenames and video duration.

## 📺 Supported Formats

This tool is designed to handle various video stream protocols and file types. Based on the FFmpeg engine, it supports:

* **HLS Streams:** `.m3u8` (Most common for streaming sites)
* **Video Files:** `.mp4`, `.mkv`, `.avi`
* **Others:** Generally supports any direct stream URL that FFmpeg can process.

*Note: All downloaded videos are automatically saved as **.mp4** for maximum compatibility.*

## 🛠️ Requirements

Before running the application, please ensure you have the following installed:

1.  **Python 3.x**
2.  **FFmpeg** (CRITICAL: FFmpeg must be installed and added to your system's PATH).

## 🚀 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com:leolynn7/video-stream-downloader.git
    cd video-stream-downloader
    ```

2.  **Install FFmpeg:**
    * **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/), extract it, and add the `bin` folder to your System Environment Variables.
    * **Mac:** `brew install ffmpeg`
    * **Linux:** `sudo apt install ffmpeg`

3.  **Run the application:**
    ```bash
    python3 video_stream_downloader.py
    ```

## 📝 How to Use

1.  Copy the video stream URL (e.g., `.m3u8` link).
2.  Click **Paste URL** or type it manually.
3.  (Optional) Change the output filename and save location.
4.  Click **⬇️ Download Video**.
5.  Watch the progress bar and logs for status.

## 👤 Author

Created by **Leo Lynn**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
