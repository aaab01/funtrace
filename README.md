# funtrace
a utility to show c/c++ functions all trace
 ![image](https://github.com/aaab01/funtrace/raw/master/funtrace.png)
 

# usage
1. gcc -fdump-rtl-expand  example.cpp example2.cpp
2. python funtrace.py example.cpp.166r.expand example2.cpp.166r.expand
3. dot -Tsvg -Grankdir=LR -o funtrace.svg funtrace.dot

# issue
1. Can not show funcation-trace when come from fun-pointer
2. virtual funcation can not be determined
