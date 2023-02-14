# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 17:08:59 2022

@author: yin
"""

import pandas as pd
import numpy as np
import random

# set parameter
up = 20  # 单个随机数上限
down = 10  # 单个随机数下限
line = 500  # 单个模式生成多少行
col_num = 3  # 最终生成几列
model_num = 6  # 执行的model数量，同事需要改下面的函数

'''
model1：加法，括号在最后 addition，   eg：1     +     2=(    )
model2：加法，括号在中间 addition，   eg：1     +(    )=     3
model3：加法，括号在前面 addition，   eg：(    )+     2=     3
model4：减法，括号在最后 Subtraction，eg：3     -     2=(    )
model5：减法，括号在中间 Subtraction，eg：3     -(    )=     1
model6：减法，括号在前面 Subtraction，eg：(    )-     2=     1
'''


# model1：加法，括号在最后
def model1():
    lis = []
    df_col_lis = ['a' + str(x) for x in range(5)]

    df = pd.DataFrame(np.random.randint(down, up, size=(line, 5)), columns=(df_col_lis))
    arr = df['a0']

    df['a1'] = '+'
    df['a3'] = '='
    df['a4'] = '(    )'

    for i in arr:
        a = random.randint(0, up - i)
        lis.append(a)
    df['a2'] = lis
    return df


# model2：加法，括号在中间
def model2():
    df_col_lis = ['a' + str(x) for x in range(5)]

    df = pd.DataFrame(np.random.randint(down, up, size=(line, 5)), columns=(df_col_lis))

    df['a1'] = '+'
    df['a3'] = '='
    df['a2'] = '(    )'

    for i in range(line):
        if df.loc[i, 'a0'] > df.loc[i, 'a4']:
            df.loc[i, 'a0'], df.loc[i, 'a4'] = df.loc[i, 'a4'], df.loc[i, 'a0']
    return df


# model3：加法，括号在前面
def model3():
    df_col_lis = ['a' + str(x) for x in range(5)]

    df = pd.DataFrame(np.random.randint(down, up, size=(line, 5)), columns=(df_col_lis))

    df['a1'] = '+'
    df['a3'] = '='
    df['a0'] = '(    )'

    for i in range(line):
        if df.loc[i, 'a2'] > df.loc[i, 'a4']:
            df.loc[i, 'a2'], df.loc[i, 'a4'] = df.loc[i, 'a4'], df.loc[i, 'a2']
    return df


# model4：减法，括号在最后
def model4():
    df_col_lis = ['a' + str(x) for x in range(5)]

    df = pd.DataFrame(np.random.randint(down, up, size=(line, 5)), columns=(df_col_lis))

    df['a1'] = '-'
    df['a3'] = '='
    df['a4'] = '(    )'

    for i in range(line):
        if df.loc[i, 'a0'] < df.loc[i, 'a2']:
            df.loc[i, 'a0'], df.loc[i, 'a2'] = df.loc[i, 'a2'], df.loc[i, 'a0']
    return df


# model5：减法，括号在中间
def model5():
    df_col_lis = ['a' + str(x) for x in range(5)]

    df = pd.DataFrame(np.random.randint(down, up, size=(line, 5)), columns=(df_col_lis))

    df['a1'] = '-'
    df['a3'] = '='
    df['a2'] = '(    )'

    for i in range(line):
        if df.loc[i, 'a0'] < df.loc[i, 'a4']:
            df.loc[i, 'a0'], df.loc[i, 'a4'] = df.loc[i, 'a4'], df.loc[i, 'a0']
    return df


# model6：减法，括号在前面
def model6():
    lis = []
    df_col_lis = ['a' + str(x) for x in range(5)]

    df = pd.DataFrame(np.random.randint(down, up, size=(line, 5)), columns=(df_col_lis))
    arr = df['a4']

    df['a1'] = '-'
    df['a3'] = '='
    df['a0'] = '(    )'

    for i in arr:
        a = random.randint(0, up - i)
        lis.append(a)
    df['a2'] = lis
    return df


def get_one_col():
    df1 = model1()
    df2 = model2()
    df3 = model3()
    df4 = model4()
    df5 = model5()
    df6 = model6()
    # 纵向拼接+随机重排
    df_res = pd.concat([df1, df2, df3, df4, df5, df6], axis=0)
    temp = list(range(df_res.shape[0]))
    df_res['a5'] = np.random.choice(a=temp, size=df_res.shape[0], replace=False)
    df_res.sort_values(by='a5', axis=0, ascending=True, inplace=True)
    df_res.reset_index(inplace=True, drop=True)
    del df_res['a5']
    return df_res


# a = get_one_col()


# 横向循环拼接
df_final = pd.DataFrame()
for j in range(col_num):
    df_temp = get_one_col()
    df_final = pd.concat([df_final, df_temp], axis=1)
    df_final.reset_index(inplace=True, drop=True)

df_col_lis2 = ['a' + str(x) for x in range(15)]
df_final.columns = df_col_lis2
df_final[['a3', 'a8', 'a13']] = ' ='  # 调整等号位置

writer = pd.ExcelWriter(r'C:\Users\yin\Desktop\加减混合随机10-20.xlsx')  # , sheet_name = '加减混合'
df_final.to_excel(writer, index=False, header=None)
writer.save()
writer.close()
