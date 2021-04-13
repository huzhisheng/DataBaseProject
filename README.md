# DataBaseProject
HITSZ2021数据库实验





## 部署数据库

>  运行服务器前要先部署数据库，以下两种方式均可成功部署数据库

### 1.通过执行libray.sql语句

- 先创建一个名为 "tiktok1" 的database（数据库名称要改的话需要到 app/config.py 文件中先修改一下）
- use tiktok1
- 再执行 Lab2/libray.sql 文件
- 再执行 Lab2/trigger.sql 文件创建相应触发器



### 2.通过flask部署数据库

- 在project根目录执行下列语句:

  ```python
  python manage.py shell
  # 接着进入db的shell模式再输入下列语句
  from app import db
  db.create_all()
  quit
  ```



## 启动服务器

- 在project根目录执行下列语句:

  ```python
  python manage.py runserver
  ```

  