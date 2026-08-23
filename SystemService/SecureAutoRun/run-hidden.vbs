' run-hidden.vbs
' Launches the autorun monitor completely hidden

Set WshShell = CreateObject("WScript.Shell")

psCommand = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -NoProfile -File ""C:\SecureAutoRun\autorun-monitor-trusted.ps1"""

WshShell.Run psCommand, 0, False