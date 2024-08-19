# main
cd D:\_CODING\py\weather_lk
git checkout main
git pull origin main
python workflows/download_from_meteo.py
python workflows/parse_all.py
python workflows/build_summaries.py
# ls C:\Users\ASUS\AppData\Local\Temp\weather_lk

# data
cd D:\_CODING\data\weather_lk
git checkout data
git pull origin data

cp C:\Users\ASUS\AppData\Local\Temp\weather_lk\pdf_meteo_gov_lk\*.pdf pdf_meteo_gov_lk\
cp C:\Users\ASUS\AppData\Local\Temp\weather_lk\*.* .

echo "* $(date) _pipeline_manual" >> update.log
git add .
git commit -m "🤖 $(date) - _pipeline_manual.yml"
git push origin data


# back
cd D:\_CODING\py\weather_lk
git checkout main
firefox_open https://github.com/nuuuwan/weather_lk/blob/data/README.md