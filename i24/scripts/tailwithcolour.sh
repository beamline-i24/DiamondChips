#Based on Fuyang Liu code: https://gist.github.com/liufuyang/df592fe3e9d77f53db45639ad1b21619

# Colors
# 30 - black   34 - blue          40 - black    44 - blue
# 31 - red     35 - magenta       41 - red      45 - magenta
# 32 - green   36 - cyan          42 - green    46 - cyan
# 33 - yellow  37 - white         43 - yellow   47 - white
#              39 - default
#above are the colour numbers. change the value in the [##m to thw desired colour number. To change back to defualt [39m
#There should be a way of changing the colour of specific bits of text, i.e. the message type (INFO,DEBUG), and the message itself but I have not worked that in yet 

tail --follow=name essex_april18.log | awk '
/INFO/ {print "\033[32m" $0 "\033[39m"}
/DEBUG/ {print "\033[33m" $0 "\033[39m"}
/WARNING/ {print "\033[31m" $0 "\033[39m"}
'
# Can include other labels using the same syntax
#If changing the alias copy the previous alis into a file and then edit for ease - tailSACLA.sh currently exists in the edl folder but have the same following problem so copy the alias first!!!!!
# The above lines do not include all the \ (escapes) that are needed for the alias because of how bash interprets it and will probably fail.
