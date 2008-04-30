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
python wurfl2python.py wurfl/wurfl.xml -o wurfl.py
if (( $? )) ; then
  echo "Unable to create wurfl.py. "
  exit 1
fi

