# VisualDeploy
See your app's deployment progress in real-time!
## What is it?
Well, it's a webhook generator written in Python.  
You can use it to make an deployment webhook endpoint for your service.
# Install
Just type
```bash
pip install visualdeploy
```
And you're good to go!
# Usage 
First, you need to specify what commands visualdeploy will run.
```python
from visualdeploy import make_app

commands = [
  'cd ~',
  'git clone https://github.com/some/project',
  'cd project',
  'touch app.wsgi',
]
```
Then, you need to actually make an WSGI application.
```python
app = make_app(commands)
```
And save the file as `app.py`.  
# Deploy
Yes, you need to deploy an deployment webhook.  
As a simple solution, you can use [gunicorn](http://gunicorn.org/):
```bash
$ pip install gunicorn
$ gunicorn app:app --timeout 120 --bind 0.0.0.0:8000 -D
```
or other solutions such as mod_wsgi.
