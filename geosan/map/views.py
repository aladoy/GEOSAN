# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponseRedirect
import folium
from branca.colormap import linear
from branca.colormap import LinearColormap
from branca.colormap import StepColormap
import pandas as pd
from .models import Communes
import geopandas as gpd
from . import forms
from folium import plugins
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import *
import numpy as np
from folium.plugins import FloatImage, MarkerCluster, FeatureGroupSubGroup
from map.utils import *
from map.utils_var import *
import json
import re
import time
from shapely.geometry import shape
from pyproj import CRS

# Create your views here.


def index(request):

    t_init = time.time()
    m = folium.Map(
        location=[46.61280022381356, 6.61517533257687],
        tiles=None,
        # tiles='OpenStreetMap',
        min_lat=46.2,
        max_lat=47.3,
        min_lon=5.9,
        max_lon=7.2,
        zoom_start=10,
        max_zoom=15,
        min_zoom=9,
        zoom_control=False,
    )
    folium.TileLayer("cartodbpositron", control=False).add_to(m)

    control = folium.LayerControl()

    chart = ""
    hist = ""
    legend_color_scale = ""
    legend_text = ""
    commune_request_name = ""
    current_commune_text = ""
    var_name = ""
    var_name_descr = ""
    limitations_informations = ""
    unit = ""
    legend_moyenne_text = ""

    # gdf_municipalities = gpd.read_file('./geojson/typology_municipalities_4326_simplified.geojson')
    gdf_municipalities = gpd.read_file(
        "./geojson/municipalities_4326_simplified.geojson"
    )

    communes_names = gdf_municipalities["MUN_NAME"]
    communes_names = sorted(communes_names)

    highlight_function = lambda x: {
        "color": "red",  # stroke becomes red
        "opacity": 0.9,
        "weight": 4,
        "dashArray": "3, 6",  # transforms the solid stroke to a dashed stroke
    }

    geojson_dir = geojson_dir = os.path.join(os.getcwd(), "geojson")
    typo_group = add_base_layers(m, highlight_function, geojson_dir, gdf_municipalities)
    add_base_places(m, geojson_dir)

    # add_categorical_legend(m)

    # Polutate

    indicators = pd.read_csv("./legend/ha_indicators_legend.csv", encoding="utf-8")
    list_env_descr = []
    list_demo_descr = []
    list_accessibility_descr = []
    list_socio_eco_descr = []

    list_env = ["NO2", "PM10", "PM25", "NOISE", "LST", "ENV_INDEX"]
    for elem in list_env:
        list_env_descr.append(
            indicators[indicators["var"] == elem]["var_descr"].iloc[0]
        )
    list_env_descr_enum = enumerate(list_env_descr)

    list_demo = [
        "RP0014",
        "RP1524",
        "RP2564",
        "RP65M",
        "RP80M",
        "RP0014_F",
        "RP1524_F",
        "RP2564_F",
        "RP65M_F",
        "RP80M_F",
        "RP0014_M",
        "RP1524_M",
        "RP2564_M",
        "RP65M_M",
        "RP80M_M",
    ]
    for elem in list_demo:
        list_demo_descr.append(
            indicators[indicators["var"] == elem]["var_descr"].iloc[0]
        )
    list_demo_descr_enum = enumerate(list_demo_descr)

    list_accessibility = [
        "ER_TIME",
        "DENTAL_TIME",
        "PHARMA_TIME",
        "AMBU_TIME",
        "D_MEDIC",
        "D_SCHOOL_O",
        "D_SCHOOL_S",
        "D_EDUC",
        "D_SECURITY",
        "N_ACC_PED",
        "N_ACC_BIC",
        "D_GROCERY",
        "PLAYGRD_TIME",
        "D_FOREST",
        "D_LAKE",
        "D_SPORT",
        "D_SWIM",
        "D_STOP_TOT",
        "GREEN_SP",
        "BLUE_SP",
        "HEALTHCARE_INDEX",
    ]
    for elem in list_accessibility:
        list_accessibility_descr.append(
            indicators[indicators["var"] == elem]["var_descr"].iloc[0]
        )
    list_accessibility_descr_enum = enumerate(list_accessibility_descr)

    list_socio_eco = [
        "R_PLA",
        "AVG_PPH",
        "MEDREV",
        "R_DIV_WID",
        "R_FFB",
        "R_NN_FRA",
        "R_NN_POBL",
        "R_DIS",
        "R_UNEMP",
        "SOC_ECO_INDEX",
    ]
    # list_socio_eco = ["AVG_PPH","R_FFB","R_NN_FRA","R_NN_POBL","R_DIS","R_UNEMP"]

    for elem in list_socio_eco:
        list_socio_eco_descr.append(
            indicators[indicators["var"] == elem]["var_descr"].iloc[0]
        )
    list_socio_eco_descr_enum = enumerate(list_socio_eco_descr)

    if request.method == "POST":

        typo_group.show = False

        selected_list = request.POST.get("var_name")

        match = re.match(r"(\d+)(\D+)", selected_list)
        index_var = int(match.group(1))
        name_var = match.group(2)

        # gdf_municipalities = gpd.read_file('./geojson/typology_municipalities_4326.geojson')

        if any(name_var in x for x in list_env_descr):
            var_name = list_env[index_var]
            var_name_descr = list_env_descr[index_var]

        elif any(name_var in x for x in list_demo_descr):
            var_name = list_demo[index_var]
            var_name_descr = list_demo_descr[index_var]

        elif any(name_var in x for x in list_accessibility_descr):
            var_name = list_accessibility[index_var]
            var_name_descr = list_accessibility_descr[index_var]

        elif any(name_var in x for x in list_socio_eco_descr):
            var_name = list_socio_eco[index_var]
            var_name_descr = list_socio_eco_descr[index_var]

        t_init = time.time()
        """gdf = gpd.read_file("./geojson/ha_indicators_4326.geojson")
        list_var = ["NO2","PM10","PM25","NOISE","LST","ENV_INDEX", "RP0014","RP1524","RP2564","RP65M","RP80M","RP0014_F","RP1524_F","RP2564_F","RP65M_F","RP80M_F","RP0014_M","RP1524_M","RP2564_M","RP65M_M","RP80M_M", "ER_TIME","DENTAL_TIME","PHARMA_TIME","AMBU_TIME","D_MEDIC","D_SCHOOL_O","D_SCHOOL_S","D_EDUC","D_SECURITY","N_ACC_PED","N_ACC_BIC","D_GROCERY","PLAYGRD_TIME","D_FOREST","D_LAKE","D_SPORT","D_SWIM","D_STOP_TOT","GREEN_SP","BLUE_SP","HEALTHCARE_INDEX", "R_PLA","AVG_PPH","MEDREV","R_DIV_WID","R_FFB","R_NN_FRA","R_NN_POBL","R_DIS","R_UNEMP","SOC_ECO_INDEX"]
        
        for var in list_var:
            gdf_var = gdf[['RELI','MUN_OFS_ID','MUN_NAME',var,'PTOT','geometry']]
            gdf_var.to_file("./GPKG/ha_indicators_4326.gpkg" , layer=var, driver='GPKG')
            print("Var :"+var)"""

        # gdf = gpd.read_file("./GPKG/ha_indicators_4326_"+var_name+".gpkg")
        gdf = gpd.read_file("./GPKG/ha_indicators_4326.gpkg", layer=var_name)
        print(gdf)

        # recuperer le nom de la commune qui commence par les memes caracteres :
        communes_liste = gdf["MUN_NAME"].tolist()

        commune_request_name = request.POST["commune_name"]
        for nom_commune in communes_liste:
            if nom_commune.startswith(commune_request_name):
                commune_request_name = nom_commune

        commune_numero = gdf_municipalities[
            gdf_municipalities["MUN_NAME"] == commune_request_name
        ]["MUN_OFS_ID"].iloc[0]

        print("----------------------------")
        print(str(time.time() - t_init))
        # gdf = gpd.read_file("./GPKG/ha_indicators_4326.gpkg", layer=var_name)

        map_dict = gdf.set_index("RELI")[var_name].to_dict()
        gdf_kept = gdf[gdf["MUN_OFS_ID"] == commune_numero]

        mean_commune = gdf_kept[var_name].mean()

        gdf_to_dissolve = gdf_kept[["MUN_OFS_ID", "geometry"]]
        gdf_to_dissolve = gdf_to_dissolve.to_crs("2056")
        gdf_to_dissolve = gdf_to_dissolve.dissolve(by="MUN_OFS_ID").centroid

        m.location = [gdf_to_dissolve[0].y, gdf_to_dissolve[0].x]

        hec_group = folium.FeatureGroup(name=var_name)

        [x_list, x_text, limitations_informations, unit, href] = select_var_limites(
            var_name, gdf, gdf_kept
        )

        x_vect = [
            x_list[0] + (x_list[1] - x_list[0]) / 2,
            x_list[1] + (x_list[2] - x_list[1]) / 2,
            x_list[2] + (x_list[3] - x_list[2]) / 2,
            x_list[3] + (x_list[4] - x_list[3]) / 2,
            x_list[4] + (x_list[5] - x_list[4]) / 2,
        ]

        width_vect = [
            x_list[1] - x_list[0],
            x_list[2] - x_list[1],
            x_list[3] - x_list[2],
            x_list[4] - x_list[3],
            x_list[5] - x_list[4],
        ]
        color_vect = []

        for elem in x_vect:
            color_vect.append(
                get_color_discrete_value(
                    elem, x_list[1], x_list[2], x_list[3], x_list[4]
                )
            )

        data_tuples = list(zip(x_vect, width_vect, color_vect))
        df_test = pd.DataFrame(data_tuples, columns=["x", "width", "color"])

        [
            legend_color_scale,
            legend_text,
            hist,
            chart,
            legend_moyenne_text,
        ] = add_informations(
            df_test,
            x_list,
            mean_commune,
            gdf_kept,
            var_name,
            map_dict,
            x_text,
            unit,
            commune_request_name,
            href,
            var_name_descr,
        )

        gdf_kept_1 = gdf_kept[["MUN_NAME", var_name, "PTOT", "geometry"]]
        folium.GeoJson(
            gdf_kept_1,
            name="geojson",
            zoom_on_click=False,
            # tooltip=folium.GeoJsonTooltip(fields=['MUN_NAME', var_name, 'PTOT'],aliases=['Nom de la commune', 'Valeur',"Population totale de l'hectare"]),
            tooltip=folium.GeoJsonTooltip(
                fields=["MUN_NAME", var_name, "PTOT"],
                aliases=[
                    "Nom de la commune",
                    "Valeur " + unit,
                    "Population totale de l'hectare",
                ],
            ),
            style_function=lambda feature: {
                "fillColor": get_color_discrete(
                    feature, var_name, x_list[1], x_list[2], x_list[3], x_list[4]
                ),
                "fillOpacity": 0.8,
                "weight": 0.1,
            },
            highlight_function=highlight_function,
        ).add_to(hec_group)

        m.fit_bounds(hec_group.get_bounds())

        """gdf_communes = gpd.read_file('./shapefiles/Caracterisation_PCA_simplified.shp')

        commune_a_intersecter_geom = gdf_communes[gdf_communes['Nom_CMN']==commune_request_name].geometry.buffer(1000)

        gdf_communes_geom = gdf_communes.geometry

        result_touches = gdf_communes_geom.intersects(commune_a_intersecter_geom.iloc[0])
        
        communes_kept_indexes = []"""

        gdf_municipalities_projected = gdf_municipalities.to_crs(CRS.from_epsg(2056))
        commune_a_intersecter_geom = gdf_municipalities_projected[
            gdf_municipalities_projected["MUN_NAME"] == commune_request_name
        ].geometry.buffer(1000)
        result_touches = gdf_municipalities_projected.geometry.intersects(
            commune_a_intersecter_geom.iloc[0]
        )

        communes_kept_indexes = []

        for index, elem in enumerate(result_touches):
            if elem == True:
                name_of_commune = gdf_municipalities.iloc[index].MUN_NAME
                # print(gdf_municipalities)
                # print(index)
                # name_of_commune = gdf_municipalities.iloc[index].MUN_NAME
                communes_kept_indexes.append(index)
                print("name of commune :")
                print(name_of_commune)

                for nom_commune in communes_liste:
                    if nom_commune.startswith(name_of_commune):
                        name_of_commune = nom_commune

                print(name_of_commune)

                if name_of_commune != commune_request_name:
                    folium.GeoJson(
                        gdf[gdf["MUN_NAME"] == name_of_commune][
                            ["MUN_NAME", var_name, "PTOT", "geometry"]
                        ],
                        name="geojson",
                        zoom_on_click=False,
                        tooltip=folium.GeoJsonTooltip(
                            fields=["MUN_NAME", var_name, "PTOT"],
                            aliases=[
                                "Nom de la commune",
                                "Valeur " + unit,
                                "Population totale de l'hectare",
                            ],
                        ),
                        style_function=lambda feature: {
                            "fillColor": get_color_discrete(
                                feature,
                                var_name,
                                x_list[1],
                                x_list[2],
                                x_list[3],
                                x_list[4],
                            ),
                            "fillOpacity": 0.8,
                            "weight": 0.1,
                        },
                        highlight_function=highlight_function,
                    ).add_to(hec_group)

        hec_group.add_to(m)
        m.keep_in_front(hec_group)

        current_commune_text = (
            commune_request_name + " - " + var_name_descr + " " + unit
        )

    control.add_child(
        folium.IFrame(
            html='<a href="https://www.example.com">Visiter le site web</a>',
            width=200,
            height=100,
        )
    )
    control.add_to(m)
    m = m._repr_html_()
    context = {
        "m": m,
        "communes_names": communes_names,
        "list_env": list_env_descr_enum,
        "list_demo": list_demo_descr_enum,
        "list_accessibility": list_accessibility_descr_enum,
        "list_socio_eco": list_socio_eco_descr_enum,
        "chart": chart,
        "hist": hist,
        "legend_color_scale": legend_color_scale,
        "legend_text": legend_text,
        "legend_moyenne_text": legend_moyenne_text,
        "current_commune_name": commune_request_name,
        "limitations_informations": limitations_informations,
        "current_commune_text": current_commune_text,
        "var_name": var_name,
        "var_name_descr": var_name_descr,
    }

    return render(request, "index.html", context)


