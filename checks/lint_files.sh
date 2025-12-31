#!/bin/bash

RET=0

CONSTRAINTS_PATH='src/COIM/constraints/'
CONSTRAINTS_SEARCH_STR='constrain*.py'
CONSTRAINTS="$CONSTRAINTS_PATH$CONSTRAINTS_SEARCH_STR"

TESTS_PATH='tests/'
TESTS_SEARCH_STR='test*.py'
TESTS="$TESTS_PATH$TESTS_SEARCH_STR"

LOGS_PATH='lint_output/'
RESULT_PATH='lint_result.csv'
OK_STRING=':) No issues found.'

echo 'path;num_warnings' > $RESULT_PATH

name='operator'
log="$LOGS_PATH$name.log"
if [ -f $log ]; then
	head_log=$(head $log)
	if [ "$head_log" = "$OK_STRING" ]; then
		num_warns=0
	else
		num_warns=$(sed -n '$=' $log)
	fi
else
	num_warns=-1
	RET=1
fi
echo "$name;$num_warns" >> $RESULT_PATH

for file in $CONSTRAINTS; do
	script="${file/$CONSTRAINTS_PATH/''}"
	name="${script/'.py'/''}"
	log="$LOGS_PATH$name.log"
	if [ -f $log ]; then
		head_log=$(head $log)
		if [ "$head_log" = "$OK_STRING" ]; then
			num_warns=0
		else
			num_warns=$(sed -n '$=' $log)
		fi
	else
		num_warns=-1
		RET=1
	fi
	echo "$name;$num_warns" >> $RESULT_PATH
done

for file in $TESTS; do
	script="${file/$TESTS_PATH/''}"
	name="${script/'.py'/''}"
	log="$LOGS_PATH$name.log"
	if [ -f $log ]; then
		head_log=$(head $log)
		if [ "$head_log" = "$OK_STRING" ]; then
			num_warns=0
		else
			num_warns=$(sed -n '$=' $log)
		fi
	else
		num_warns=-1
		RET=1
	fi
	echo "$name;$num_warns" >> $RESULT_PATH
done

exit $RET