CREATE TABLE `ebnew`
(
    `id`                int(11) NOT NULL AUTO_INCREMENT,
    `ori_id`            int(11) DEFAULT NULL,
    `details_title`     varchar(255) DEFAULT NULL,
    `release_time`      datetime     DEFAULT NULL,
    `bidcode`           varchar(255) DEFAULT NULL,
    `announcement_type` varchar(255) DEFAULT NULL,
    `tender_method`     varchar(255) DEFAULT NULL,
    `deadline`          datetime     DEFAULT NULL,
    `orgname`           varchar(255) DEFAULT NULL,
    `tender_area`       varchar(255) DEFAULT NULL,
    `tender_products`   varchar(255) DEFAULT NULL,
    `industry`          varchar(255) DEFAULT NULL,
    `details_content`   mediumtext,
    `update_time`       datetime     DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=396 DEFAULT CHARSET=utf8mb4;