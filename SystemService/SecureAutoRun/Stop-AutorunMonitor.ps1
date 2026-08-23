# Double-click this file to stop the background monitor


$StopFile = "C:\SecureAutorun\stop.txt"


New-Item -Path $StopFile -ItemType File -Force | Out-Null


Write-Host "Stop signal sent. The monitor will shut down within 10 seconds." -ForegroundColor Green
Start-Sleep -Seconds 3
