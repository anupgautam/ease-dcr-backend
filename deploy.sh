cd /root/home/ease-dcr/ease-dcr-backend/
git pull
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
