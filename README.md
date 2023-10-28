# spotify-podcast-viz



# Setup
1. Get access to your personal server: https://docs.google.com/document/d/1WhGPj32ukYWc-v9qEs1WmMqofmXIKm0bniJs7tG19dI/edit
2. Go into your w209 folder and clone this repo. The directory should look something like this

w209/
...
...
w209.py
start.wsgi
spotify-podcast-viz/
...

3. Update start.wsgi to point to spotify-podcast-viz folder

Example:
```
import os, sys

PROJECT_DIR = '/home/tijayant/w209/spotify-podcast-viz'

activate_this = '/home/tijayant/w209/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.append(PROJECT_DIR)

from w209 import app as application
```

4. You should have the flask app from spotify-podcast-viz running by hitting /w209 path
example: https://apps-fall.ischool.berkeley.edu/~tijayant/w209/

