import lightgbm as lgb
import pandas as pd
import copy

from sub.field_class import *

'''
main_collectData.pyで作成したシミュレーション結果を元に、ゲームをクリアするモデルを作成する。
本モデルでは、現在のすべてのマスの状態とそのときに開けるマスを説明変数として、結果を被説明変数とする。
(汎用性はない)
'''

x,y,bom = 3,3,3 # x:横のマス数 y:縦のマス数 bom:bomの数
x_input_init, y_input_init = 0,0 #1回目にどのマスを開けるか

df = pd.read_csv('random_simulation_kekka.csv')
df.loc[(df.return_val==1), 'return_val'] = 0 #1(クリア)を0(継続)に統一する。
df.loc[(df.return_val==-1), 'return_val'] = 1 #-1(bom)を1に

print(df.head())

X_df =df.iloc[:,:-1]
y_df = df.loc[:,['return_val']]
X_train = X_df.iloc[:int(len(y_df)*0.8), :]
y_train = y_df.iloc[:int(len(y_df)*0.8), :]
X_test  = X_df.iloc[int(len(y_df)*0.8):, :]
y_test  = y_df.iloc[int(len(y_df)*0.8):, :]

# LGBMモデルのパラメータ
num_leaves_ = 100
learning_rate_ = 0.05
max_bin_ = 255 #初期値255
test_size_ =0.2 #モデル作成時の値

# LightGBM のハイパーパラメータ
lgbm_params = {
    'objective': 'binary',
    'metric':'auc',
    'verbosity':-1, #学習の途中経過をprintするかどうか。デフォはする、-1はしない
    'num_leaves':num_leaves_,
    'learning_rate':learning_rate_,
    'max_bin':max_bin_ 
}

# データセットを生成する
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

# 上記のパラメータでモデルを学習する
model = lgb.train(lgbm_params, lgb_train, valid_sets=lgb_eval,
                num_boost_round=1500,early_stopping_rounds=30,
                verbose_eval=4
                )

import pickle
with open('model_lgbm.pkl', mode='wb') as fp:
    pickle.dump(model, fp)

print(model.predict(X_train))
