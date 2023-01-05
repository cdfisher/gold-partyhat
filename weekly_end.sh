#!/bin/bash
week=`date +%V`
year=`date +%G`
year_code=${year:2:2}
id="WEEK_"$week$year_code

/usr/bin/python3 update_master_dataframe.py $id 'group' -u 1
/usr/bin/python3 top_players.py $id 'week'