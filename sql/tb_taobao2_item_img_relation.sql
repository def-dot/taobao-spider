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

 Date: 08/04/2019 15:00:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_taobao2_item_img_relation
-- ----------------------------
DROP TABLE IF EXISTS `tb_taobao2_item_img_relation`;
CREATE TABLE `tb_taobao2_item_img_relation` (
  `taobao2_items_id` int(11) NOT NULL COMMENT '商品 id',
  `taobao2_img_id` int(11) NOT NULL COMMENT '商品图片 id'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
