
$venvName="bot2"

Write-Host "Creation de l'environnement virtuel $venvName..."
& c:\Users\Biran\AppData\Local\Programs\Python\Python311\python.exe -m venv $venvName

Write-Host "Activation de l'environnement virtuel $venvName..."
& "$venvName\Scripts\Activate"

Write-Host "Installation des dependances depuis requirements.txt..."
& "$venvName\Scripts\pip" install -r requirements.txt

Read-Host -Prompt "Press Enter to exit"