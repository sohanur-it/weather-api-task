#Assessment WeatherAPI

<h4>
I've dockerized the project to seamlessly integrate multiple components: a Django app, a Redis server serving as a broker, Celery for asynchronous task management, and Celery Beat for scheduling periodic tasks. This setup efficiently handles various functionalities, such as fetching data from NewsAPI every 60 minutes and automatically saving any new data into the database
</h4>


Used Technolgies :
</h2>
<ul>
<li>Python</li>
<li>Django</li>
<li>Docker</li>
<li>Celery</li>
<li>Redis Server</li>
<li>POSTGRES</li>
</ul>

<h2>Build and Run Code:</h2>
<p>
docker-compose up --build -d
</p>
Now go to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a> 

<h2>API Documentation</h2>
<p>
http://127.0.0.1
</p>

<h2>
Features:
</h2>
<ul>
<li><b>Part-1 Done </b>
<br>
<u>127.0.0.1/api/find-coolest-district/</u><br>
</li>
<li>
<b>Part2 - Done </b>
<br>
<u>127.0.0.1/api/check-location/</u><br>

<h3>
SQLITE3 Superadmin Creds:
</h3>
<p>

username: admin <br>

password: admin123
</p>

</ul>
