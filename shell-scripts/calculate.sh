#! /bin/bsah

# /**
#  * @author daydream
#  * @email zn.moon2016@gmail.com
#  * @create date 2017-06-12 07:17:54
#  * @modify date 2017-06-12 07:21:11
#  * @desc [一些用于shell中的数字计算和数字比较的函数/命令]
# */


great_than(){
    result=$(awk -v x=$1 -v y=$2 "BEGIN{if (x>y) print 1 ;else print 0}")
    return $result 
}

less_than(){
    result=$(awk -v x=$1 -v y=$2 "BEGIN{if (x<y) print 1 ;else print 0}")
    return $result 
}

equal_with(){
    result=$(awk -v x=$1 -v y=$2 "BEGIN{if (x==y) print 1 ;else print 0}")
    return $result 
}

# add
result=$(awk -v x=$1 -v y=$2 "BEGIN{print x+y}")
echo $result

# reduce
result=$(awk -v x=$1 -v y=$2 "BEGIN{print x-y}")
echo $result

# multiply
result=$(awk -v x=$1 -v y=$2 "BEGIN{print x*y}")
echo $result

# divide
result=$(awk -v x=$1 -v y=$2 "BEGIN{print x/y}")
echo $result


# use example
add=$(awk -v x=$1 -v y=$2 "BEGIN{print x+y}")
reduce=$(awk -v x=$1 -v y=$2 "BEGIN{print x-y}")
equal_with $add $reduce
result=$?
if [ $result -eq 1 ];then
    echo add == reduce
else
    echo add != reduce
fi
