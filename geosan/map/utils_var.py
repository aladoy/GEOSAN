import numpy as np
import pandas as pd
import math

def select_var_limites(var_name, gdf):

    df = pd.read_csv("./legend/ha_indicators_legend.csv")


    var_values = gdf[var_name]
    max_canto = np.nanmax(var_values)
    min_canto = np.nanmin(var_values)


    
    df_kept = df[df['var'] == var_name]

    jul = df_kept['x1_value'].iloc[0]
    jul_2 = float(df_kept['x1_value'].to_list()[0])


    x_list = [min_canto, df_kept['x1_value'].iloc[0],df_kept['x2_value'].iloc[0],df_kept['x3_value'].iloc[0],df_kept['x4_value'].iloc[0], max_canto]
    x_text = [df_kept['x1_label'].iloc[0],df_kept['x2_label'].iloc[0],df_kept['x3_label'].iloc[0],df_kept['x4_label'].iloc[0]]
    href = [df_kept['x1_hyperlink'].iloc[0],df_kept['x2_hyperlink'].iloc[0],df_kept['x3_hyperlink'].iloc[0],df_kept['x4_hyperlink'].iloc[0]]


    limitations_informations = ""
    unit = df_kept['unit'].iloc[0]
    
    '''
    if var_name == 'PM10':

        quantile_25 = gdf[var_name].quantile(0.25)
        var_mediane = gdf[var_name].median()
        WHO = 15
        Opair = 20

        x_list = [min_canto, quantile_25, var_mediane, WHO, Opair, max_canto]

        x_text = ["25 % Quantile","Mediane","WHO","Opair"]
        href = ["",
                "",
                """<a href="https://www.who.int/health-topics/air-pollution#tab=tab_1"><b>""",
                """<a href="https://www.fedlex.admin.ch/eli/cc/1986/208_208_208/fr"><b>"""]
            
        limitations_informations = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        
        unit = "[µg/m3]"

    if var_name == 'NOISE':

        x_list = [min_canto, 30, 40, 55, 65, max_canto]

        x_text = ["slice effect","effect","dangerous situation","LPE"]
        href = ["",
                "",
                "",
                "",
                """<a href="https://www.bafu.admin.ch/bafu/fr/home/themes/bruit/info-specialistes/exposition-au-bruit/valeurs-limites-pour-le-bruit/valeurs-limites-dexposition-au-bruit.html"><b>"""]

        limitations_informations ="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

        unit = "dB(A)"

    '''
    
    limitations_informations = "* " + limitations_informations

    return x_list, x_text, limitations_informations, unit, href

def get_var_from_post(var_name_disp):
    
    indicators = pd.read_csv('./legend/ha_indicators_legend.csv', encoding='utf-8')

    var_name = indicators[indicators['var_descr'].str.contains(var_name_disp)]['var'].iloc[0]

    return var_name