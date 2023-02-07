# on execution of this script

# c++ symbols are going to be converted to readable ones
# strip function parameters
# remove nodes consisted of "std::" function calls

# note that we can't see exact virtual function calls 
# for the graph is generated from c/c++ object files

echo "input .expand files (file names)"
read FILES;
python2 ../funtrace.py ${FILES}
cat funtrace.dot|c++filt > funtrace.dot1
sed -i "s/, funcdef_no=[^)]*)/)/g" funtrace.dot1
sed -i "s/ ([^\"]*)/()/g" funtrace.dot1
grep -v '\-> "std::' funtrace.dot1 > funtrace.dot2
grep -v '^"std::' funtrace.dot2 > funtrace.dot3
dot -Tsvg -Grankdir=LR -o funtrace.svg funtrace.dot3

