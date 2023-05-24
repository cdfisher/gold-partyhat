#!/bin/bash
month=`date +%m`
month_tm=`date --date="tomorrow" +"%m"`

if [month != month_tm]
  then
    year=`date +%G`
    year_code=${year:2:2}
    id="MONTH_"$month$year_code
    /usr/bin/python3 update_master_dataframe.py $id 'group' -u 1
    /usr/bin/python3 top_players.py $id 'month'
fi