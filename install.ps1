
$venvName="bot2"

Write-Host "Creation de l'environnement virtuel $venvName..."
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name.Split("\")[1]
$pythonPath = "c:\Users\$currentUser\AppData\Local\Programs\Python\Python311\python.exe"
& $pythonPath -m venv $venvName

Write-Host "Activation de l'environnement virtuel $venvName..."
& "$venvName\Scripts\Activate"

Write-Host "Installation des dependances depuis requirements.txt..."
& "$venvName\Scripts\pip" install -r requirements.txt

Read-Host -Prompt "Press Enter to exit"