def typologie(request):

    m = folium.Map(
        location=[46.61280022381356, 6.61517533257687],
        tiles=None,
        min_lat=46.2,
        max_lat=47.3,
        min_lon=5.9,
        max_lon=7.2,
        zoom_start=9,
        max_zoom=15,
        min_zoom=9,
        zoom_control=False,
        prefer_canvas=True,
    )
    folium.TileLayer("cartodbpositron", control=False).add_to(m)

    highlight_function = lambda x: {
        "color": "red",  # stroke becomes red
        "opacity": 0.9,
        "weight": 4,
        "dashArray": "3, 6",  # transforms the solid stroke to a dashed stroke
    }

    geojson_dir = geojson_dir = os.path.join(os.getcwd(), "geojson")

    typology_legend = pd.read_csv("./legend/typology_legend.csv", encoding="utf-8")

    colors = typology_legend["hex_color"]

    colormap = StepColormap(
        colors,
        index=range(len(colors) + 1),
        vmin=1,
        vmax=len(colors) + 1,
        caption="Color Map",
    )

    gdf_municipalities = gpd.read_file(
        os.path.join(geojson_dir, "typology_municipalities_4326_simplified.geojson")
    )

    typo_group = folium.FeatureGroup(name="Typologie")
    folium.GeoJson(
        gdf_municipalities,
        name="geojson",
        zoom_on_click=True,
        overlay=False,
        tooltip=folium.GeoJsonTooltip(
            fields=["MUN_NAME", "GROUP_ID", "shortname", "PTOT"],
            aliases=[
                "Nom de la commune",
                "Classe de typologie",
                "Typologie description",
                "Population totale",
            ],
        ),
        style_function=lambda feature: {
            "fillColor": colormap(feature["properties"]["GROUP_ID"]),
            "fillOpacity": 0.6,
            "weight": 1,
            "color": "white",
        },
        highlight_function=highlight_function,
    ).add_to(typo_group)
    typo_group.add_to(m)
    m.keep_in_front(typo_group)

    class_id = typology_legend["group_id"]

    typo_title = typology_legend["shortname"]
    stats = typology_legend["stats"]
    description = typology_legend["full_descr"]

    typo_list = zip(class_id, colors, typo_title, stats, description)

    is_all_communes = True

    if request.method == "POST":

        m = folium.Map(
            location=[46.61280022381356, 6.61517533257687],
            tiles=None,
            min_lat=46.2,
            max_lat=47.3,
            min_lon=5.9,
            max_lon=7.2,
            zoom_start=10,
            max_zoom=15,
            min_zoom=9,
            zoom_control=False,
            prefer_canvas=True,
        )
        folium.TileLayer("cartodbpositron", control=False).add_to(m)

        category_numero = int(request.POST["category"])
        gdf = gdf_municipalities  # gpd.read_file(os.path.join(geojson_dir,'typology_municipalities_4326.geojson'))
        if category_numero < 10:
            gdf_sorted = gdf[gdf["GROUP_ID"] == category_numero]
            folium.GeoJson(
                gdf_sorted,
                name="geojson",
                zoom_on_click=True,
                overlay=False,
                tooltip=folium.GeoJsonTooltip(
                    fields=["MUN_NAME", "GROUP_ID"],
                    aliases=["Nom de la commune", "Classe de typologie"],
                ),
                style_function=lambda feature: {
                    "fillColor": colormap(category_numero),
                    "fillOpacity": 0.6,
                    "weight": 1,
                    "color": "white",
                },
                highlight_function=highlight_function,
            ).add_to(m)
            is_all_communes = False
        else:
            # gdf_sorted = gdf
            folium.GeoJson(
                gdf_municipalities,
                name="geojson",
                zoom_on_click=True,
                overlay=False,
                tooltip=folium.GeoJsonTooltip(
                    fields=["MUN_NAME", "GROUP_ID", "shortname", "PTOT"],
                    aliases=[
                        "Nom de la commune",
                        "Classe de typologie",
                        "Typologie description",
                        "Population totale",
                    ],
                ),
                style_function=lambda feature: {
                    "fillColor": colormap(feature["properties"]["GROUP_ID"]),
                    "fillOpacity": 0.6,
                    "weight": 1,
                    "color": "white",
                },
                highlight_function=highlight_function,
            ).add_to(m)
            is_all_communes = True

    m = m._repr_html_()
    context = {"m": m, "typo_list": typo_list, "is_all_communes": is_all_communes}

    map_html = request.session.get("m")

    return render(request, "typologie.html", context)


