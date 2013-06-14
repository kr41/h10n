#!/bin/bash

echo "Test examples:"

if [[ -z "$PYTHON_VENV_PATH" ]]
then
    PYTHON_VENV_PATH='python'
fi

OK=0
FAIL=0
for APP in `find -name "app*.py" | sort`
do
    echo -en "\t$APP ... "
    cd `dirname $APP`
    APP=`basename $APP`
    OUTPUT=`$PYTHON_VENV_PATH $APP 2>&1`
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
[[ $FAIL -eq 0 ]] || exit 1
