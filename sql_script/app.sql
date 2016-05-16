/*
Navicat MySQL Data Transfer

Source Server         : nearby
Source Server Version : 50543
Source Host           : localhost:3306
Source Database       : heicha_db

Target Server Type    : MYSQL
Target Server Version : 50543
File Encoding         : 65001

Date: 2016-05-16 16:52:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for app
-- ----------------------------
DROP TABLE IF EXISTS `app`;
CREATE TABLE `app` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `desc` text,
  `full_desc` mediumtext,
  `version` varchar(16) DEFAULT NULL,
  `ptype` tinyint(4) DEFAULT NULL,
  `dtype` varchar(256) DEFAULT NULL,
  `category` varchar(256) DEFAULT NULL,
  `tag` varchar(256) DEFAULT NULL,
  `thumbnail_s` varchar(1024) DEFAULT NULL,
  `thumbnail_b` varchar(1024) DEFAULT NULL,
  `remarks` int(11) unsigned DEFAULT NULL,
  `score` varchar(16) DEFAULT NULL,
  `download_count` int(11) unsigned DEFAULT NULL,
  `download_url` varchar(256) DEFAULT NULL,
  `appstore_url` varchar(256) DEFAULT NULL,
  `file_size` bigint(20) unsigned DEFAULT NULL,
  `file_hash` varchar(128) DEFAULT NULL,
  `pkg_name` varchar(256) DEFAULT NULL,
  `bundle_id` varchar(128) DEFAULT NULL,
  `vendor` varchar(256) DEFAULT NULL,
  `source_type` tinyint(4) NOT NULL COMMENT '0: 591vr',
  `source_page` varchar(256) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