def add_base_layers(m, highlight_function, geojson_dir, gdf_municipalities):

    typology_legend = pd.read_csv("./legend/typology_legend.csv", encoding="utf-8")
    colors = typology_legend["hex_color"]
    colormap = StepColormap(
        colors,
        index=range(len(colors) + 1),
        vmin=1,
        vmax=len(colors) + 1,
        caption="Color Map",
    )

    ################ COMMUNES ##############################################################
    communes_group = folium.FeatureGroup(name="Communes", control=False)
    folium.GeoJson(
        gdf_municipalities[["MUN_NAME", "PTOT", "geometry"]],
        name="geojson",
        zoom_on_click=True,
        tooltip=folium.GeoJsonTooltip(
            fields=["MUN_NAME", "PTOT"],
            aliases=["Nom de la commune", "Population totale"],
        ),
        # tooltip=folium.GeoJsonTooltip(fields=['MUN_NAME', 'PTOT','shortname'], aliases=['Nom de la commune', 'Population totale','Description de la typologie']),
        style_function=lambda feature: {
            "fillOpacity": 0,
            "weight": 1,
            "color": "black",
        },
        highlight_function=highlight_function,
        smooth_factor=0.1,
    ).add_to(communes_group)
    communes_group.add_to(m)

    gdf_municipalities = gpd.read_file(
        "./geojson/typology_municipalities_4326_simplified.geojson"
    )
    ################ Typologie ##############################################################

    typo_group = folium.FeatureGroup(name="Typologie")
    folium.GeoJson(
        gdf_municipalities[["MUN_NAME", "GROUP_ID", "shortname", "PTOT", "geometry"]],
        name="geojson",
        zoom_on_click=True,
        overlay=False,
        tooltip=folium.GeoJsonTooltip(
            fields=["MUN_NAME", "GROUP_ID", "shortname", "PTOT"],
            aliases=[
                "Nom de la commune",
                "Classe de typologie",
                "Description de la typologie",
                "Popultation totale",
            ],
        ),
        style_function=lambda feature: {
            "fillColor": colormap(feature["properties"]["GROUP_ID"]),
            "fillOpacity": 0.6,
            "weight": 1,
            "color": "white",
        },
        highlight_function=highlight_function,
    ).add_to(typo_group)
    typo_group.add_to(m)
    m.keep_in_front(typo_group)

    return typo_group


