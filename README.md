
=== Requirements

1. Django must be installed (pip install Django)
2. pygrib must be installed (https://code.google.com/p/pygrib/wiki/LinuxMacInstallation)
    - Brew install grib-api
    - Install pyproj (I'm using 1.9.3)
    - Install pygrib (using 1.9.8)

=== Basic Testing

python harness.py

 - Creates a SQLite database in current dir test.db
 - Fills with data
 - Plots temps from Katahdin

