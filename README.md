# IITG_Dashboard

## Django WebApp && ReactNative MobileApp

1. It includes a dashboard in which a user can create pages and becomes the admin of that page , then other users can subscribe to 
that pages and the app notifies them about any events created or posted on that page.
2. Users can also add events to their **Google Calender** by clicking on *Add to my Calender* button.


## Install Dependencies

For Django WebApp

```
pip3 install requests
sudo apt install django
pip3 install httplib2
pip3 install google_api_python_client
```



To install django.
Note: Use sudo only if some errors pop up.

```
sudo pip3 install -r requirements.txt
```

Finally run

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

in the directory which has manage.py to get your site up and running.

For MobileApp

```
npm install -g react-native-cli
npm install -g expo-cli
```
Finally run following command to run the mobileApp

```
cd <directory>
expo start
```
## Screenshots

![Screenshot 1](https://github.com/codervivek/iitg_dashboard/blob/master/1.png "Create Event")
Creating an Event

![Screenshot 2](https://github.com/codervivek/iitg_dashboard/blob/master/2.png "Dashboard")
list of events created

![Screenshot 3](https://github.com/codervivek/iitg_dashboard/blob/master/3.png "Dashboard")
Event automatically made in google calendar


