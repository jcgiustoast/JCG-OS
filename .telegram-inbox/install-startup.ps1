$startup = [Environment]::GetFolderPath('Startup')
$lnk = Join-Path $startup 'JCG-OS Telegram Inbox.lnk'
$shell = New-Object -ComObject WScript.Shell
$s = $shell.CreateShortcut($lnk)
$s.TargetPath = 'C:\Users\jcgiu\Documents\JCG-OS\.telegram-inbox\run-silent.vbs'
$s.WorkingDirectory = 'C:\Users\jcgiu\Documents\JCG-OS\.telegram-inbox'
$s.Save()
Write-Host "Shortcut created: $lnk"
