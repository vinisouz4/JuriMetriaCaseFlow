# Dicionário de mapeamento
tribunal_map = {
    'TRT-1': "1",
    'TRT-2': "2",
    'TRT-3': "3",
    'TRT-4': "4",
    'TRT-5': "5",
    'TRT-6': "6",
    'TRT-7': "7",
    'TRT-8': "8",
    'TRT-9': "9",
    'TRT-10': "10",
    'TRT-11': "11",
    'TRT-12': "12",
    'TRT-13': "13",
    'TRT-14': "14",
    'TRT-15': "15",
    'TRT-16': "16",
    'TRT-17': "17",
    'TRT-18': "18",
    'TRT-19': "19",
    'TRT-20': "20",
    'TRT-21': "21",
    'TRT-22': "22",
    'TRT-23': "23",
    'TRT-24': "24"
}

# Função para obter o número do tribunal
def getTribunalNumber(tribunal):
    return tribunal_map.get(tribunal, None)