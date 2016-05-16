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
MYSQL_REPORT_TABLE=movie

RESULT_FILE=mysql_movie_result
$MYSQL_CMD --local-infile=1 -e "LOAD DATA LOCAL INFILE '$RESULT_FILE' INTO TABLE $MYSQL_REPORT_TABLE\
 FIELDS TERMINATED BY '\t'\
 (name,@var1,category,tag,thumbnail_s,thumbnail_b,score,year,source_page,@dummy)\
 SET \`desc\`=@var1, full_desc=@var1, type=0, remarks=0, play_count=0, source_type=0, create_time=NOW();"
