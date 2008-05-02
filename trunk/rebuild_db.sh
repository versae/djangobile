#!/bin/bash

rm djangobile.sqlite
touch djangobile.sqlite
if (( $? )) ; then
  echo "Unable to create database. Check Django does not running and try again."
  exit 1
fi

./manage.py syncdb
if (( $? )) ; then
  echo "Unable to create new schema (syncdb). "
  exit 1
fi

echo "Generating wurfl.py"
python wurfl2python.py djangobile/wurfl/wurfl.xml -o djangobile/wurfl.py
if (( $? )) ; then
  echo "Unable to create wurfl.py. "
  exit 1
fi

