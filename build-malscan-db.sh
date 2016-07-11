#!/bin/bash
# -------------------------------------------------
#
# Package: Malscan
# Author: Josh Grancell <josh@joshgrancell.com>
# Description: Linux malware scanner for web servers
# Copyright: 2015-2016 Josh Grancell
# License: MIT License
# 
# -------------------------------------------------

VERSION="$1"
RELEASE="$2"

# Deleting everything
rm -rf "/home/makerpm/rpmbuild/malscan-db-1*"
rm -rf "/home/makerpm/rpmbuild/BUILD/***"
rm -rf "/home/makerpm/rpmbuild/BUILDROOT/***"
rm -rf "/home/makerpm/rpmbuild/SOURCES/***"

# Creating a temp working directory
TEMP=$(mktemp -d)
mkdir -p "$TEMP/malscan-db-$VERSION"

## Creating the file structure for the SOURCE tarball
rsync -avzP /home/makerpm/rpmbuild/malscan/malscan-db/ "$TEMP/malscan-db-$VERSION/"

## Packaging the files
cd "$TEMP"
tar -czvf "$TEMP/malscan-db-$VERSION.tar.gz" "malscan-db-$VERSION"

# Moving the newly packaged files into the build sources directory
mv "$TEMP/malscan-db-$VERSION.tar.gz" "/home/makerpm/rpmbuild/SOURCES/"

## Copying the latest SPEC files from our git repo into SPECS
cp "/home/makerpm/rpmbuild/malscan/rpm-build/malscan-db.spec" "/home/makerpm/rpmbuild/SPECS/malscan-db.spec"

## Moving back into our pwd
cd /home/makerpm/rpmbuild

## Deleting the temp directory and all of its staging contents
rm -rf "$TEMP"

## Finishing up the source build
echo "Staging of all malscan-db files completed. Beginning build process."

## Creating the RPM
rpmbuild -ba /home/makerpm/rpmbuild/SPECS/malscan-db.spec

## Doing the RPM signing
rpm --define="%_gpg_name Josh Grancell <josh@joshgrancell.com>" --resign "/home/makerpm/rpmbuild/RPMS/noarch/malscan-db-$1-$2.noarch.rpm"