def add_base_places(m, geojson_dir):

    fg = MarkerCluster(
        name="Etablissements", show=False, disableClusteringAtZoom=14, control=False
    )
    m.add_child(fg)
    g = folium.plugins.FeatureGroupSubGroup(
        fg, "Ne pas afficher d'etablissement", overlay=False
    )
    m.add_child(g)

    etablissements_names = ["Pharmacies"]
    etablissement_colors = ["green"]
    etablissements_geojson = ["pharmacies_4326"]

    for index_etablissement, etablissement in enumerate(etablissements_names):
        gdf = gpd.read_file(
            os.path.join(
                geojson_dir, etablissements_geojson[index_etablissement] + ".geojson"
            )
        )
        g = folium.plugins.FeatureGroupSubGroup(fg, etablissement, overlay=False)
        m.add_child(g)
        cluster = MarkerCluster(name=etablissement)
        geo_df = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry]

        for index, coordinates in enumerate(geo_df):

            if etablissement == "Pharmacies":
                iframe = folium.IFrame(
                    "<strong>Nom: </strong>" + str(gdf.nom[index]) + "<br>"
                )
                # + '<strong>Exploitant: </strong>' + str(gdf.EXPLOITANT[index]))

            if etablissement == "Centre medico-social":
                iframe = folium.IFrame(
                    "<strong>Nom: </strong>"
                    + str(gdf.nom[index])
                    + "<br>"
                    + "<strong>Exploitant: </strong>"
                    + str(gdf.EXPLOITANT[index])
                )

            cluster.add_child(
                folium.Marker(
                    location=coordinates,
                    popup=folium.Popup(iframe, min_width=300, max_width=300),
                    icon=folium.Icon(
                        icon="glyphicon-plus",
                        color=etablissement_colors[index_etablissement],
                    ),
                )
            )
        cluster.add_to(g)


