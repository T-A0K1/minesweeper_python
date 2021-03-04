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
        self.fieldOld = self.field.copy()
        # 各マスの周囲８マスのボムの数を入れる
        for y in range(self.tate):
            for x in range(self.yoko):
                # 周囲の８マス
                a8mass_all = [[y-1, x-1],   [y-1, x], [y-1, x+1],
                                [y, x-1],   [y, x+1],
                                [y+1, x-1], [y+1,x],  [y+1, x+1]]
                a8mass = []
                for a8mass_i in a8mass_all:
                    if ((a8mass_i[0]>=0) and (a8mass_i[0] < self.tate) and (a8mass_i[1] >= 0) and (a8mass_i[1] < self.yoko)):
                        #角や端のマスで周囲８マスが枠内の場合、
                        #本当はfieldの周囲を更に１マス囲んだほうが処理は絶対速い。ただ、めんどい。
                        self.field[y,x] -= self.fieldOld[a8mass_i[0], a8mass_i[1]] #ボムのところは-1, それ以外は0。
        
        self.field[self.fieldOld < 0] = -1

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
            self.return_list.append(0) # 0出ない場合は、0を入れておく。
            
            # 開けたマスが0(周りにbomがない)だったら、周囲のマスも開ける
            zero_mass_l = []
            zero_mass_execed_l = []
            if self.field[y,x]==0:
                zero_mass_l.append(y*1000+x)

            i = 0
            while len(zero_mass_l) > 0:
                y,x = zero_mass_l[0]//1000, zero_mass_l[0] % 1000
                zero_mass_execed_l.append(y*1000+x)
                a8mass_all = [[y-1, x-1],   [y-1, x], [y-1, x+1],
                            [y, x-1],   [y, x+1],
                            [y+1, x-1], [y+1,x],  [y+1, x+1]]
                for a8mass_i in a8mass_all:
                    #そのマスが枠内のマスかつまだ未開封だったら
                    if ((a8mass_i[0]>=0) and (a8mass_i[0] < self.tate) and \
                        (a8mass_i[1] >= 0) and (a8mass_i[1] < self.yoko)) and \
                        (self.field[a8mass_i[0], a8mass_i[1]] != self.original_field[a8mass_i[0], a8mass_i[1]]): 
                            self.field_list.append(self.field.reshape(self.masu,).copy())
                            self.input_list.append([a8mass_i[1],a8mass_i[0]])
                            self.return_list.append(0) 
                            self.field[a8mass_i[0], a8mass_i[1]] = self.original_field[a8mass_i[0], a8mass_i[1]]
                            if self.field[a8mass_i[0], a8mass_i[1]] == 0:
                                zero_mass_l.append(a8mass_i[0]*1000 + a8mass_i[1])
                #実行済みの0のマスは削除
                zero_mass_l = set(zero_mass_l) - set(zero_mass_execed_l)
                zero_mass_l = list(zero_mass_l)
                # zero_mass_l.pop(0) #処理したマスは削除する
                        
            open_masu = (~np.isin(self.field, [9,99])).sum() #9(未開封)と99(ボムの目印)以外のマスの合計   
            if open_masu < (self.masu - self.boms):
                if self.simu==0:
                    print(self.field)
                    return 0
                elif self.simu == 1:
                    return 0, self.field_list, self.input_list, self.return_list
            elif open_masu == (self.masu - self.boms):
                self.return_list.pop(-1) #bomがなければとりあえず0が入っているので、一回削除する
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