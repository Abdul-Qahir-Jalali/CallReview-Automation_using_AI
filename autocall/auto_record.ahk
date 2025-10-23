; Press Ctrl+Q to start recording
^q::

    ; 1. Route system audio to VB-Cable (playback device)
    ;Run, nircmd setdefaultsounddevice "CABLE Input (VB-Audio Virtual Cable)" 0  ; Main playback device
    ;Run, nircmd setdefaultsounddevice "CABLE Input (VB-Audio Virtual Cable)" 1  ; Communication playback

    





    Run, nircmd setdefaultsounddevice "CABLE Input" 0  ; Main playback device
    Run, nircmd setdefaultsounddevice "CABLE Input" 1  ; Communication playback



    ; NEW: Clear contents of audio_temp folder before recording
    FileDelete, D:\call\autocall\audio_temp\*.*
    



    ; 2. Start recording from VB-Cable (recording device)
    ;Run, ffmpeg -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -ac 1 -ar 16000 "D:\call\autocall\audio_temp\rec.wav", , Hide


    Run, ffmpeg -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -ac 1 -ar 16000 "D:\call\autocall\audio_temp\rec.wav", , Hide
    
    ; 3. Notification
    ToolTip, Recording started... Press Ctrl+W to stop
    SetTimer, RemoveToolTip, 3000
return

; Press Ctrl+W to stop and process
^w::
    ; 4. Stop recording
    Run, nircmd killprocess ffmpeg.exe
    
    ; 5. Restore original audio devices (replace with your actual device names)
    ;    Check your playback devices in sound settings to confirm names
    
    
    Run, nircmd setdefaultsounddevice "Speakers" 0
    Run, nircmd setdefaultsounddevice "Speakers" 1

    ;Run, nircmd setdefaultsounddevice "%OriginalDevice%" 0
    ;Run, nircmd setdefaultsounddevice "%OriginalDevice%" 1

    Run, nircmd setdefaultsounddevice "Realtek HD Audio 2nd output" 0  ; Uncomment if different
    Run, nircmd setdefaultsounddevice "Realtek HD Audio 2nd output" 1  ; Uncomment if different
    

    Run, nircmd setdefaultsounddevice "Headphones" 0  ; Uncomment if different
    Run, nircmd setdefaultsounddevice "Headphones" 1  ; Uncomment if different




    ; restore microphone
    Run, nircmd setdefaultsounddevice "Microphone Array (Intel® Smart Sound Technology (Intel® SST))" 2
    Run, nircmd setdefaultsounddevice "Microphone Array (Intel® Smart Sound Technology (Intel® SST))" 3

    Run, nircmd setdefaultsounddevice "Headset (soundcore R50i)" 2
    Run, nircmd setdefaultsounddevice "Headset (soundcore R50i)" 3


    




    ; 6. Transcribe audio
    ;RunWait, C:\Users\user\anaconda3\envs\call\python.exe D:\call\transcribe_audio.py
    SetWorkingDir, D:\call


    RunWait, %ComSpec% /c C:\Users\user\anaconda3\envs\call\python.exe D:\call\transcribe_audio.py > D:\call\autocall\transcripts\log.txt 2>&1
    Run, http://127.0.0.1:5000


    
    ; 7. Cleanup
    Sleep, 10000
    ToolTip, done done done done done!
    SetTimer, RemoveToolTip, 2000
return

RemoveToolTip:
    SetTimer, RemoveToolTip, Off
    ToolTip
return