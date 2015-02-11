#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
TMPDIR='/tmp/csv_merger_tmp'

if [ $# -eq 2 ]
then
	echo -e "\n\n:: Running csv_merger.py"
	$DIR/csv_merger.py $1
	
	echo -e "\n\n:: Extracting paged from PDF\n\c"
	mkdir -p $TMPDIR > /dev/null 2>&1
	COUNT=0
	rm $TMPDIR/extract-*.txt > /dev/null 2>&1
	while true;
	do
		let COUNT=COUNT+1 
		echo -ne "Extracting Page $COUNT\r"

		pdf2txt.py-2.7 -p $COUNT -o $TMPDIR/extract-$COUNT.txt $2

		if [ ! -s $TMPDIR/extract-$COUNT.txt ];
		then
			rm $TMPDIR/extract-$COUNT.txt
			let COUNT=COUNT-1
			echo -ne "Done, extracted $COUNT pages."
			break
		fi
	done

	echo -e "\n\n:: Running csv_index_maker.py"
	$DIR/csv_index_maker.py $1 $TMPDIR

	echo -e "\n\n:: Cleaning up"
	rm $TMPDIR/extract-*.txt
	rmdir $TMPDIR

	echo -e "\n\n:: Finished!"
else
	echo "Please run me like this:"
	echo "run.sh file.csv file.pdf"
fi