
=== Requirements
This uses a virtual environment, so execute source venv/bin/activate before doing the following

1. Install flask (pip install flask)
2. pygrib must be installed (https://code.google.com/p/pygrib/wiki/LinuxMacInstallation)
    - Brew install grib-api (1.12.3_1)
3. Other python dependencies include
  - pyproj
  - pygrib
  - numpy
  - matplotlib


=== Basic Testing

python harness.py

 - Creates a SQLite database in current dir test.db
 - Fills with data
 - Plots temps from Katahdin

== Overview

This uses flask to publish a simple web application that shows one page with a map and place markers.
When a place marker is selected, a time-series of temperature, snow fall, and wind speed is shown. The
flask code is in weather.py, it uses sqlalchemy to access time series data from record_db.py.  Records
are populated asynchronously, using code in update.py.  The cron.sh script will do this.

Configuration for foreman is in .env.  The update script downloads GRIB files from NOAA, extracts temperature,
wind speed, and snowfall at desired locations, and inserts the records into a database.
