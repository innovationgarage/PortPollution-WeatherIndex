#! /bin/sh

while true; do
  python3 -u /add_grib_to_index.py 1>&2
    
  now="$(date +%s)"
  nextScrape="$((($now / (3600*4) + 1) * 3600*4))"
  waitTime="$(($nextScrape - $now))"
  sleep "$waitTime"
done
