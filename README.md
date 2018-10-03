# PortPollution-WeatherIndex

This project indexes a directory tree of grib files of weather reports into a postgis database.

You must set up the postgis database outside of this docker container, create the tables manually and point this container to it
by setting `DATABASE` to a postgres connection string in `.env`.

If using Python3, you also need to add the following lines in `.env`.
      
    LC_ALL="C.UTF-8"
    LANG="C.UTF-8"

See [GribUtils](https://github.com/innovationgarage/gributils/blob/master/gribindex.sql) for the create table statements.
