## Creating the worker and util files

### Learning Objectives

After completing this unit, you will be able to:

- Describe what background workers are.
- Describe use cases for background workers.
- Create and connect to a worker job queue.
- Move your blocking function to a separate file.
- Adjust your route to use your queue.

### What are background workers?

Background workers are separate dynos that perform work outside the web
application context. They are incredibly useful when you have work to do
that might cause the request to your web process to time out.

### When to use a background worker

If you are seeing H12 errors or other errors that indicate that something is
taking too long to finish, and you can't otherwise optimize away the error,
it's time to shift the time-consuming work to a worker queue.

It's important to identify what the blocking function is so you know what to
move in to your utility file. It is often a long file upload, database query,
report generation, etc. Or sometimes it's more than one of these at the same
time!

In the example project we're going to do now, it's simulating a lengthy
report generation and upload to s3.

### Set Up the Worker queue

In the previous Unit, we set up the ``redis-server`` locally as well as
provisioning it on Heroku. Now we will set up the worker queue to talk to
the Redis.

This project also assumes you have an AWS S3 bucket set up and you know how
to write to it with python. See the attached ``boto3_test.py``` if you need
tips on setting up S3.

(This bit is mostly stolen from https://devcenter.heroku.com/articles/python-rq
with a few changes to make it applicable to this project.)

#### Configuration

The Python library we need so Python can talk to Redis is called ``rq``.
It can be installed via pip.

```
$ pip install rq
$ pip freeze > requirements.txt
```

#### Create your worker file

Create a file calle ``worker.py``. Put the following code in it.

```python
import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
```

In order to test this file locally, you need to run the previously configured
``redis-server``. Fire it up in another shell, then go back to your project
directory and try to run ``python worker.py``. You will get errors if you
don't have the ``redis-server`` running.

### Queueing Jobs

Find the offending code that is causing the timeouts and shift it to a function
in a file called ``utils.py``.

#### Set up your ``utils.py`` file

In our example, we're using a function that makes and uploads reports that
looks like this:

```python
def make_report():
    """Upload to s3 function for use with the worker queue."""

    filename = make_pdf()
    file_contents = open(filename, 'rb').read()

    s3 = boto3.resource('s3')
    s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=file_contents)
    return
```

The ``make_pdf()`` function is in the sample code, or you can make your own.

#### Add the queue calls to your app

In your app, in this case a Flask app, you need to include the calls to
connect to the queue.

```python
from worker import conn

q = Queue(connection=conn)
```

Then add the call to add your new utility function to your Redis queue in
the appropriate place in your code.

```python
from utils import make_report

q.enqueue(make_report)
```

We will test and deploy this in the next unit.

### Resources

- [Background Tasks in Python with RQ](https://devcenter.heroku.com/articles/python-rq)

### Challenge

1) Which of the following are reasons you would need to use a background
worker?
    a) Long Database Queries
    b) Running Reports
    c) Uploading big files to cloud storage
    d) All of the above
