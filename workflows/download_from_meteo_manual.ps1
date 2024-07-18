# main
cd D:\_CODING\py\weather_lk
git pull origin master
python workflows/download_from_meteo.py
ls C:\Users\ASUS\AppData\Local\Temp\weather_lk

# data
cd D:\_CODING\data\weather_lk
git pull origin data
cp -r C:\Users\ASUS\AppData\Local\Temp\weather_lk\pdf_meteo_gov_lk\* .

echo "* $(date) download_from_meteo_manual" >> update.log
git add .
git commit -m "🤖 $(date) - download_from_meteo_manual.yml"
git push origin data
