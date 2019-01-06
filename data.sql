use MessageMerge;
create table if not exists qjwqzhb2(
id bigint(20) NOT NULL AUTO_INCREMENT primary key,
name varchar(255) NOT NULL unique,
url varchar(255) NOT NULL ,
pub_time varchar(255) NOT NULL,
con_finish_time varchar(255) NOT NULL,
click_num varchar(255) DEFAULT NULL,
dock_enter_num varchar(255) DEFAULT NULL,
func_use varchar(255) DEFAULT NULL,
main_indice varchar(255) DEFAULT NULL,
tp varchar(255) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;