def set_layout(fig, min_canto, max_canto, height, var_name, unit):

    fig.update_layout(
        autosize=True,
        height=height,
        margin=dict(l=20, r=20, t=30, b=10),
        xaxis_range=[min_canto, max_canto],
        font=dict(size=10),
        title_font=dict(size=12),
        title_font_family="Helvetica Neue",
        title_font_color="black",
    )

    fig.update_xaxes(title=var_name + " " + unit, title_font={"size": 10})


def set_layout_legend(fig, min_canto, max_canto):

    fig.update_layout(
        autosize=True,
        height=50,
        margin=dict(l=20, r=20, t=10, b=10),
        xaxis_range=[min_canto, max_canto],
        font=dict(size=10),
    )


def add_annotations(fig, x_1, x_2, x_3, x_4):

    fig.add_vline(x=x_1, line_width=1, line_dash="dash", line_color="black")
    fig.add_vline(x=x_2, line_width=1, line_dash="dash", line_color="black")
    fig.add_vline(x=x_3, line_width=1, line_dash="dash", line_color="black")
    fig.add_vline(x=x_4, line_width=1, line_dash="dash", line_color="black")


def set_x_values(x_min, x_1, x_2, x_3, x_4, x_max):
    x_list = [x_min, x_1, x_2, x_3, x_4, x_max]
    return x_list


