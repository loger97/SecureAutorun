#Certificate file
$TrustFileName = "trust.txt"
$StopFile = "C:\SecureAutoRun\stop.txt"

# Allows external drive scaning
$IncluedExternalDrives = $true

#TrustHash, for code execution this must be the same on external drive.
$RequiredTrustHash = "9b2d1a2fab125347df0e07ea7e1ef4eedd6b1c76da863ab4e32aec7216982a43"

$seen = @{}

Write-Host "Trusted Autorun Monitor started at $(Get-Date)"

while ($True) {
    #Check for stop signal
    if (Test-Path $StopFile){
        Write-Host "Stop signal recived. Shutting down..."
        Remove-Item $StopFile -Force -ErrorAction SilentlyContinue
        break
    }

    try {
        # Build drive filter
        if ($IncludeExternalDrives) {
            $filter = "DriveType=2 OR DriveType=3"
        } else {
            $filter = "DriveType=2"
        }


        $drives = Get-CimInstance -ClassName Win32_LogicalDisk -Filter $filter


        # Clean up seen entries for drives that are no longer connected
        $currentInfPaths = $drives | ForEach-Object { 
            (Join-Path $_.DeviceID "autorun.inf").ToLower() 
        }
        $keysToRemove = $seen.Keys | Where-Object { 
            $_ -notin $currentInfPaths -and $_ -notlike "ignored_*" 
        }
        foreach ($key in $keysToRemove) {
            $seen.Remove($key)
        }


        foreach ($drive in $drives) {
            $root = $drive.DeviceID + "\"
            $infPath = Join-Path $root "autorun.inf"
            $trustPath = Join-Path $root $TrustFileName


            if (Test-Path $infPath) {
                $infItem = Get-Item $infPath -ErrorAction SilentlyContinue
                if (-not $infItem) { continue }


                $key = $infPath.ToLower()
                $lastWrite = $infItem.LastWriteTimeUtc


                # Trust check (with optional content validation for added security)
                $hasValidTrust = $false
                if (Test-Path $trustPath) {
                    if ([string]::IsNullOrWhiteSpace($RequiredTrustHash)) {
                        # Original behavior: any trust.txt is accepted
                        $hasValidTrust = $true
                    } else {
                        try {
                            $trustContent = Get-Content $trustPath -Raw -ErrorAction Stop
                            if ($trustContent -and $trustContent.ToLower().Contains($RequiredTrustHash.ToLower())) {
                                $hasValidTrust = $true
                            }
                        } catch {
                            # Silently ignore read errors; treat as invalid
                        }
                    }
                }


                if (-not $hasValidTrust) {
                    if (-not $seen.ContainsKey("ignored_$key")) {
                        if (Test-Path $trustPath) {
                            Write-Host "Ignored $($drive.DeviceID) � trust.txt found but missing required security text"
                        } else {
                            Write-Host "Ignored $($drive.DeviceID) � no trust.txt found"
                        }
                        $seen["ignored_$key"] = $true
                    }
                    continue
                }


                if (-not $seen.ContainsKey($key) -or $seen[$key] -ne $lastWrite) {
                    Write-Host "Processing trusted drive: $($drive.DeviceID) ($($drive.VolumeName))"


                    # Simple INI parser
                    $ini = @{}
                    $currentSection = ""
                    Get-Content $infPath | ForEach-Object {
                        $line = $_.Trim()
                        if ($line -match '^\[(.+)\]$') {
                            $currentSection = $matches[1].ToLower()
                            $ini[$currentSection] = @{}
                        }
                        elseif ($line -match '^([^=;]+)=(.*)$' -and $currentSection) {
                            $k = $matches[1].Trim().ToLower()
                            $v = $matches[2].Trim()
                            $ini[$currentSection][$k] = $v
                        }
                    }


                    $autorun = $ini['autorun']
                    if ($autorun) {
                        $toRun = $autorun['open']
                        if (-not $toRun) { $toRun = $autorun['shellexecute'] }


                        if ($toRun) {
                            $toRun = $toRun.Trim('"', "'")
                            $fullPath = Join-Path $root $toRun


                            if (Test-Path $fullPath) {
                                Start-Process -FilePath $fullPath -WorkingDirectory $root
                            }
                        }
                    }
                    $seen[$key] = $lastWrite
                }
            }
        }
    } catch {
        Write-Warning $_
    }


    Start-Sleep -Seconds 5
}


Write-Host "Autorun Monitor has stopped cleanly."
