import os
import sys
import pygrib
import psycopg2
import shapely.geometry
import numpy as np
import json

"""
create table gribfiles (
 file varchar primary key
);
create table measurement (
 measurementid varchar primary key,
 parameterName varchar,
 typeOfLevel varchar,
 level integer
);
create table griblayers(
  file varchar references gribfiles(file),
  measurementid varchar references measurement(measurementid),
  timestamp timestamp,
  gridid varchar references gridareas(gridid));
create index on griblayers(timestamp);
"""

conn = psycopg2.connect(os.environ["DATABASE"])
cur = conn.cursor()

basedir = os.environ["BASEDIR"]



for root, dirs, files in os.walk(basedir):
    for filename in files:
        try:
            if not (filename.endswith(".grib") or filename.endswith(".grb")): continue
            filepath = os.path.join(root, filename)
            cur.execute("SELECT count(*) FROM gribfiles WHERE file = %s",
                         (filepath,))
            if cur.fetchone()[0] > 0:
                print("%s IGNORE" % filepath)
                continue
            print("%s INDEX" % filepath)
            cur.execute("INSERT INTO gribfiles (file) VALUES (%s)",
                         (filepath,))
            with pygrib.open(filepath) as grbs:
                for grb in grbs:
                    lats, lons = grb.latlons()

                    coords = np.concatenate((
                        np.concatenate((lons[:,0:1], lats[:,0:1]), axis=1),
                        np.concatenate((np.transpose(lons[-1:,:]), np.transpose(lats[-1:,:])), axis=1),
                        np.concatenate((lons[::-1,-1:], lats[::-1,-1:]), axis=1),
                        np.concatenate((np.transpose(lons[0:1,::-1]), np.transpose(lats[0:1,::-1])), axis=1)))

                    poly = {'type': 'Polygon',
                            'coordinates': [coords],
                            "crs":{"type":"name","properties":{"name":"EPSG:4326"}}}
                    poly = shapely.geometry.shape(poly).simplify(0.05)

                    if "Dx" in grb.keys():
                        dx = grb.Dx
                    else:
                        dx = grb.Di
                    if "Dy" in grb.keys():
                        dy = grb.Dy
                    else:
                        dy = grb.Dj
                    x = grb.longitudeOfFirstGridPoint
                    y = grb.latitudeOfFirstGridPoint
                    w = dx * grb.Nx
                    h = dy * grb.Ny

                    gridid = ",".join(["%s=%s" % (a, b) for (a, b) in sorted(grb.projparams.items())]
                                      + [str(item) for item in (x, y, w, h)])
                    measurementid = "%s,%s,%s" % (grb.parameterName, grb.typeOfLevel, grb.level)

                    cur.execute("INSERT INTO gridareas (gridid, projparams, the_geom) VALUES (%s, %s, st_geomfromtext(%s, 4326)) ON CONFLICT DO NOTHING",
                                (gridid, json.dumps(grb.projparams), poly.wkt))

                    cur.execute("INSERT INTO measurement (measurementid, parameterName, typeOfLevel, level) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                                (measurementid, grb.parameterName, grb.typeOfLevel, grb.level))

                    cur.execute("INSERT INTO griblayers (file, measurementid, timestamp, gridid) VALUES (%s, %s, %s, %s)",
                                (filepath, measurementid, grb.validDate, gridid))

            cur.execute("COMMIT")
        except Exception as e:
            print("%s: %s" % (filename, e))
            
