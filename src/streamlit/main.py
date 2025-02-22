import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import streamlit as st
import plotly.express as px

from src.adapter.dataframe.pandas.index import PandasDataFrame
from src.use_case.insights.insights import Insights
from src.use_case.dataCaseFlow.readData import ReadCaseFlowData
from src.use_case.dataDataJud.readDataJud import ReadDataJud
from src.utils.utils import Utils
from src.use_case.dataEscavador.readDataEscavador import ReadEscavador

insights = Insights(PandasDataFrame())
dataCaseFlow = ReadCaseFlowData(PandasDataFrame())
dataJud = ReadDataJud(PandasDataFrame())
escavador = ReadEscavador(PandasDataFrame())
util = Utils()


# Variaveis com os dataframes

dfCaseFlow = dataCaseFlow.getData(
    table="Case", 
    activedFilter="True", 
    removeSpecialCharacters=True
)

dfEscavador = escavador.getData()

dfDataJud, notFoundProcess = dataJud.readDataJud()
allMoviments = dataJud.getAllMoviments()


# Insights:

thirtyDays = insights.distributionData(
    dfCaseFlow, 
    "distribution_date"
)

dfUf = insights.totalUf(dfCaseFlow)

st.title("Jurimetria")

with st.sidebar:
    st.title("Filtros")
    

    numberProcess = st.text_input(
        "Numero Processo", 
        value="", 
        placeholder="Digite o numero do processo"
    )
    
    st.text_input("UF", value="", placeholder="Digite o UF")
    
    client = st.multiselect(
        "Cliente", 
        dfEscavador["cliente"].unique(), 
        placeholder="Selecione o Cliente"
    )
    
    st.text_input("Advogado", value="", placeholder="Digite o nome do Advogado")
    
    tribunal = st.multiselect(
        "Tribunal", 
        dfEscavador["tribunal"].unique(), 
        placeholder="Selecione o Tribunal"
    )



poloAtivo, poloPassivo = escavador.processAtivoPassivo(dfEscavador, numberProcess)


st.write(f"Ativo: {poloAtivo} x Passivo: {poloPassivo}")


# Métricas:

qtdProcess, distributionData, notFound = st.columns(3)

qtdProcess.metric(
    "Quantidade de processos", 
    dfCaseFlow.shape[0]
)

notFound.metric(
    "Processos não encontrados", 
    notFoundProcess.shape[0],
    help="Processos não encontrados no DataJud"
)

distributionData.metric(
    "Distribuidos nos Ultimos 30 dias", 
    thirtyDays
)

st.subheader("Processos não encontrados")

if notFoundProcess.shape[0] > 0:
    st.write(notFoundProcess)
else:
    st.write("Todos os Processos Encontrados")


st.subheader("Quantidade de Processos por Status")
st.dataframe(
    dataJud.totalStatus(
        allMoviments.explode(
            "movimentos"
        ),
        numberProcess
    )
)


st.subheader("Quantidade das causas por UF")

fig = px.bar(
    dfUf, 
    x="uf", 
    y="uf_count",
    title="Quantidade de causas por UF",
    labels={"uf_count": "Quantidade de causas", "uf": "UF"},
    color="uf",
    category_orders={"uf_count": dfUf["uf_count"].tolist()},
    text="uf_count"
)

fig.update_traces(textposition='outside')

st.plotly_chart(fig)

st.subheader("Tempo de Tramiatação dos Processos")
st.dataframe(
    dataJud.meanDateProcess(
        allMoviments.explode(
            [
                "movimentos", 
                "dataMovimentacao"
            ]
        ),
        numberProcess
    )
)

st.subheader("Quantidades por Tribunal")
st.dataframe(
    escavador.totalTribunal(
        dfEscavador, 
        processNumber = None, 
        tribunal = tribunal, 
        client=None
    )
)