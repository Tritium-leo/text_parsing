# 本工具适用于将 中英文文本段落分句、句子时间提取（中英文句子自身时间提取和中文的推算时间）
背景：大量对文本数据每句话提取时间作为依据，对段落数据进行分句等操作。开发了此工具将段落文本对象化。
具体代码可能粗糙，经过千万级时间文本的测试可行性。分享给需要的人，若有需求 联系作者再做更新。
+ 功能介绍
  + 分整句 短句(正则)
  +  （支持 时间顿号分割：2021年01月、2021年02月干了XXX -> 2021年01月干了XXX，2021年02月干了XXX）
  + 整短句的时间提取（支持 推断时间：7天前/ 具体时间：2021年10月1日 等）
    + 句子时间提取：exp:7天前 2020-01-02
  + 整短句的时间的继承（范围的设置）
    

## 目录结构
+ main 主函数
+ module 对象
+ test 单元测试
+ util 工具类方法
+ web_ui 自带简单的UI界面展示（FLASK）

## 使用方法 参照test 测试用例使用