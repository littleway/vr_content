/*
Navicat MySQL Data Transfer

Source Server         : nearby
Source Server Version : 50543
Source Host           : localhost:3306
Source Database       : heicha_db

Target Server Type    : MYSQL
Target Server Version : 50543
File Encoding         : 65001

Date: 2016-05-16 16:43:58
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for movieflow
-- ----------------------------
DROP TABLE IF EXISTS `movieflow`;
CREATE TABLE `movieflow` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `movie_id` bigint(20) unsigned NOT NULL,
  `type` tinyint(4) DEFAULT NULL,
  `play_url` varchar(256) DEFAULT NULL,
  `full_url` varchar(256) DEFAULT NULL,
  `file_size` bigint(20) unsigned DEFAULT NULL,
  `file_hash` varchar(128) DEFAULT NULL,
  `width` int(10) unsigned DEFAULT NULL,
  `height` int(10) unsigned DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
