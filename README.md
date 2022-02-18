# messing-with-TwitterAPI

Warning: When cloning, create .env file in the working directory root with following variables 
(replace yourapikey with corresponding key you`ve got from Twitter):
```python
TWITTER_API_KEY=yourapikey
TWITTER_API_SECRET_KEY=yourapikey
TWITTER_BEARER_TOKEN=yourapikey
FLASK_SECRET_KEY=yourapikey
```
And don`t forget to install requirements.txt :)
```console
pip install -r requirements.txt
```
### Task 2: navigate_json.py
This file allows you to navigate json object, returned from Twitter API.
![image](https://user-images.githubusercontent.com/51854282/154634300-7ccae1d5-e419-411b-8979-fc45e662aa03.png)

### Task 3: web_app.py, webserver.py
I know you've always dreamed of seeing a locations map of following users of chosen user of Twitter!
Now it's working live on http://jetboom.pythonanywhere.com/, check it out. (will be online before May 2022)
![image](https://user-images.githubusercontent.com/51854282/154635217-596562b1-9464-48dc-815c-5183806b3b7d.png) 
![image](https://user-images.githubusercontent.com/51854282/154635669-ed1b1803-4866-4385-bbe7-5b09dafe16f5.png)
map of followings of Elon Musk
