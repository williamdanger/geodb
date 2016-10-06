# Flask + PostGIS Test

This is a simple API in front of a PostGIS-enabled Postgresql DB using Flask.  A couple of notes
for later if I want to reproduce this in the future.

Using OS X, so everything is for that.

Although there is a separate `requirements.txt` file for installing everything and should work
in general, I split the packages out into sections just to talk more aobut them.

## Database Setup

### Data File

The data is from http://download.geonames.org/export/dump/.  I include it here because I'd rather
have the repo be complete than force yet another download.

### Install Postgres.app

It contains all the Postgresql + PostGIS installed.  Alternatively, you could also run an RDS
instance on AWS, but we're going for free toys.

### Install psycopg2

As far as I can tell, it's the go-to Postgresql driver for Python. Some
fun gotchas for vanilla `pip install psycopg2` include the following:

  * Add `pg_config` to your path: Since this is actually building as part of the install, you'll
   have to add the Postgres.App bins to your path.  They're located at
   `/Applications/Postgres.app/Contents/Versions/9.5/bin/` for the current version (as of 9/2016).

  * Install/Update Xcode's CLI: El Capitan seems to have added the ability for multiple XCode
   installs a la `nvm`, but it completely hoses anything trying to use the CLI even if you had it
   previously.  So you may need to do a `xcode-select --install`.

### Install SQLAlchemy

It's the go-to ORM.  `pip install sqlalchemy`

### Install GeoAlchemy2

This adds the bits for simple PostGIS in SQLAlchemy using the ORM: `pip install geoalchemy2`

### Seed the database

Since Postgres.app uses the default user as superuser, everything around the seeding process uses
that to make a new superuser for enabling the extension as well as connecting to Postgres itself.

In the `db/` folder, simply run `seedDB.py`.  It'll take a minute or two.  You can drop everything
with `cleanDB.py`.

## REST API Setup

### Install Flask

This is the normal `pip install flask`.  Nothing special.

### Install Simple Swagger Support

Since the easiest way to test a UI is Swagger support, let's make this easy.  Since it runs on
annotations and doesn't use YAML, `flask-restful-swagger` seems like the best way to go.  Also,
`flask-restful` makes API declaration pretty easy.


## Post notes

[See this post](http://gitblog.pandelyon.com/technical/flask/postgresql/2016/10/06/geodb.html)
