sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/default
mv /home/box/stepic_web_project/web /home/box/
sudo pip3 install django==1.11.9
sudo pip3 install gunicorn
cd /home/box/web/ask
gunicorn -c '/home/nikita/projects/Course/stepik_web/gunic/gunicorn-django.py' ask.wsgi:application &
cd /home/box/stepic_web_project/gunic/
gunicorn -c gunicorn-wsgi.py hello:app &
sudo /etc/init.d/nginx restart
