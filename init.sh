sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
mv /home/box/stepic_web_project/web /home/box/
rm /home/box/web/ask/db.sqlite3
python3 /home/box/web/ask/manage.py makemigrations
python3 /home/box/web/ask/manage.py migrate
sudo pip3 install django==1.11.9
sudo pip3 install gunicorn
cd /home/box/web/ask
gunicorn -c '/home/box/stepic_web_project/gunic/gunicorn-django.py' ask.wsgi:application &
cd /home/box/stepic_web_project/gunic/
rm /home/box/web/ask sb.sqlite3
python3 /home/box/web/ask/manage.py makemigrations
python3 /home/box/web/ask/manage.py migrate
gunicorn -c gunicorn-wsgi.py hello:app &
sudo /etc/init.d/nginx restart
sudo /etc/init.d/mysql start
