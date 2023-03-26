import streamlit as st
import pandas as pd
import numpy as np
import glob
import datetime


lunch_menus = glob.glob('*중식*.xls')
dinner_menus = glob.glob('*석식*.xls')

all_orders = pd.read_pickle('all_orders.pkl')

def find_menu(substring):

    menu_list = []
    type_list = []
    for lunch_menu in lunch_menus:
        menu = pd.read_pickle(lunch_menu + '.pkl')
        menu = menu.replace('\n', '', regex=True)
        menu.replace(np.nan, '', inplace=True)
        for i, s in menu.iterrows():
            for j in s:
                if j != '' and type(j) != int:
                    if j.find(substring) > 0:
                        print(lunch_menu.split(' ')[-2], j[:2].replace('[', '') + '일', j)
                        st.write(lunch_menu.split(' ')[-2] + j[:2].replace('[', '') + '일' + str(j))
                        menu_list.append(lunch_menu.split(' ')[-2] + j[:2].replace('[', '') + '일')
                        type_list.append(j.split("[")[1][:2])

    for dinner_menu in dinner_menus:
        menu = pd.read_pickle(dinner_menu + '.pkl')
        menu = menu.replace('\n', '', regex=True)
        menu.replace(np.nan, '', inplace=True)
        for i, s in menu.iterrows():
            for j in s:
                if j != '' and type(j) != int:
                    if j.find(substring) > 0:
                        print(dinner_menu.split(' ')[-2], j[:2].replace('[', '') + '일', j)
                        st.write(lunch_menu.split(' ')[-2] + j[:2].replace('[', '') + '일' + str(j))
                        menu_list.append(dinner_menu.split(' ')[-2] + j[:2].replace('[', '') + '일')
                        type_list.append(j.split("[")[1][:2])

    yymmdd = [datetime.datetime.strptime(c, "%m월%d일") for c in menu_list]
    return menu_list, type_list, yymmdd

def find_orders(yymmdd, type_list):
    find_all = pd.DataFrame()
    for mmdd, meal in zip(yymmdd, type_list):
        # print(mmdd.month, '월', mmdd.day,'일', meal)
        df = all_orders[(all_orders['식사구분'] == meal) & (all_orders['month'] == mmdd.month) & (all_orders['day'] == mmdd.day)]
        find_all = pd.concat([find_all, df], axis=0)
    return find_all.drop(columns=['친환경인증정보','원산지','수입국','에듀파인전송여부','menu_date'])


if __name__ == '__main__':

    recipe = st.text_input("**레시피를 입력하세요**")


    if recipe:
        menu_list, type_list, yymmdd = find_menu(recipe)
        menu_df = pd.DataFrame({'날짜': menu_list, '식사구분': type_list })
        st.write(menu_df)
        df = find_orders(yymmdd, type_list)
        st.markdown("**필터 전 결과**")
        st.write(df)
        choice = st.sidebar.radio(label="날짜를 선택하세요", options = ['전체'] + menu_list)
        st.markdown("**필터 후 결과**")
        if choice!='전체':
            st.write(df[ (df['month'] == int(choice.split('월')[0])) & ( df['day'] == int(choice.split('월')[1].replace('일','')) )])
        else:
            st.write(df)
