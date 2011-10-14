#!/bin/bash

# Copyright (C) 2011 Lubomir Rintel
# Build script and SPEC files distributable under the terms of GNU GPLv3

set -e
set -o pipefail

# Constants
PACKAGES="
xnu-headers
arm-apple-darwin10-sdk
cctools
ld64
arm-apple-darwin10-gcc
"

HINT=""

# Utility functions
debug_save ()
{
	if [ "$DEBUG" ] && echo "$1" |grep -q "$DEBUG"
	then
		tee "$1".dump
	else
		cat
	fi
}

croak ()
{
	echo "ERROR: $@" >&2
	[ "$HINT" ] && echo "Hint: $HINT" >&2
	trap '' EXIT
	exit 1
}

urlescape ()	{ echo -n "$1" |hexdump -ve '1/1 "_%02x"' |sed 's/_/%/g'; }
log ()		{ echo "$@"; }
exit_handler ()	{ [ $? == 0 ] || croak "Unexpected problem encountered, bailing out."; }

check_deps ()
{
	# Find out if all requisites are present
	for EXEC in $(DRY=1 $SHELL --rpm-requires script |debug_save deps |sed -n 's,executable(\(.*\)),\1,p')
	do
		HINT="Try yum -y install /usr/bin/$EXEC"
		which "$EXEC" >/dev/null || croak "Missing dependency: $EXEC"
	done
	HINT=
}

# Main

trap exit_handler EXIT
check_deps

	awk '/^Source[0-9]*:/ {print $NF}' arm-apple-darwin10-gcc.spec |
		while read U
		do 
			:;
		done

log "Ensuring the source packages are present"
HINT='Please put the missing file into the working directory.'
for P in $PACKAGES
do
	awk '/^Source[0-9]*:/ {print $NF}' $P.spec |
		while read U
		do
			rpm --define 'debug_package %{nil}' -q --specfile $P.spec --qf \
				$(eval rpm $(awk '/^%global/ {print "--define \""$2" "$3"\""}' $P.spec) --eval "$U")"\n" || :
		done
done |
while read F
do
	log "Ensuring '$F' is present"
	B=$(basename $F)
	[ -f $B ] && continue
	echo $F |grep -q :// && wget $F && continue
	false
done
HINT=

log "Building source packages"
rm -f *.src.rpm
HINT="Check your source files"
for SPEC in $PACKAGES
do
	rpmbuild --nodeps --define "_sourcedir $PWD" --define "_srcrpmdir $PWD" -bs $SPEC.spec ||
		croak "Unable to roll a Source package"
done
HINT=

log "Chain-building binary packages"
HINT="Inspect the log from mock"
for SRPM in $PACKAGES
do
	HINT="Inspect the logs in resultdir-$SRPM"
	log "Building $SRPM"

	DEPS=
	[ "$SRPM" = arm-apple-darwin10-gcc ] && DEPS="arm-apple-darwin10-sdk cctools ld64"
	[ "$SRPM" = ld64 ] && DEPS="xnu-headers"
	[ "$SRPM" = cctools ] && DEPS="xnu-headers"

	rm -rf resultdir-$SRPM
	mock $MOCKFLAGS --init --resultdir resultdir-$SRPM
	[ "$DEPS" ] && mock $MOCKFLAGS --install --resultdir resultdir-$SRPM $(ls $(echo "$DEPS " |
		sed 's,\([^ ]*\)  *,resultdir-\1/*.rpm ,g') |egrep -v 'debuginfo|src.rpm$')
	mock $MOCKFLAGS --rebuild --no-clean --resultdir resultdir-$SRPM --cleanup-after $SRPM-*.src.rpm
done
HINT=

log "Creating a repository"
rm -rf resultdir
mkdir -p resultdir
for RPM in $PACKAGES
do
	log "Linking $RPM"
	ln $(find resultdir-$RPM -name '*.rpm') resultdir
done
createrepo resultdir

log "Result is now in resultdir/"
