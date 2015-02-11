#!/bin/bash

TDIR='pdf work'
mkdir -p $TDIR

COUNT=0
rm extract-*.txt
while true;
do
	let COUNT=COUNT+1 

	echo "Extractinge page $COUNT"
	pdf2txt.py-2.7 -p $COUNT -o $TDIR/extract-$COUNT.txt $1

	if [ ! -s extract-$COUNT.txt ];
	then
		rm extract-$COUNT.txt
		let COUNT=COUNT-1
		echo "Done, found $COUNT pages."
		break
	fi
done