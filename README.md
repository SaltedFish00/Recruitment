**way to start:**  
python3 ./manage.py runserver 0.0.0.0:8000 --settings=settings.local  
**packages**
pip3 install django-grappelli  
pip3 install DingtalkChatbot  
pip3 install django-bootstrap4  

dingtalk usage:  
python3 manage.py shell --settings=settings.local
from interview import dingtalk
dingtalk.send("招聘开始")