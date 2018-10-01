# PortPollution-WeatherIndex

This project indexes a directory tree of grib files of weather reports into a postgis database.

You must set up the postgis database outside of this docker container, create the tables manually and point this container to it
by setting `DATABASE` to a postgres connection string in `.env`.

See [GribUtils](https://github.com/innovationgarage/gributils/blob/master/gribindex.sql) for the create table statements.
