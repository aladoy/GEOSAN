import numpy as np
import pandas as pd
import math

def select_var_limites(var_name, gdf, gdf_kept):

    df = pd.read_csv("./legend/ha_indicators_legend.csv")


    var_values = gdf[var_name]
    max_canto = np.nanmax(var_values)
    min_canto = np.nanmin(var_values)

    df_kept = df[df['var'] == var_name]
    unit = df_kept['unit'].iloc[0]

    jul = df_kept['x1_value'].iloc[0]
    jul_2 = float(df_kept['x1_value'].to_list()[0])

    if max_canto <= df_kept['x4_value'].iloc[0]:
        max_canto = df_kept['x4_value'].iloc[0] + 1
    
    if min_canto >= df_kept['x1_value'].iloc[0]:
        min_canto = df_kept['x1_value'].iloc[0] -1

    if min_canto < 0 :
        min_canto = 0
    
    if unit == "[%]":
        min_canto = 0
        max_canto = 100

    time_list = ["ER_TIME","DENTAL_TIME","PHARMA_TIME","AMBU_TIME","PLAYGRD_TIME"]
    if var_name in time_list :
        max_canto = gdf_kept[var_name].max()
        if max_canto <= df_kept['x4_value'].iloc[0]:
            max_canto = df_kept['x4_value'].iloc[0] + 5

    if var_name == "AVG_PPH" or var_name == "MEDREV":
        max_canto = gdf_kept[var_name].max()
        if max_canto <= df_kept['x4_value'].iloc[0]:
            max_canto = df_kept['x4_value'].iloc[0] + 10

    x_list = [min_canto, df_kept['x1_value'].iloc[0],df_kept['x2_value'].iloc[0],df_kept['x3_value'].iloc[0],df_kept['x4_value'].iloc[0], max_canto]
    x_text = [df_kept['x1_label'].iloc[0],df_kept['x2_label'].iloc[0],df_kept['x3_label'].iloc[0],df_kept['x4_label'].iloc[0]]
    href = [df_kept['x1_hyperlink'].iloc[0],df_kept['x2_hyperlink'].iloc[0],df_kept['x3_hyperlink'].iloc[0],df_kept['x4_hyperlink'].iloc[0]]

    limitations_informations = ""
    
    limitations_informations = "* " + limitations_informations

    return x_list, x_text, limitations_informations, unit, href

def get_var_from_post(var_name_disp):
    
    indicators = pd.read_csv('./legend/ha_indicators_legend.csv', encoding='utf-8')

    var_name = indicators[indicators['var_descr'].str.contains(var_name_disp)]['var'].iloc[0]

    return var_name