/*
Navicat MySQL Data Transfer

Source Server         : nearby
Source Server Version : 50543
Source Host           : localhost:3306
Source Database       : heicha_db

Target Server Type    : MYSQL
Target Server Version : 50543
File Encoding         : 65001

Date: 2016-05-16 16:53:07
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `desc` text,
  `full_desc` mediumtext,
  `type` tinyint(4) DEFAULT NULL,
  `category` varchar(256) DEFAULT NULL,
  `tag` varchar(256) DEFAULT NULL,
  `thumbnail_s` varchar(1024) DEFAULT NULL,
  `thumbnail_b` varchar(1024) DEFAULT NULL,
  `remarks` int(11) unsigned DEFAULT NULL,
  `score` varchar(16) DEFAULT NULL,
  `play_count` int(11) DEFAULT NULL,
  `duration` int(11) unsigned DEFAULT NULL,
  `year` int(11) unsigned DEFAULT NULL,
  `area` varchar(16) DEFAULT NULL,
  `actor` varchar(512) DEFAULT NULL,
  `source_type` tinyint(4) NOT NULL COMMENT '0: 591vr',
  `source_page` varchar(256) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
