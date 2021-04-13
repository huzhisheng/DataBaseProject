/*==============================================================*/
/* Trigger 插入一条关注记录就让被关注的用户的粉丝数加1          */
/*==============================================================*/
delimiter //
create trigger trigger_fans_count_insert
after insert on fans_relation
for each row
begin
      update user_info set user_fans = user_fans + 1
      where user_id = new.famous_user_id;
end //

/*==============================================================*/
/* Trigger 删除一条关注记录就让原来被关注的用户的粉丝数减1      */
/*==============================================================*/
delimiter //
create trigger trigger_fans_count_delete
after delete on fans_relation
for each row
begin
      update user_info set user_fans = user_fans - 1
      where user_id = old.famous_user_id;
end //

/*==============================================================*/
/* Trigger 插入一条点赞记录就让视频的点赞数加1                  */
/*==============================================================*/
delimiter //
create trigger trigger_like_count_insert
after insert on like_relation
for each row
begin
      update video_info set video_nlike = video_nlike + 1
      where video_id = new.video_id;
end //

/*==============================================================*/
/* Trigger 删除一条点赞记录就让视频的点赞数减1      			*/
/*==============================================================*/
delimiter //
create trigger trigger_like_count_delete
after delete on like_relation
for each row
begin
      update video_info set video_nlike = video_nlike - 1
      where video_id = old.video_id;
end //