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
rm -rf "/home/makerpm/rpmbuild/malscan-release-1*"
rm -rf "/home/makerpm/rpmbuild/BUILD/***"
rm -rf "/home/makerpm/rpmbuild/BUILDROOT/***"
rm -rf "/home/makerpm/rpmbuild/SOURCES/***"

# Creating a temp working directory
TEMP=$(mktemp -d)
SOURCEDIR="$TEMP/malscan-release-$VERSION"
mkdir -p "$SOURCEDIR"

# Moving into the malscan directory
cd /home/makerpm/rpmbuild/malscan/rpm-build
git fetch
git pull
cd /home/makerpm/rpmbuild

## Creating the file structure for the SOURCE tarball
cp /home/makerpm/rpmbuild/malscan/rpm-build/malscan-el.repo "$SOURCEDIR/malscan.repo"

## Packaging the files
cd "$TEMP"
wget https://repo.malscan.org/RPM-GPG-KEY-Malscan --prefix "$SOURCEDIR/"
tar -czvf "$TEMP/malscan-release-$VERSION.tar.gz" "$SOURCEDIR"

# Moving the newly packaged files into the build sources directory
mv "$TEMP/malscan-release-$VERSION.tar.gz" "/home/makerpm/rpmbuild/SOURCES/"

## Copying the latest SPEC files from our git repo into SPECS
cp "/home/makerpm/rpmbuild/malscan/rpm-build/malscan-release.spec" "/home/makerpm/rpmbuild/SPECS/malscan-release.spec"

## Moving back into our pwd
cd /home/makerpm/rpmbuild

## Deleting the temp directory and all of its staging contents
rm -rf "$TEMP"

## Finishing up the source build
echo "Staging of all malscan files completed. Beginning build process."

## Creating the RPM
rpmbuild -ba /home/makerpm/rpmbuild/SPECS/malscan-release.spec
