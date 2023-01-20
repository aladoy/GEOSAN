import folium
import os
from branca.element import Template, MacroElement

def add_categorical_legend(m):
    template = """
    {% macro html(this, kwargs) %}

    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>jQuery UI Draggable - Default functionality</title>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

    <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    
    <script>
    $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

    </script>
    </head>
    <body>

    
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:1px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:4px; padding: 5px; font-size:12px; left: 10px; top: 10px;'>
        
    <div class='legend-title' style=" text-align: center;">Typologie</div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background:#76d886;opacity:0.7;'></span>Categorie 1</li>
        <li><span style='background:#a9975e;opacity:0.7;'></span>Categorie 2</li>
        <li><span style='background:#e97c7c;opacity:0.7;'></span>Categorie 3</li>
        <li><span style='background:#a9aac9;opacity:0.7;'></span>Categorie 4</li>
        <li><span style='background:#c293d5;opacity:0.7;'></span>Categorie 5</li>
        <li><span style='background:#e5b2e2;opacity:0.7;'></span>Categorie 6</li>
        <li><span style='background:#a2e587;opacity:0.7;'></span>Categorie 7</li>
        <li><span style='background:#d1f854;opacity:0.7;'></span>Categorie 8</li>
        <li><span style='background:#e9e320;opacity:0.7;'></span>Categorie 9</li>
    </ul>
    </div>
    <div style="text-align: center; font-size: 10px;"><a href='https://www.larousse.fr/dictionnaires/francais/typologie/80387' target="_blank">Details</a></div>
    </div>
    </body>
    </html>

    <style type='text/css'>
    .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
    .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
    .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
    .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 18px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
    .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
    .maplegend a {
        color: #777;
        }
    </style>
    {% endmacro %}"""

    macro = MacroElement()
    macro._template = Template(template)

    m.get_root().add_child(macro)