def add_informations(
    df_test,
    x_list,
    mean_commune,
    gdf_kept,
    var_name,
    map_dict,
    x_text,
    unit,
    commune_name,
    href,
    var_name_descr,
):

    ################### Legend Text ############################################################

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_test["x"],
                y=[1, 1, 1, 1, 1],
                marker={"color": "rgba(0,0,0,0)"},
                width=df_test["width"],
                marker_line_width=0,
            )
        ]
    )
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)

    fig.update_layout(
        height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )

    add_legend_limitations_text(fig, x_list, x_text, href, y=0.25)

    config = {"staticPlot": True}

    fig.update_layout(
        autosize=True,
        height=30,
        margin=dict(l=20, r=20, t=5, b=0),
        xaxis_range=[x_list[0], x_list[5]],
    )

    legend_text = fig.to_html(config=config)

    ############ Legend ##############################################
    invert_color_list = ["GREEN_SP", "BLUE_SP", "MEDREV"]
    if var_name in invert_color_list:
        df_test["color"] = np.flip(df_test["color"].values)

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_test["x"],
                y=[1, 1, 1, 1, 1],
                marker={"color": df_test["color"]},
                width=df_test["width"],
            )
        ]
    )

    fig.update_yaxes(visible=False)

    config = {"staticPlot": True}

    set_layout_legend(fig, x_list[0], x_list[5])

    add_annotations(fig, x_list[1], x_list[2], x_list[3], x_list[4])
    # fig.add_annotation(x=mean_commune, y=0.5 , text="Moyenne communale", font=dict(size=10),showarrow=False,)
    fig.add_vline(x=mean_commune, line_width=2, line_color="blue")

    legend_color_scale = fig.to_html(config=config)

    ########### moyenne communale #######################################

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_test["x"],
                y=[1, 1, 1, 1, 1],
                marker={"color": "rgba(0,0,0,0)"},
                width=df_test["width"],
                marker_line_width=0,
            )
        ]
    )
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)

    fig.update_layout(
        height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )

    config = {"staticPlot": True}

    fig.update_layout(
        autosize=True,
        height=30,
        margin=dict(l=20, r=20, t=0, b=0),
        xaxis_range=[x_list[0], x_list[5]],
    )
    fig.add_annotation(
        x=mean_commune,
        y=1,
        text="<b>Moyenne</b>",
        font=dict(size=10),
        showarrow=False,
    )
    fig.add_annotation(
        x=mean_commune,
        y=0.5,
        text="<b>Communale</b>",
        font=dict(size=10),
        showarrow=False,
    )
    legend_moyenne_text = fig.to_html(config=config)

    ################### HISTOGRAM ########################################################

    fig = px.histogram(
        gdf_kept,
        x=var_name,
        range_x=[min(map_dict.values()), max(map_dict.values())],
        title=commune_name + " : Histogram des valeurs communales",
    )

    add_annotations(fig, x_list[1], x_list[2], x_list[3], x_list[4])
    set_layout(fig, x_list[0], x_list[5], 200, var_name_descr, unit)
    fig.update_yaxes(visible=False, showticklabels=False)

    hist = fig.to_html()

    ################### BOXPLOT ##########################################################

    fig = px.box(
        gdf_kept,
        x=var_name,
        range_x=[min(map_dict.values()), max(map_dict.values())],
        title=commune_name + " : boxplot des valeurs communales",
    )

    add_annotations(fig, x_list[1], x_list[2], x_list[3], x_list[4])
    set_layout(fig, x_list[0], x_list[5], 200, var_name_descr, unit)

    chart = fig.to_html()

    return legend_color_scale, legend_text, hist, chart, legend_moyenne_text


