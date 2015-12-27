## Heroku background worker test project

A quick Python demo project to show how to use Heroku worker processes to send
long processing jobs to the background and not have them beholden to the web
request. Web requests will timeout after 30 seconds, which can lead to
unpredictable or undesirable side effects.

I chose to use uploading of images to Amazon s3 as my background process. This
works great unless you're on a slow internet connection for uploads, then just
sending the file to the server before it even gets sent to s3 can timeout. I
deliberately didn't do a direct upload to s3 with JavaScript because I wanted
to go through the server. If you run it locally, then the only hangup is in the
upload to s3, but running on the remote server right now it's a crapshoot with
large files.

Although I'm using image upload to test, using a background worker process is
very well suited for dealing with databases, generating reports, making pdfs,
or anything that takes a while and is likely to time out a web request.

### You will need:

- Python
- Flask
- A local install of the Redis server
- A Heroku account and the Heroku toolbelt installed on your computer
- An Amazon AWS/s3 account

#### Step 1: Make a Flask app

Make yourself a very small Flask app, with a landing page, a page with a form
to upload from, and whereever you want to end up after the upload. Verify that
you can use Flask and the form to upload a file to your local filesystem. Send
it to /tmp or something.

#### Step 2: Test connection to s3

Setting up a user on AWS with their own credentials is a good idea here.
Download the user's access key and secret key to your local machine. You can
then use the AWS command line tools to set up a config that will work, but
you're going to want to store them as, and make sure they're working as,
environment variables, because we'll need to be able to do that later with
the Heroku config. It's also a good idea to store the bucket name as an
environment varaible because depending on how you set up your access rules for
the bucket, you might not want the name of your bucket going on GitHub or
anywhere public.

I tried a few different techniques for talking to s3, but eventually settled
on using their recommended boto3 library. I made a quick test file
(``boto3_test.py``) to make sure all my environment variables were set correctly
and used it to play around a little with what information I could get about
the bucket. I also used the test file to identify a couple files I already had
sitting around that would be good test cases.

#### Step 3: Fold s3 upload into Flask

Change the route you had been using to send uploads to your local file system
to now send the upload to s3. Did it work? Hooray!

#### Step 4: Deploy!

Now that we've got a Flask app that's uploading to s3, let's get it on Heroku.
We're still not dealing with the background processing yet, but now is a good
time to make sure that you can deploy and run on Heroku so that shifting to
a background worker won't be so difficult and will only be a small change
instead of trying to get everything running at once.

Make sure you use ``heroku config`` to set the environment variables you've been
using locally to match on Heroku. And don't forget to pip freeze >
requirements.txt so you have all the libraries you need. Your Procfile at this
point should just have a single web: line. Also remember to turn off debugging,
make the ports available, and set your host correctly.

Remember you can always use heroku local to test your local config before you
deploy. Is it working? Great!

#### Step 5: Set up Redis

I used this doc to get Redis up and running on my computer:
http://jasdeep.ca/2012/05/installing-redis-on-mac-os-x/ because I'm not a huge
fan of homebrew or macports. I want everything on my computer to be there for
a reason and I want to know what installed where.

#### Step 6: Set up the worker and queue

Here, I followed this doc pretty much word for word:
https://devcenter.heroku.com/articles/python-rq

Things to note:

- Check your ``heroku config`` for the correct Redis URL. Mine was different
than the one in the doc.
- You can't run ``worker.py`` locally unless you have redis-server running.

Just like in the doc, I moved the file upload to s3 in to a separate function
in a separate file called ``utils.py``, then included it in my ``app.py`` and
used the queueing function from rq to offload the upload to the worker process.
The worker.py file needed no modifications, I copied it word for word from the
doc.

#### Step 7: Add worker to Procfile

Edit the Procfile to include ``worker: python worker.py``. Start up a
redis-server locally and try running ``heroku local``. Do your pages load?
Can you upload a file to s3? Does it eventually show up in the bucket list?
Whoohoo! It worked!

#### Step 8: Deploy! (again)

If you didn't yet, now's the right time to provision Redis on Heroku. Once
provisioned, make sure the Redis URL (``heroku config``) is what you're pointed
toward in your ``worker.py``.

Commit and push to GitHub and Heroku.

Make sure you've got a worker dyno running ``heroku scale worker=1``

#### Step 9: Profit!
