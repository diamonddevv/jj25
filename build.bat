pyinstaller main.py -y ^
    --onedir ^
    --name "cap-itulate-v1.0.0" ^
    --add-data res:. ^
    --contents-directory res ^
    --windowed ^
    --icon promo/icon.ico