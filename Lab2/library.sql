/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021-04-14 15:08:24                          */
/*==============================================================*/


drop
table if exists viewUserStarVideo;

drop
table if exists viewAllVideoNameList;

drop
table if exists viewAllUserNameList;

drop
table if exists viewAllUserAndVideoList;

drop table if exists admin_info;

drop table if exists fans_relation;

drop table if exists img_info;

drop table if exists like_relation;

drop table if exists msg_info;

drop table if exists review_info;

drop table if exists star_info;

drop table if exists star_relation;

# drop index index_user_name on user_info;

drop table if exists user_info;

# drop index index_user_id on video_info;

drop table if exists video_info;

drop table if exists watch_relation;

/*==============================================================*/
/* Table: admin_info                                            */
/*==============================================================*/
create table admin_info
(
   admin_id             int not null auto_increment,
   admin_account        varchar(20) not null,
   admin_pass           varchar(20) not null,
   primary key (admin_id)
);

/*==============================================================*/
/* Table: fans_relation                                         */
/*==============================================================*/
create table fans_relation
(
   fans_user_id         int not null,
   famous_user_id       int not null,
   primary key (fans_user_id, famous_user_id)
);

/*==============================================================*/
/* Table: img_info                                              */
/*==============================================================*/
create table img_info
(
   img_id               int not null auto_increment,
   img_url              varchar(256) not null,
   primary key (img_id)
);

/*==============================================================*/
/* Table: like_relation                                         */
/*==============================================================*/
create table like_relation
(
   video_id             int not null,
   user_id              int not null,
   primary key (video_id, user_id)
);

/*==============================================================*/
/* Table: msg_info                                              */
/*==============================================================*/
create table msg_info
(
   sender_id            int not null,
   receiver_id          int not null,
   msg_time             datetime not null,
   msg_text             varchar(256) not null,
   primary key (sender_id, receiver_id, msg_time)
);

/*==============================================================*/
/* Table: review_info                                           */
/*==============================================================*/
create table review_info
(
   review_id            int not null auto_increment,
   user_id              int not null,
   video_id             int not null,
   review_text          varchar(256) not null,
   review_time          datetime not null,
   primary key (review_id)
);

/*==============================================================*/
/* Table: star_info                                             */
/*==============================================================*/
create table star_info
(
   star_id              int not null auto_increment,
   user_id              int not null,
   star_ctime           datetime not null,
   star_name            varchar(20) not null,
   primary key (star_id)
);

/*==============================================================*/
/* Table: star_relation                                         */
/*==============================================================*/
create table star_relation
(
   star_id              int not null,
   video_id             int not null,
   star_rtime           datetime not null,
   primary key (star_id, video_id)
);

/*==============================================================*/
/* Table: user_info                                             */
/*==============================================================*/
create table user_info
(
   user_id              int not null auto_increment,
   user_name            varchar(20) not null,
   user_fans            int,
   user_pass            varchar(20) not null,
   user_account         varchar(20) not null,
   user_date            datetime not null,
   primary key (user_id)
);

/*==============================================================*/
/* Index: index_user_name                                       */
/*==============================================================*/
create index index_user_name on user_info
(
   user_name
);

/*==============================================================*/
/* Table: video_info                                            */
/*==============================================================*/
create table video_info
(
   video_id             int not null auto_increment,
   user_id              int not null,
   img_id               int not null,
   video_url            varchar(256) not null,
   video_title          varchar(20) not null,
   video_comment        varchar(256),
   video_ctime          datetime not null,
   video_mtime          datetime,
   video_nlike          int not null,
   primary key (video_id)
);

/*==============================================================*/
/* Index: index_user_id                                         */
/*==============================================================*/
create index index_user_id on video_info
(
   user_id
);

/*==============================================================*/
/* Table: watch_relation                                        */
/*==============================================================*/
create table watch_relation
(
   user_id              int not null,
   video_id             int not null,
   watch_time           datetime not null,
   primary key (user_id, video_id)
);

/*==============================================================*/
/* View: viewAllUserAndVideoList                                */
/*==============================================================*/
create VIEW  viewAllUserAndVideoList
 as
select
   U.user_id,
   U.user_name,
   V.video_id,
   V.video_title
from
   video_info V,
   user_info U
where
   V.user_id = U.user_id
order by
   U.user_id;

/*==============================================================*/
/* View: viewAllUserNameList                                    */
/*==============================================================*/
create VIEW  viewAllUserNameList
 as
select
   U.user_id,
   U.user_name
from
   user_info U
order by
   U.user_id;

/*==============================================================*/
/* View: viewAllVideoNameList                                   */
/*==============================================================*/
create VIEW  viewAllVideoNameList
 as
select
   V.video_id,
   V.video_title
from
   video_info V
order by
   V.video_id;

/*==============================================================*/
/* View: viewUserStarVideo                                      */
/*==============================================================*/
create VIEW  viewUserStarVideo
 as
select
   U.user_id,
   S.star_id,
   SR.video_id
from
   user_info U,
   star_info S,
   star_relation SR
where
   U.user_id = S.user_id and
   S.star_id = SR.star_id
order by
   U.user_id;

alter table fans_relation add constraint FK_fans_relation foreign key (fans_user_id)
      references user_info (user_id) on delete restrict on update restrict;

alter table fans_relation add constraint FK_fans_relation2 foreign key (famous_user_id)
      references user_info (user_id) on delete restrict on update restrict;

alter table like_relation add constraint FK_like_relation foreign key (video_id)
      references video_info (video_id) on delete restrict on update restrict;

alter table like_relation add constraint FK_like_relation2 foreign key (user_id)
      references user_info (user_id) on delete restrict on update restrict;

alter table msg_info add constraint FK_msg_info foreign key (receiver_id)
      references user_info (user_id) on delete restrict on update restrict;

alter table msg_info add constraint FK_msg_info2 foreign key (sender_id)
      references user_info (user_id) on delete restrict on update restrict;

alter table review_info add constraint FK_user_review foreign key (user_id)
      references user_info (user_id) on delete restrict on update restrict;

alter table review_info add constraint FK_video_review foreign key (video_id)
      references video_info (video_id) on delete restrict on update restrict;

alter table star_info add constraint FK_star_user foreign key (user_id)
      references user_info (user_id) on delete restrict on update restrict;

alter table star_relation add constraint FK_star_relation foreign key (video_id)
      references video_info (video_id) on delete restrict on update restrict;

alter table star_relation add constraint FK_star_relation2 foreign key (star_id)
      references star_info (star_id) on delete restrict on update restrict;

alter table video_info add constraint FK_img_video foreign key (img_id)
      references img_info (img_id) on delete restrict on update restrict;

alter table video_info add constraint FK_user_video foreign key (user_id)
      references user_info (user_id) on delete restrict on update restrict;

alter table watch_relation add constraint FK_watch_relation foreign key (video_id)
      references video_info (video_id) on delete restrict on update restrict;

alter table watch_relation add constraint FK_watch_relation2 foreign key (user_id)
      references user_info (user_id) on delete restrict on update restrict;

