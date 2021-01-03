# HoochieBaby

## run_self_test:
true or false  

Auto runs a self-test to check for working conditions whenever preference options are changed.



## choice_probability:
This controls the probability of getting a new, learning, or review card.

0: New card  
1: Intra-day learning card (<1440)  
2: Day leaning card (>=1440)  
3: Review card  

[0,1,2,3,3,3] = more review cards  
[0,0,0,1,2,3] = more new cards  
[0,0,1,2,2,3] = more new and learning cards  
[0,1,0,2,3,2] = same as above  
