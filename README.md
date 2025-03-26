# 🎶 LSL Slicer 🎶

Welcome to **LSL Slicer**! This **insanely simple** application is designed to help you slice audio files into 30-second mono WAV clips, specifically encoded for use in **Second Life** using FFmpeg.

## 🐍 To execute the script using Python:
1. **Clone the Repository**:
```
git clone https://github.com/Denveous/LSL-Slicer.git
cd LSL-Slicer
```

3. **Run the Application**:
   ```python slicer.py --log```
   * The `--log` option enables logging to a file for troubleshooting.

## 💾 Download the Executable

If you prefer not to run the script using Python, you can download the precompiled executable file directly from the Releases page:

https://github.com/Denveous/LSL-Slicer/releases/download/Windows/slicer.exe

Simply download the latest version and run it on your system.

* LSL Slicer will look for the folder "convert" in the same directory as the application, if not it'll prompt you for the directory.

## 📋 Second Life audio clip requirements:

To ensure your audio files work seamlessly with Second Life, they must meet the following criteria:

- **Format**: WAV files in standard PCM format.
- **Bit Depth**: 16-bit.
- **Sample Rate**: 44.1 kHz.
- **Channel**: Mono format (stereo will be automatically converted to mono).
- **Length**: 30 seconds or less (or more precisely: 1,323,000 samples or less).

For more information on sound clips in Second Life, check out the [Second Life Sound Clips Wiki](https://wiki.secondlife.com/wiki/Sound_Clips).

## 🎤 Credits

This project uses FFmpeg for audio processing. For more information, visit the [FFmpeg Homepage](https://ffmpeg.org/) or check out [FFmpeg on github](https://github.com/FFmpeg/FFmpeg).

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.
