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

dfClients = dataCaseFlow.getClients("Client")

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
    
    client = st.text_input(
        "Cliente",
        placeholder="CPF ou CNPJ do Cliente",
    )
    
    tribunal = st.multiselect(
        "Tribunal", 
        dfEscavador["tribunal"].unique(), 
        placeholder="Selecione o Tribunal"
    )

    status = st.multiselect(
        "Status",
        dfDataJud["movimento"].unique(),
        placeholder="Selecione o Status"
    )


dfTramitacao = dataJud.meanDateProcess(
    allMoviments.explode(
        [
            "movimentos", 
            "dataMovimentacao"
        ]
    ),
    numberProcess
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

# =======================================================================

st.subheader("Processos não encontrados")

if notFoundProcess.shape[0] > 0:
    st.write(notFoundProcess)
else:
    st.write("Todos os Processos Encontrados no DataJud")

# =======================================================================

st.subheader("Quantidade de Processos por Status os Top 10")

totalStatus = dataJud.totalStatus(
    allMoviments.explode(
        "movimentos"
    ),
    numberProcess,
    status).sort_values(by="total", ascending=False).head(10)


figStatus = px.bar(
    totalStatus,
    x="movimentos",
    y="total",
    labels={"total": "Quantidade de Processos", "movimentos": "Status"},
    color="movimentos",
    text="total",
    orientation="v"
)

st.plotly_chart(figStatus, help="Top 10 Status de Processos com mais quantidade")

# =======================================================================
st.subheader("Quantidade das causas por UF")

fig = px.bar(
    dfUf, 
    x="uf", 
    y="uf_count",
    labels={"uf_count": "Quantidade de causas", "uf": "UF"},
    color="uf",
    category_orders={"uf_count": dfUf["uf_count"].tolist()},
    text="uf_count"
)

fig.update_traces(textposition='outside')

st.plotly_chart(fig)

# =======================================================================

st.subheader("Distribuição do tempo de tramitação dos processos (Dias)")

dfTramitacao["tempoTotalTramitacaoDias"] = dfTramitacao["tempoTotalTramitacao"].apply(util.converter_tempo)
dfTramitacao["tempoMedioMovimentacaoDias"] = dfTramitacao["tempoMedioMovimentacao"].apply(util.converter_tempo)

# Converter os valores por dias de tramitação
fig1 = px.histogram(
    dfTramitacao,
    x="tempoTotalTramitacaoDias",
    nbins=20,
    text_auto=True,
)

fig1.update_layout(
    xaxis_title="Dias",
    yaxis_title="Quantidade de Processos",
    bargap=0.1
)

st.plotly_chart(fig1)

st.subheader("Tempo de Tramitação dos Processos")
st.dataframe(
    dfTramitacao
)


# =======================================================================
st.subheader("Quantidade de Movimentação por Data de Movimentação")

figMov = px.line(
    dataJud.qtdMovProcess(dfDataJud),
    x="periodoMovimentacao",
    y="totalMovimentacoes",
    labels={"totalMovimentacoes": "Quantidade de Movimentos", "periodoMovimentacao": "Data Movimentação"},
    text="totalMovimentacoes"
)

figMov.update_traces(textposition='top center')
figMov.update_xaxes(tickangle=45)

st.plotly_chart(figMov)


# =======================================================================
st.subheader("Quantidades por Tribunal")

figtb = px.bar(
    escavador.totalTribunal(
        dfEscavador, 
        processNumber = None, 
        tribunal = tribunal, 
        client=None
    ),
    x="Tribunal",
    y="Total",
    color="Tribunal",
    text="Total"
)

figtb.update_traces(textposition='outside')
figtb.update_xaxes(tickangle=45)

st.plotly_chart(figtb)

# =======================================================================

st.subheader("Quantidade de Processos por Tipo")

figType = px.bar(
    escavador.totalTipo(dfEscavador),
    x="Tipo",
    y="Total",
    color="Tipo",
    text="Total"
)

figType.update_traces(textposition='outside')
figType.update_xaxes(tickangle=45)

st.plotly_chart(figType)

# =======================================================================
st.subheader("Quantidade de Processos Novos e Encerrados Por Mes e Ano atual")

qtdNewClose = dataJud.processNewAndCloset(dfDataJud)

figNewClose = px.line(
    qtdNewClose.melt(id_vars="mesAno", var_name="Status", value_name="Quantidade"),
    x="mesAno",
    y="Quantidade",
    color="Status",
    markers=True,
    labels={"Quantidade": "Quantidade de Processos", "mesAno": "Mês e Ano"},
    color_discrete_map={"Novos": "#0000ff", "Encerrados": "#008000"},
    text="Quantidade"
    
)

figNewClose.update_xaxes(tickangle=45)
figNewClose.update_traces(textposition='top center')

st.plotly_chart(figNewClose)

# =======================================================================
st.subheader("Quantidade de Processos por Cliente")

dfAtivo, dfPassivo = escavador.totalClient(
    dfEscavador, 
    processNumber = numberProcess, 
    client = client,
    clientHvk = dfClients["cpf_cnpj"].tolist()
)


st.dataframe(
    dfAtivo.sort_values(by="Total", ascending=False).head(10)
)

st.dataframe(
    dfPassivo.sort_values(by="Total", ascending=False).head(10)
)