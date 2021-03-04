import pandas as pd
import copy

from sub.field_class import *

import pickle

'''
main_makeModel.pyで作成したモデルをもとにシミュレーションを行う。
最後に、そのモデルで行った場合のクリア率を算出する。
例えば、x,y.mass = 3,3,3のときは勝率が30%程度になれば概ね最適解を得ることができている。
'''

with open('model_lgbm.pkl', mode='rb') as fp:
    model = pickle.load(fp)

simulation_num = 400
# 以下はモデル作成時のものに合わす
df = pd.read_csv('random_simulation_kekka.csv')
x,y,bom = 3,3,3
x_input_init, y_input_init = 0,0 #1回目にどれを開けるか

field_list_all = [] #各手番ごとの各マスのリスト
input_list_all = [] #各手番ごとの開けたマス
return_list_all = [] #各手番ごとの返り値(bom or safe or clear)

for _ in range(simulation_num):
    notOpenYet_list_origin = np.arange(x*y) #まだ明けていないマスのリスト
    mf = mainField(x,y)
    mf.set_boms(bom)
    mf.set_nums()

    pf = pField(mf.field)
    stat = 0

    stat, field_list, input_list, return_list = pf.exec_my_turn(input_val = 0, 
                                                                x = x_input_init, y=y_input_init, simu=1) #1マス目を開ける
    x_input, y_input = copy.copy(x_input_init), copy.copy(y_input_init)
    while stat==0:
        notOpenYet_list = notOpenYet_list_origin[pf.field.reshape(x*y,) ==  9]
        
        # 未開封のマス"すべて"に対して、predictを実施し、各マスの予測ハズレ率を求める
        list_for_df = []
        for i in notOpenYet_list:
            list_for_df.append(pf.field.reshape(x*y,).tolist() + [i])
        df_input = pd.DataFrame(list_for_df)
        
        df_input.columns = df.columns[:-1] 
        predict_val = list(model.predict(df_input)) #予測値
        #一番ボムの確率の低いマスを選ぶ
        mass_input = notOpenYet_list[predict_val.index(min(predict_val))]
        y_input = mass_input // x
        x_input = mass_input % x

        stat, field_list, input_list, return_list = pf.exec_my_turn(input_val = 0, #inpute_val; 0:マスをオープン、99:bom_flagをつける
                                                                    x = x_input, y=y_input, simu=1)
    field_list_all = field_list_all + field_list[1:] #1回目は完全なランダムなので除外する
    input_list_all = input_list_all + input_list
    return_list_all = return_list_all + return_list
    
return_list_all = np.array(return_list_all)    
    
print('クリア率：',
      np.round(sum(return_list_all==1)/simulation_num*100,2), '%')