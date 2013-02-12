pari
====

Sainath's People's Archive Of Rural India


Dev Setup
==========

* clone the repo.
* if you are using virtualenvwrapper, create a virtual env.
<pre>
mkvirtualenv pari
workon pari
</pre>
* pip install -r requirements.txt
* manage setup.py runserver
* add these to your .bash_profile if you are getting "unknown locale: UTF-8" error
<pre>
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
</pre>
