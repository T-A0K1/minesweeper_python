import numpy as np

class mainField:
    def __init__(self, yoko, tate):
        if (yoko < 2) or (tate < 2):
            print("x_range and y_range must ber over 1")
        else:
            self.yoko = yoko
            self.tate = tate
            self.masu = yoko * tate
            self.field = np.zeros([self.tate, self.yoko])

    def set_boms(self, boms):
        if boms > self.masu:
            print("bom's num must be under x_range * y_range")
        else:
            self.boms = boms
            bomPoint = np.random.choice(range(self.masu), boms, replace=False)
            self.field = self.field.reshape(self.masu,)
            self.field[bomPoint] = -1
            self.field = self.field.reshape([self.tate, self.yoko])
    
    def set_nums(self):
        tate, yoko, masu = self.tate, self.yoko, self.masu
        self.field = self.field.reshape(self.masu,)
        self.fieldOld = self.field.copy()
        #左上 右, 下, 右下
        self.field[0] = -(self.fieldOld[[1,yoko, yoko+1]].sum())
        #右上 左, 右下, 下
        self.field[yoko-1] = -(self.fieldOld[[yoko-2, yoko*2-2, yoko*2-1]].sum())
        #左下
        self.field[masu-yoko] = -(self.fieldOld[[masu-yoko*2, masu-yoko*2+1, masu-yoko+1]].sum())
        #右下
        self.field[masu-1] = -(self.fieldOld[[masu-yoko-2, masu-yoko-1,masu-2]].sum())
        #上辺
        for i in range(yoko-2):
            nPoint = 1 + i
            self.field[nPoint] =  -(self.fieldOld[[nPoint-1, nPoint+1, nPoint+yoko-1,
                                    nPoint+yoko, nPoint+yoko+1]].sum())
        #下辺
        for i in range(yoko-2):
            nPoint = masu - yoko + 1 + i
            self.field[nPoint] =  -(self.fieldOld[[nPoint - yoko -1, nPoint - yoko, nPoint - yoko +1,
                                                    nPoint -1, nPoint + 1]].sum())
        #左辺
        for i in range(tate-2):
            nPoint = yoko*(i+1)
            self.field[nPoint] =  -(self.fieldOld[[nPoint - yoko, nPoint - yoko+1,nPoint + 1,
                                                    nPoint+yoko, nPoint + yoko + 1]].sum())

        #右辺
        for i in range(tate-2):
            nPoint = yoko*(i+2) - 1
            self.field[nPoint] =  -(self.fieldOld[[nPoint - yoko - 1, nPoint - yoko,nPoint - 1,
                                                    nPoint+yoko - 1, nPoint + yoko]].sum())
        #中央
        for x in range(yoko-2): 
            for y in range(tate-2):
                nPoint = yoko*(y+1) + 1 + x
                self.field[nPoint] =  -(self.fieldOld[[nPoint - yoko - 1, nPoint - yoko,nPoint - yoko +  1,
                                                    nPoint - 1, nPoint + 1,
                                                    nPoint + yoko - 1, nPoint + yoko,nPoint + yoko +  1]].sum())


        # ボムの場所を戻す
        self.field[self.fieldOld < 0] = -1
        self.field = self.field.reshape([tate, yoko])

class pField:
    def __init__(self, original_field):
        self.tate = original_field.shape[0]
        self.yoko = original_field.shape[1]
        self.boms = (original_field==-1).sum()
        self.masu = self.yoko * self.tate
        self.field = np.ones_like(original_field)*9
        self.original_field = original_field
        self.field_list = [] #フィールドの履歴
        self.input_list = [] #開けたマスの履歴
        self.return_list = [] #戻り値の履歴(0:継続, -1:bom!, 1:クリア) ※開封時のみ

    def open_one(self, x = -1, y = -1): #simu==1のときは、シミュレーションモード
        
        ## 以下は例外処理
        if self.simu == 0: # simuのときは、x,yを実行時に入力
            print('input x coordinate')
            x = int(input())
            print('input y coordinate')
            y = int(input())
        if (x >= self.yoko) or (y >= self.tate):
            print("you must set x<", self.yoko, "and y<",self.tate, ".")
            print(self.field)
            return 0
        if self.field[y,x]==99:
            print('The point was set "Bom Flag". Do you open that? yes:0,no:1')
            exec_open = str(input())
            if exec_open=='0':
                pass
            else:
                return 0 #開けない
        elif self.field[y,x]!=9: #9でも99でもない
            print('The point was opened.')
            return 0

        ## メイン処理
        #開封前のフィールドと指定したマスを記録
        self.field_list.append(self.field.reshape(self.masu,).copy())
        self.input_list.append([x,y])

        if self.original_field[y,x]==-1:
            self.field = np.ones_like(self.original_field)*99
            self.return_list.append(-1)
            if self.simu == 0:
                print('bom!!!!!!')
                print(self.original_field)
                return -1
            else:
                return -1, self.field_list, self.input_list, self.return_list
        else:
            self.field[y,x] = self.original_field[y,x]
            open_masu = (~np.isin(self.field, [9,99])).sum() #9(未開封)と99(ボムの目印)以外のマスの合計
            if open_masu < (self.masu - self.boms):
                self.return_list.append(0)
                if self.simu==0:
                    print(self.field)
                    return 0
                elif self.simu == 1:
                    return 0, self.field_list, self.input_list, self.return_list
            elif open_masu == (self.masu - self.boms):
                self.return_list.append(1)
                if self.simu == 0:
                    print(self.field)
                    print('GOAL!')
                    return 1
                else:
                    return 1, self.field_list, self.input_list, self.return_list

    def reset(self):
        self.field = np.ones_like(original_field)*9

    def mark_bom(self):
        x = int(input())
        y = int(input())
        if (x >= self.yoko) or (y >= self.tate):
            print("you must set x<", self.yoko, "and y<",self.tate, ".")
            print(self.field)
            return 0
        self.field[y,x] = 99
        print(self.field)

        #99をつけたマスと、実際のボムの位置が同じならクリア
        tmp_field = self.field.copy()
        tmp_field[tmp_field!=99]= 999
        tmp_field[tmp_field==99]= -1
        true_boms_count = (tmp_field == self.original_field).sum()
        if true_boms_count == self.boms:
            print('GOAL!')
            return 1
        else:
            return 0

    def exec_my_turn(self, input_val, x=-1, y=-1, simu=0):
        self.simu = simu
        
        if input_val == 99:
            return self.mark_bom()
        else:
            if self.simu == 0:
                return self.open_one()
            elif self.simu == 1:
                return self.open_one(x,y)