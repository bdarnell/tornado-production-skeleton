Overview
========

This is a skeletal example of one way to run a Tornado application in
production.  It currently covers running the application under 
[Supervisor](http://supervisord.org).  Future additions may include
automating initial setup and deploying new code (e.g. with 
[Fabric](http://fabfile.org)) and running multiple processes behind a proxy
(e.g. [nginx](http://nginx.org)).


Code layout
===========

`chat` directory
----------------

This is our application; it's just the chat demo from the Tornado
distribution.

`third_party` directory
-----------------------

This directory contains third-party modules we depend on, such as Tornado.
Including the module directly in the codebase ensures that updates to these
modules can be deployed as a single unit with the application code rather
than a separate step (note that this really only makes sense for pure-python
modules; C modules like pycurl are probably best managed externally).

Tornado is included as a git submodule; this means that after cloning this
repository you must run `git submodule update --init`, and re-run
`git submodule update` when the version of tornado being used has changed.

`sitecustomize.py`
-----------------

`sitecustomize.py` is the magic that makes the `third_party` directory
work (together with `.pth` files like `third_party/tornado.pth`).
Simply point your `PYTHONPATH` at the directory containing
`sitecustomize.py` and `third_party` will be added to the path
automatically. The magic that makes this work is the site module,
see http://docs.python.org/library/site.html. The site module is imported when
python is initialized, it appends site-specific paths to the module search
path.

`production` directory
----------------------

This directory contains scripts used for Supervisor and other production
services.


Setup instructions
==================

All of these steps should be run as the user the app will be running
as (except installing Supervisor).  

1. Install supervisor (e.g. `sudo easy_install supervisor`).  
2. Create directories: `mkdir -p ~/logs ~/apps/tornado-production-skeleton`
3. Make this directory available at 
   `~/apps/tornado-production-skeleton/current` (either copy it into that 
   location or use a symlink)
4. Set up supervisor files in `~`.  Note that `supervisord.conf` is a copy
   because it changes rarely and can be shared by multiple projects,
   while `chat.supervisor` is a symlink to the current code.
   `cp ~/apps/tornado-production-skeleton/current/production/supervisord.conf ~; ln -s apps/tornado-production-skeleton/current/production/chat.supervisor ~`
5. Run `supervisord` (in your home directory)


Usage notes
===========

* After each reboot, `supervisord` will need to be restarted.  (TODO: 
  instructions on making this happen automatically)
* Run `supervisorctl update` after any change to the supervisor config files.
  To restart the servers when the supervisor config files have not changed,
  use `supervisorctl restart chat:*`
* Use `supervisorctl status` to check on the status of the process.  Once
  the program starts its logs are written to `~/logs`, but if it crashes on
  startup you'll have to ask supervisor for the output: `supervisorctl tail 
  chat:chat-8000 stderr`
