#!/bin/bash

echo "Test examples:"

OK=0
FAIL=0
for APP in `find -name "app*.py" | sort`
do
    echo -en "\t$APP ... "
    cd `dirname $APP`
    APP=`basename $APP`
    OUTPUT=`python $APP 2>&1`
    if [[ $? -eq 0 ]]
    then
        echo 'Ok'
        OK=$(( $OK + 1 ))
    else
        echo 'Fail'
        echo '-----------------------------------------------------------'
        echo -e "$OUTPUT"
        echo '-----------------------------------------------------------'
        FAIL=$(( $FAIL + 1 ))
    fi
    cd - > /dev/null
done

echo "Passed: $OK"
echo "Failed: $FAIL"
if [[ $FAIL -eq 0 ]]
then
    echo "Ok"
else
    echo "Fail"
fi
