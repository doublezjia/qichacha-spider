# qichacha-spider

爬取企查查网站上面登记的企业信息

## 脚本文件说明

- qichachaspider.py 爬虫脚本
- qichachaspider.2.0.py 新页面的爬虫脚本
- qichacha_company.csv 数据保存的CSV文件，自动生成

> 脚本目前只爬取广东地区的企业信息，如果需要请更改脚本的URL地址

> 网站页面修改了，重新编写获取电话、邮箱、官网和地址的代码，新脚本为qichachaspider.2.0.py
 
> 如果获取的电话号码和邮箱地址不显示，请添加登录后的网站cookies然后在contentPage(url)中的requets.get()中添加cookies=cookies,然后再执行爬虫

> 代码修改进行中 2018-06-1