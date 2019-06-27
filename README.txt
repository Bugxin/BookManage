本项目主要实现了
1. 实现用户登录、注册
2. 列出图书列表、出版社列表、作者列表
3. 点击作者，会在新的页面列出该作者出版的图书列表
4. 点击出版社，会列出该出版社旗下图书列表
5. 可以创建、修改、删除 图书、作者、出版社

升级需求：
1. 点击修改按钮，弹出模块框，模态框中展示该书的信息且信息可以修改，
2. 书名不可重复，不可修改
3. 修改图书信息时，使用ajax请求发送信息


用到的知识点:
form表单验证
利用自定义中间件 实现路由过滤
封装了分页器， 以include导入的方式 实现了 共用
cookies和session登录状态的验证



不足之处:
1.分页 上一页/下一页 当前页 选中效果
2.form表单验证 除注册部分 实现了 局部钩子 全局钩子  ， 添加作者，出版社的验证写的很粗糙
3.未写日志模块
4. auth_user表中扩展字段 未写到作业来，后续自己实验
其他待补充


一个报错  “OverflowError: Python int too large to convert to C long”
原因是数据错误  之前部分数据 是直接在sql表中添加 如日期， 手动添加与通过代码添加 形式是不一样的， 取数据无法转换导致的报错


开发环境: pycharm + python 3.7 + django2.2.1 + django自带数据库

流程图：https://www.processon.com/view/link/5c795392e4b00bcc4f76c015

项目目录结果
BookManage
│  db.sqlite3
│  manage.py
│  README.txt    说明文档
│          
├─app01
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  my_forms.py    自定义form表单验证
│  │  my_middleware.py   自定义中间件   实现路由过滤
│  │  my_pages.py       分页的封装
│  │  tests.py
│  │  urls.py           app01的路由
│  │  views.py        视图函数 主要逻辑部分
│  │  __init__.py
│          
├─BookManage
│  │  settings.py     项目配置 配置了路由白名单
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│
│          
└─templates
    └─app01
            authors.html         展示所有作者
            author_books.html   作者相关书籍
            books.html      展示所有书籍
            index.html          首页
            login.html      登录
            my_page.html     分页  公共部分
            publishes.html   所有出版社
            publish_books.html   出版社出版的书籍
            reg.html      注册
            
