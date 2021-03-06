抓取微信公众号文章
===

### 原理

抓取微信公众号文章数据，有三种方案：

1. 从微信端抓取数据难度较大，一般需要通过代理来抓取，需要人工、手机等，而且需要改动开源库的代码来定制符合需求的功能

2. 从微信搜狗抓取数据简单，但微信搜狗提供的都是临时数据，要解决转为永久数据的问题；并且微信搜狗做了反爬处理，如何自动识别验证码也是个问题

3. 从新榜抓取数据较简单而且数据永久、丰富

综上所述，选择第三种方案。

### 使用

##### 配置

编辑 `wechat/config.py`，修改为符合环境的配置。

##### 导入excel中的公众号到数据库

执行`python3 import.py`

##### 抓取文章数据入库

执行`python3 get_all.py`