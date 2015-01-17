for %%f in (*.ui) do c:\python26\python.exe c:\Python26\Lib\site-packages\PyQt4\uic\pyuic.py %%f -x -o %%~nf_ui.py
pause
