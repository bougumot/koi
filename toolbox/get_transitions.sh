#/bin/bash

CNT=0

FILES=`find . -name koi.transitions`

for file in $FILES; do
	ITEMS=`cat $file`
	CNT=$(( CNT + ITEMS ))
done

echo $CNT
