/*
 Navicat Premium Data Transfer

 Source Server         : 本地测试
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : GraduationProject

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 08/04/2019 15:00:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_taobao2_items_info
-- ----------------------------
DROP TABLE IF EXISTS `tb_taobao2_items_info`;
CREATE TABLE `tb_taobao2_items_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '商品主键 id',
  `username` varchar(255) NOT NULL COMMENT '出售人 name',
  `userpage_url` varchar(255) NOT NULL COMMENT '出售人详情页',
  `user_avatar` varchar(255) NOT NULL COMMENT '出售人头像 url',
  `user_level` varchar(4) NOT NULL COMMENT 'vip 等级',
  `item_url` varchar(255) NOT NULL COMMENT '商品链接',
  `item_title` varchar(255) NOT NULL COMMENT '商品标题',
  `item_image` varchar(255) NOT NULL COMMENT '商品图片',
  `item_price` float(10,2) NOT NULL COMMENT '商品价格',
  `item_location` varchar(10) NOT NULL COMMENT '所在地',
  `item_desc` varchar(255) NOT NULL COMMENT '商品描述',
  `ctime` int(10) NOT NULL COMMENT '创建记录时间',
  `mtime` int(10) NOT NULL COMMENT '修改记录时间',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '记录状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
