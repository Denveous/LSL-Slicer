@echo off
REM Cleanup old nuitka-crash-report.xml
if exist nuitka-crash-report.xml del nuitka-crash-report.xml

REM Compile the Python script with Nuitka  --remove-output 
nuitka --onefile --standalone --windows-icon-from-ico=slicer.ico --windows-console-mode=disable --enable-plugin=tk-inter --output-dir=./ --output-filename=slicer.exe --include-data-file="rsc/ffmpeg.exe=rsc/ffmpeg.exe" --msvc=latest slicer.py --show-progress
pause
