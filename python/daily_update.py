import fetch_hrrr
import sub_grib

# To be run on a cron-job, actually probably run hourly
# although the file is named 'daily'

def get_new_data(dt, data_dir):
  # Fetch the latest HRRR data
  # Turn it into a sub-grib
  # Add entries to the database for all locations

  # (somehow) if time has not already been downloaded...
  file_name = fetch_hrrr.download_time(dt)
  sub_file = sub_grib.create_sub(file_name, data_dir)
  pass

