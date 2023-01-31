> 本人声明：仅作学习交流使用

前言：雨课堂支持多开同时播放，视频一个一个播放反而效率低，因此这个视频自动播放脚本意图不在于刷课，仅仅是用雨课堂平台作为实验对象进行编程练习而已。

# 脚本主要功能和实现方法
功能：根据用户给定的课程，自动播放课程内的所有视频。

实现方法：使用python的selenium库在chromeDriver驱动程序下操作chrome浏览器，根据脚本逻辑实现视频播放。


config.ini文件：
section为classinfo中，classname1,classname2,classname3，数字需要递增
