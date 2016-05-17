#!/bin/sh

WORKDIR=`dirname $0`
DIR=`cd $WORKDIR && pwd`
cd $DIR

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3310
MYSQL_USER=wacc
MYSQL_PWD=123456
MYSQL_DB=heicha_db

MYSQL_CMD="mysql -h$MYSQL_HOST -P$MYSQL_PORT -u$MYSQL_USER -p$MYSQL_PWD -D$MYSQL_DB"
MYSQL_REPORT_TABLE=movieflow

RESULT_FILE=mysql_movie_result
$MYSQL_CMD --local-infile=1 -e "LOAD DATA LOCAL INFILE '$RESULT_FILE' INTO TABLE $MYSQL_REPORT_TABLE\
 FIELDS TERMINATED BY '\t'\
 (@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,full_url)\
 SET type=0, create_time=NOW(), update_time=NOW();"
