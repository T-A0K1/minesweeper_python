import numpy as np

from sub.field_class import *

'''
手動でマインスイーパーを遊ぶためのゲーム
'''

x,y,bom = 3,2,2
mf = mainField(x,y)
mf.set_boms(bom)
mf.set_nums()

pf = pField(mf.field)
stat = 0
print(pf.field)
while stat==0:
    print('input 0:open a mass, input 99:set "Bom Flag" , other input: End this game')
    input_val = int(input())
    stat = pf.exec_my_turn(input_val)
print(pf.input_list)
print()
print(pf.return_list)
print()
print(pf.field_list)
print(len(pf.field_list))
print(stat)

