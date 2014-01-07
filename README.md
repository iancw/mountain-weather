
=== Requirements

1. Django must be installed (pip install Django)
2. pygrib must be installed (https://code.google.com/p/pygrib/wiki/LinuxMacInstallation)
    - Brew install grib-api
    - Install pyproj (I'm using 1.9.3)
    - Install pygrib (using 1.9.8)

=== Download data from NOAA

(edit download.py line 28 with appropriate minimum time)
mkdir data
python
>> import download
>> download.download_history()
(this will take awhile, and fill the data directory you create with grib files)

=== Initialize Database

python manage.py shell
import conditions.populate


