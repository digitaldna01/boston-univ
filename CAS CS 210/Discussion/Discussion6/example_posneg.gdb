display {{long long}&positive_count, {long long}&negative_count}
display /1gd $rax

define myreturn
  set $pc = RETURN_HERE
end