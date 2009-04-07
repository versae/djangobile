#!/bin/bash

rm djangobile.sqlite
touch djangobile.sqlite
if (( $? )) ; then
  echo "Unable to create database. Check Django does not running and try again."
  exit 1
fi

./manage.py syncdb
if (( $? )) ; then
  echo "Unable to create new schema (syncdb)."
  exit 1
fi

echo "Generating wurfl.py"
xsltproc --stringparam 'file' "wurfl_patch_2.xml" "wurfl/patch_wurfl.xsl" "wurfl/wurfl.xml" > "wurfl/wurfl_tmp.xml"
xsltproc --stringparam 'file' "wurfl_patch_1.xml" "wurfl/patch_wurfl.xsl" "wurfl/wurfl_tmp.xml" > "wurfl/wurfl_patched.xml"
xsltproc "wurfl/check_wurfl.xsl" "wurfl/wurfl_patched.xml"
rm wurfl/wurfl_tmp.xml
python wurfl2python.py wurfl/wurfl_patched.xml -o djangobile/wurfl.py
if (( $? )) ; then
  echo "Unable to create wurfl.py."
  exit 1
fi

