CREATE TABLE `tgcw_zhaobiao`
(
    `id`             int(11) NOT NULL AUTO_INCREMENT,
    `ori_id`         int(11) DEFAULT NULL,
    `notice_title`   varchar(255) DEFAULT NULL,
    `publish_time`   datetime     DEFAULT NULL,
    `notice_content` text,
    `update_time`    datetime     DEFAULT NULL,
    `type_code`      varchar(255) DEFAULT NULL,
    `type_name`      varchar(255)  DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;
