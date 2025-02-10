import streamlit as st
import sys
import os
import pydeck as pdk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.use_case.insights.insights import Insights
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData



insights = Insights(PandasDataFrame())
dataCaseFlow = ReadCaseFlowData(PandasDataFrame())

@st.cache_data
def get_data():
    return dataCaseFlow.getData("Case", "true")

data = insights.totalUf(get_data())

st.title("Maps Test")


layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position=["longitude", "latitude"],
    get_radius="uf_count",
    get_color=[255, 75, 75],
    pickable=True,
    auto_highlight=True
)

view_state = pdk.ViewState(
    latitude=-23.5505,
    longitude=-46.6333,
    zoom=5,
    pitch=0, # Inclinação do mapa (0 = plano, 45 = inclinado, 60 = quase deitado, 90 = deitado)
)

tooltip = {
    "html": "<b>UF:</b> {uf}<br/><b>Total:</b> {uf_count}<br/><b>Valor:</b> {value_cause:,.2f}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "red"
    }
}

# Renderizando no Streamlit
st.pydeck_chart(
    pdk.Deck(
        layers=layer,
        initial_view_state=view_state,
        tooltip=tooltip
    )
)

st.write(tooltip)