def select_var_lim_names(var_name):
    if var_name == "PM10":
        x_text = ["25 % Quantile", "Mediane", "WHO", "Opair"]
        href = [
            "",
            "",
            """<a href="https://www.who.int/health-topics/air-pollution#tab=tab_1"><b>""",
            """<a href="https://www.fedlex.admin.ch/eli/cc/1986/208_208_208/fr"><b>""",
        ]

    if var_name == "NOISE":
        x_text == ["No effect", "slice effect", "effect", "dangerous situation"]
        href = ["", "", "", "", ""]

    return x_text, href


def add_legend_limitations_text(fig, x_list, x_text, href, y):
    if href[0] != "":
        fig.add_annotation(
            x=x_list[1],
            y=1,
            text=href[0] + x_text[0] + """</b></a>""",
            font=dict(size=10),
            showarrow=False,
        )
    else:
        fig.add_annotation(
            x=x_list[1],
            y=1,
            text=x_text[0],
            font=dict(size=10),
            showarrow=False,
        )

    if href[1] != "":
        fig.add_annotation(
            x=x_list[2],
            y=0,
            text=href[1] + x_text[1] + """</b></a>""",
            font=dict(size=10),
            showarrow=False,
        )
    else:
        fig.add_annotation(
            x=x_list[2],
            y=0,
            text=x_text[1],
            font=dict(size=10),
            showarrow=False,
        )

    if href[2] != "":
        fig.add_annotation(
            x=x_list[3],
            y=1,
            text=href[2] + x_text[2] + """</b></a>""",
            font=dict(size=10),
            showarrow=False,
        )
    else:
        fig.add_annotation(
            x=x_list[3],
            y=1,
            text=x_text[2],
            font=dict(size=10),
            showarrow=False,
        )

    if href[3] != "":
        fig.add_annotation(
            x=x_list[4],
            y=0,
            text=href[3] + x_text[3] + """</b></a>""",
            font=dict(size=10),
            showarrow=False,
        )
    else:
        fig.add_annotation(
            x=x_list[4],
            y=0,
            text=x_text[3],
            font=dict(size=10),
            showarrow=False,
        )


