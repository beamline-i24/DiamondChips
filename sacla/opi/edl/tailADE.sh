tail --follow=name ADE.log | awk '
/INFO/ {print "\033[32m" $0 "\033[39m"}
/DEBUG/ {print "\033[33m" $0 "\033[39m"}
/WARNING/ {print "\033[31m" $0 "\033[39m"} 
'
