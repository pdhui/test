panda.xiong
====
ghjs 模板引擎 测试版 beta 1.0

改变了传统模板引擎以"< >"或"{ }"作为指令的模式，使用了html的属性作为引擎的语法，使html文件的结构更好的呈现，而不会被引擎所破坏。

本引擎结合了jquery插件使用，通过
var template =$("#id").template()或$.template($("#id"))就可以改变html结构，然后通过返回的template函数，直接调用template（context)，context是数据仓库，一个js对象，就可以给该模板填值。

本引擎也提供了接口让使用者可自定义字符串解析器和语法指令，用以自己解析特殊的html结构。

本文档后续完善，多谢支持......

