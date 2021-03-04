import numpy as np
import pandas as pd
import copy

from sub.field_class import *

'''
ランダムにマスを開けるシミュレーションをn回繰り返す。
各手番ごとに、開けたマス/その時の全マスの状態/開けた結果 を記録する。
'''

x,y,bom = 3,3,3 # x:横のマス数 y:縦のマス数 bom:bomの数
simulation_num = 100
x_input_init, y_input_init = 0,0 #1回目にどこのマスを開けるか

field_list_all = []
input_list_all = []
return_list_all = []
field_true_list_all = []

for _ in range(simulation_num):
    notOpenYet_list_origin = list(range(x*y)) #まだ開けていないマスのリスト
    mf = mainField(x,y)
    mf.set_boms(bom)
    mf.set_nums()

    pf = pField(mf.field)
    stat = 0

    stat, field_list, input_list, return_list = pf.exec_my_turn(input_val = 0, x = x_input_init, y=y_input_init, simu=1) #1マス目を開ける
    x_input, y_input = copy.copy(x_input_init), copy.copy(y_input_init)
    field_true_list_all.append(pf.original_field.reshape(-1,).tolist())
    while stat==0:
        field_true_list_all.append(pf.original_field.reshape(-1,).tolist())
        notOpenYet_list = notOpenYet_list_origin.copy()
        notOpenYet_list_mass = [input_tmp[1] * x + input_tmp[0] for input_tmp in input_list]#x, y座標を1次元に変換
        for input_ in notOpenYet_list_mass:
            notOpenYet_list.remove(input_) #既に開封済みのマスを除去
        mass_input = np.random.choice(notOpenYet_list, 1)[0]
        y_input = mass_input // x
        x_input = mass_input % x
        tmp = pf.exec_my_turn(input_val = 0,x = x_input, y=y_input, simu=1)
        stat, field_list, input_list, return_list = tmp
    field_list_all = field_list_all + field_list#[1:] #1回目は完全なランダムなので除外する
    input_list_all = input_list_all + input_list#[1:]
    return_list_all = return_list_all + return_list#[1:]

df = pd.DataFrame(field_list_all)
df_input = pd.DataFrame(input_list_all)
df_input['input'] = df_input.iloc[:, 0] + df_input.iloc[:, 1]*x
df_return = pd.DataFrame(return_list_all)
df_return.columns = ['return_val']
df = pd.concat([df,df_input['input'],df_return], axis=1)

# 答えをdfに付加するデバッグ用のコード。但し、0が開けられるとずれるので注意
# print(field_true_list_all[:12])
# df_debug = pd.DataFrame(field_true_list_all)
# print(df_debug.head())
# df= pd.concat([df, df_debug], axis=1)
df.to_csv('random_simulation_kekka.csv',
            index=False)
