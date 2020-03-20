# Flask + PostGIS Test

This is a simple API in front of a PostGIS-enabled Postgresql DB using Flask.  A couple of notes
for later if I want to reproduce this in the future.

A hosted version of this with only US cities is running at http://geodb.pandelyon.com/

Using OS X, so everything is for that.

Although there is a separate `requirements.txt` file for installing everything and should work
in general, I split the packages out into sections just to talk more about them.


# System requirements

If you're looking to run this locally, this is developed against:

* Python 2.7
* Postgres 9.5 (via Postgres.app)


# Local Development

## Install and Run
After you've done the prerequisite "Clone and setup any virtual environments", do the following:

* Start a new instance of default Postgres (e.g. 5432, postgres default user)
* Execute the following

```
pip install -r requirements.txt  # Python dependencies
python seedDB.py                 # Seed the DB with Geodata
python app/main.py               # Start Flask running in debug mode
```

## Using the app

By default, Flask will run on `localhost:5000`.  Assuming that's the case (You'll see it in the logs if not),
you can interact with the app on the following routes:

* `http://localhost:5000/`: Basic sanity test.  Returns `{"status": "ok"}` if the app is running.
* `http://localhost:5000/city/{cityId}/neighbor/`: Performs a search for the given city, returning the nearest cities.  Make sure to include the trailing slash!
* `http://localhost:5000/api/spec.json`: OpenAPI spec for the application in JSON format
* `http://localhost:5000/api/spec.html`: Interactive OpenAPI spec for the application

Note the city search doesn't work in this UI, so you'll need to do searches with `curl` on the command line for now.

If you would like some sample cities, see:
* San Francisco: 5391959
* Seattle: 5809844
* Shreveport: 4341513
* St. Petersburg: 498817
* Solothurn: 2658564
* Swindon: 2636388


## Database Notes

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

## REST API Notes

### Flask

This is the normal `pip install flask`.  Nothing special.

### Swagger Support

Since the easiest way to test a UI is Swagger support, let's make this easy.  Since it runs on
annotations and doesn't use YAML, `flask-restful-swagger` seems like the best way to go.  Also,
`flask-restful` makes API declaration pretty easy.


## Blog Post notes

[See this post](http://play.pandelyon.com/technical/flask/postgresql/2016/10/06/geodb.html)
