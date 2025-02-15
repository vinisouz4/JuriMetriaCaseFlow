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

insights = Insights(PandasDataFrame())
dataCaseFlow = ReadCaseFlowData(PandasDataFrame())
dataJud = ReadDataJud(PandasDataFrame())
util = Utils()

st.title("Jurimetria")

# =============================================================================

dataCase = dataCaseFlow.getData("Case", "true")

df = dataJud.readDataJud()

groupedJud = dataJud.statusGrouped(df)

# =============================================================================

with st.sidebar:
    st.title("Filtros")

    filterNumberDays = st.number_input("Numero de Dias", min_value=7, max_value=100000)

    numberProcess = st.text_input("Numero do Processos", placeholder="Digite o numero de processos sem pontos e traços")

    month = st.selectbox("Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])

# =============================================================================

thirtyDaysProcess, sevenDaysProcess = insights.distributionData(dataCase, "distribution_date")


# =============================================================================

# Metricas

totaProcesso, processoPeriodos = st.columns(2)

totaProcesso.metric("Total de processos", insights.totalProcess(dataCase))
processoPeriodos.metric("Distribuídos Últimos 30 dias", thirtyDaysProcess, help=f"Processos distribuídos nos últimos 30 dias, considerando a data de distribuição")
# st.metric("Valor total das causas", f"R$ {insights.totalValueCause(dataCase):.2f}")

# =============================================================================

# Movimentos de Decisão e Conclusão

st.subheader("Andamentos Processuais")

peticao, distribuicao, conclusao, meroExpedientePublicao = st.columns(4)

peticao.metric(
    f"Petição - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Petição", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que estão no status de Petição nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)

distribuicao.metric(
    f"Distribuição - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Distribuição", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram distruibuidos nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)

conclusao.metric(
    f"Conclusão - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Conclusão", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram Conclusão nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)

meroExpedientePublicao.metric(
    f"Mero Expediente e publicação - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Mero Expediente e publicação", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram Mero Expediente e publicação nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)


# Movimentos de Tramitação e Baixa

st.subheader("Audiências ou Conclusos para Julgamento")

dependerJulgamento, instrucao, retiradaPauta = st.columns(3)

dependerJulgamento.metric(
    f"A depender do julgamento - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "A depender do julgamento", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram A depender do julgamento nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)

instrucao.metric(
    f"de Instrução - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "de Instrução", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram de Instrução nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)

retiradaPauta.metric(
    f"Retirada de pauta - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Retirada de pauta", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram Retirada de pauta nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)

# Movimentos de Adiantamento ou Obstaculos

st.subheader("Arquivados ou Julgados")

decisaoJudicial, baixaDefinitiva, definitivo, acolhimentoEmbargosDeclarao = st.columns(4)

decisaoJudicial.metric(
    f"Por decisão judicial - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Por decisão judicial", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram Por decisão judicial nos últimos {filterNumberDays} dias, considerando a data de ajuizamento"
)

baixaDefinitiva.metric(
    f"Baixa Definitiva - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Baixa Definitiva", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram Baixa Definitiva nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)

definitivo.metric(
    f"Definitivo - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Definitivo", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram Definitivo nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)

acolhimentoEmbargosDeclarao.metric(
    f"Não acolhimento de embargos de declaração - {filterNumberDays} Dias", 
    dataJud.statusCount(
        df, 
        "Não acolhimento de embargos de declaração", 
        "dataUltimoMovimento", 
        filterNumberDays
    ), 
    help=f"Processos que foram Não acolhimento de embargos de declaração nos últimos {filterNumberDays} dias, considerando a data da ultima movimentação"
)



# =============================================================================

st.dataframe(groupedJud)

allMoviments = dataJud.getAllMoviments().explode(["movimentos", "dataMovimentacao"])

st.dataframe(dataJud.meanDateProcess(allMoviments, numberProcess))

st.dataframe(insights.newProcessMonth(dataCase, month=util.getNumberMonth(month)))