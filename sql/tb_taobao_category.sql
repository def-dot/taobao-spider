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

 Date: 08/04/2019 15:00:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_taobao_category
-- ----------------------------
DROP TABLE IF EXISTS `tb_taobao_category`;
CREATE TABLE `tb_taobao_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '商品种类主键',
  `category` varchar(255) NOT NULL COMMENT '商品种类名称',
  `code` varchar(8) NOT NULL COMMENT '商品种类代码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
