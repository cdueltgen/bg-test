## Creating the worker and util files

### Learning Objectives

After completing this unit, you will be able to:

- Describe what background workers are.
- Describe use cases for background workers.
- Create and connect to a woker job queue.
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
provisioning it on Heroku.