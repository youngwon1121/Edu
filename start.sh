echo '-------------------------------'
echo 'Run migrate'
echo '-------------------------------'
python ./manage.py migrate

echo '-------------------------------'
echo 'Run server'
echo '-------------------------------'
python -u ./manage.py runserver 0.0.0.0:8000