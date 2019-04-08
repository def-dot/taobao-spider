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

 Date: 08/04/2019 15:00:24
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_taobao2_img
-- ----------------------------
DROP TABLE IF EXISTS `tb_taobao2_img`;
CREATE TABLE `tb_taobao2_img` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '图片 id',
  `img_url` varchar(255) NOT NULL COMMENT '图片 url',
  `ctime` int(10) NOT NULL COMMENT '创建时间',
  `mtime` int(10) NOT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
