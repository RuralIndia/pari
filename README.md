<h1>Pari</h1>


P.Sainath's People's Archive Of Rural India


Dev Setup
==========

* clone the repo.
* if you are using virtualenvwrapper, create a virtual env.
<pre>
mkvirtualenv pari
workon pari
</pre>
* Install the dependencies
<pre>
pip install -r requirements.txt
</pre>
* Setup the database
<pre>
python manage.py syncdb --all
python manage.py migrate --fake
manage setup.py runserver
</pre>

<b>Note:</b> Add these to your .bash_profile if you are getting "unknown locale: UTF-8" error
<pre>
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
</pre>
