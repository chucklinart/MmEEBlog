###  MmEEBlog setup instructions

 *First a caveat: Before you enable this app, make sure you're logged in to your Django admin site.*  You won't be 
  able to log in due to a missing relationship.  I'm trying to fix this bug, but it's a toughie. If anyone wants to help figure 
  out why get_or_create() does not work as it should (to auto-create the relationship for existing users in a 
  migration), I'm all ears.

  After you've enabled MmEEBlog, save all users.  This will create the relationship.

## Environment

 To use all features of MmEEBlog, your server environment needs a few things:

 - Ffmpeg
 - Redis
 - sox
 - libsox-fmt-mp3 
 - libsox-fmt-all 
 - mpg321 dir2ogg 
 - libav-tools

MmEEBlog will work without the above, but you won't be able to use the multimedia content types.

## Django Requirements

All of these are listed in /examples/requirements_example.txt  django-audiofield needed some adjustments so I forked it a 
little to make it work with Django>=2.1.  You can get the forked version at https://github.com/chucklinart/django-audiofield.git or just install 
with pip if you're on an older version of Django.

If you're on an older version of Django, you'll also have to change the syntax in the urls.py file to use path() instead of 
url().

## Installation -- MAKE SURE YOU ARE LOGGED IN to the ADMIN SECTION BEFORE DOING THIS 

*Working examples of settings.py, supervisor.conf, requirements.txt, and the redis_worker file that starts the Redis worker are in
/examples directory if you want to save yourself the trouble of figuring it out yourself... or maybe you can come up with 
something different and better!*

1) Place the mmeeblog directory in your project's root or wherever you place apps.  Just clone the git repo or whatever.
2) Make suggested changes to your settings.py file (examples/settings.py_example
3) Get the forked audiofield app from my Github and place it where your project's apps live
   ( https://github.com/chucklinart/django-audiofield.git )
4) Configure your Redis settings to match whatever you put in the settings.py file
   https://redis.io/topics/config 
5) Configure supervisor per examples/supervisor.conf_example 
6) Restart supervisor (sudo service supervisor restart), Redis, and your project and web servers

You should see everything in the admin section, and it should be working splendidly. 

I did leave static files in the repo, but I would expect you'd want to change those to suit your needs.  Instead of 
extending base.html, in the MmEEBlog templates you should extend whatever you usually extend and load your own front 
end stuff that way.

There are still a lot of TODOs here, like adding a real streaming video format so people can live stream from their own 
sites and stuff like that.  If you want to contribute, let me know through my github.

Happy hacking!


