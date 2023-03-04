CREATE TABLE `jtsww`
(
    `id`                 int(11) NOT NULL AUTO_INCREMENT,
    `guid`               varchar(255) DEFAULT NULL,
    `type_code`          varchar(255) DEFAULT NULL,
    `type_name`          varchar(255) DEFAULT NULL,
    `name`               varchar(255) DEFAULT NULL,
    `time`               datetime     DEFAULT NULL,
    `project_type`       varchar(255) DEFAULT NULL,
    `type`               varchar(255) DEFAULT NULL,
    `bid_section_code`   varchar(255) DEFAULT NULL,
    `doc_get_start_time` datetime     DEFAULT NULL,
    `tender_agency_lxr`  varchar(255) DEFAULT NULL,
    `tender_agency_name` varchar(255) DEFAULT NULL,
    `tenderer_name`      varchar(255) DEFAULT NULL,
    `notice_content`     mediumtext,
    `update_time`        datetime     DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=396 DEFAULT CHARSET=utf8mb4;