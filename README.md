# icpdomain-tyc
在攻防演练时，一般甲方会给一堆目标单位的中文名称，让我们自己进行域名、IP的信息收集。我们经常需要上企查查、天眼查这些权威网站查看目标单位的备案域名，这些备案域名是公开的，一般是进入网站后，在知识产权-网站备案里看到。如果人工一个个单位去点去翻，会大大消耗我们有限的时间。本程序通过python selenium自动化爬取目标资产在天眼查上的备案域名，无需使用代理地址池，也不需要对登录验证码、加密算法之类的进行攻击。
# 使用说明
将目标单位的名称逐行保存在company_name.txt文档里，然后python3 icpdomain-tyc.py运行即可，生成的文件保存在icpdomain.txt里
<img width="1110" height="510" alt="QQ20250803-223910" src="https://github.com/user-attachments/assets/ffa696c7-f180-4a72-9bde-2c7da31b6a32" />
