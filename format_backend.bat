@echo off
echo Formatting backend code with Black...
pip install black
black Backend/
echo Backend formatting complete.
