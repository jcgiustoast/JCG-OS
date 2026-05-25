' Launches the Telegram inbox bot hidden (no console window).
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\jcgiu\JCG-OS\.telegram-inbox"
WshShell.Run "pythonw bot.py", 0, False