def get_color_discrete_access(feature, var_name, min, range):
    value = feature["properties"][var_name]
    if value is None:
        return "#8c8c8c"
    if value <= min + range / 5:
        return " #32ff6a "
    elif value <= min + 2 * range / 5:
        return "#cdff32"
    elif value <= min + 3 * range / 5:
        return "#f6ff32"
    elif value <= min + 4 * range / 5:
        return "#ffca32"
    else:
        return "#ff0b0b"


def get_color_discrete(feature, var_name, x1, x2, x3, x4):
    value = feature["properties"][var_name]
    invert_color_list = ["GREEN_SP", "BLUE_SP", "MEDREV"]
    if value is None:
        return "#8c8c8c"
    if var_name in invert_color_list:
        if value <= x1:
            return "#ff0b0b"
        elif value <= x2:
            return "#ffca32"
        elif value <= x3:
            return "#f6ff32"
        elif value <= x4:
            return "#cdff32"
        else:
            return "#32ff6a"
    else:
        if value <= x1:
            return "#32ff6a"
        elif value <= x2:
            return "#cdff32"
        elif value <= x3:
            return "#f6ff32"
        elif value <= x4:
            return "#ffca32"
        else:
            return "#ff0b0b"


def get_color_access(val, min, range):
    value = val
    if value is None:
        return "#8c8c8c"
    if value <= min + range / 5:
        return "#32ff6a"
    elif value <= min + 2 * range / 5:
        return "#cdff32"
    elif value <= min + 3 * range / 5:
        return "#f6ff32"
    elif value <= min + 4 * range / 5:
        return "#ffca32"
    else:
        return "#ff0b0b"


def get_color_discrete_value(val, x1, x2, x3, x4):
    value = val
    if value is None:
        return "#8c8c8c"
    if value <= x1:
        return " #32ff6a "
    elif value <= x2:
        return "#cdff32"
    elif value <= x3:
        return "#f6ff32"
    elif value <= x4:
        return "#ffca32"
    else:
        return "#ff0b0b"
