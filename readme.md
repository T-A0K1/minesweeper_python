
## 概要
マインスイーパーのためのpythonのコードです。
CUI上でゲームをプレイや、マインスイーパーをプレイするモデルの作成ができます。
This is python code for a minesweeper.
You can play the game on CUI or create a model to play minesweeper.

## 各ファイルの説明
以下の４つのことができます。

1. main_play.py:
CUI上で、マス目の数と爆弾の数を指定して、マインスイーパーを人がプレイできます。

2. main_collectData.py:
開けるマスをランダムで選んだ場合の結果をcsvで出力します。
マス目の数と爆弾の数とシミュレーション回数を指定します。

3. main_makeModel.py
main_collectDataで作成したcsvを元に、当該の設定値でのマインスイーパーを攻略するためのモデルを作成します。
簡易的なモデルです。

4. main_simu.py
main_makeMpdelで作成したモデルを使用して、実際にシミュレーションを行います。

### 今後やりたいこと

5. 
モデルを作成するためのデータをn, n*2, n*3...とした場合のモデルとその場合のクリア率をプロットする。
(どれぐらいのデータが有れば収束するかを図る)

6. 
もっと高度で汎用性の高いモデル

<English by DeepL>
##Description of each file

1. main_play.py:
Allows a person to play minesweeper in the CUI, specifying the number of squares and the number of bombs. 

2. main_collectData.py:
Outputs a csv file of the results of randomly selecting the squares to open.
You can specify the number of squares, the number of bombs, and the number of simulations. 3.

3. main_makeModel.py
Create a model for attacking a minesweeper with the settings in question, based on the csv created in main_collectData.
This is a simple model. 

4. main_simu.py
Using the model created by main_makeMpdel, perform the actual simulation.

## What I want to do in the future

5. 
The data to create the model are n, n*2, n*3... and plot the model and the clearing rate in that case.
(to see how much data is needed for convergence). 

6. 
More advanced and versatile models
