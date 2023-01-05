#!/bin/bash
month=`date +%m`
year=`date +%G`
year_code=${year:2:2}
id="MONTH_"$month$year_code

/usr/bin/python3 update_master_dataframe.py $id 'group'
