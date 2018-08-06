# 写一个shell脚本 尽可能的输出 linux 机器的 参数
set $(uname -mnrs) 
echo "计算机名  $2"
echo "操作系统  $1"
echo "发行编号  $3"
echo "计算机类型  $4"
