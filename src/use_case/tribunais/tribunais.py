# Dicionário de mapeamento
tribunal_map = {
    'Diário Eletrônico da Justiça do Trabalho (TRT-2)': "2",
    'Tribunal Regional do Trabalho da 2ª Região': "2",
    'Tribunal Regional do Trabalho da 15ª Região': "15",
    'Tribunal Regional do Trabalho da 2ª Região (TRT2) - SP': "2",
    'Tribunal Regional do Trabalho da 15ª Região (TRT15) - SP': "15"
}

# Função para obter o número do tribunal
def getTribunalNumber(tribunal):
    return tribunal_map.get(tribunal, None)