# JiaGuoMeng
家国梦建筑摆放计算

在线版：http://39.107.248.130:9100/ 来自nga[hello_bond1989]
## 使用方法

### 依赖
- python3
- 可选tqdm库提供更好的进度条
### 参数输入的两种方式:
- 写入到data.txt文件内
- 写入到jiaguomeng.py开头JsonData={}中
### 参数说明
#### Mode
- "Online":计算在线模式加成
- "Offline":计算离线模式加成
#### LastResult
- 可将上次输出的建筑策略记录,下次计算会出现替换操作提示
#### Builds
- 将建筑按星级输入,以空格分割
#### 数值调整
数值调整均为增加的部分,即游戏内显示增加150%则输入1.5
##### Mission
- 以 "建筑":加成 的方式输入
- 使用"住宅","商业","工业","Online","Offline"来输入对某类情况的加成
- 注意大括号中最后一行末尾没有逗号
##### Policy&Photos
- "Online":在线加成
- "Offline":离线加成
- "Residence":住宅加成
- "Commercial":商业加成
- "Industry":工业加成

## 说明

- 程序假设所有建筑等级相同**这一假设可能会造成和输出最优与实际最优不符**

- 部分高星建筑数据缺失，欢迎补充、修改


公式参考： https://bbs.nga.cn/read.php?tid=18675554
nga：https://bbs.nga.cn/read.php?tid=18677204

## 更新记录：

9.28更新：
- 修复了一系列数值bug
- 优化了政策计算
- 修复升级优先级的bug

9.30更新：
- 进一步优化代码和交互逻辑
- 增加在线版本
