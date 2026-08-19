
#função pra normalizar parametros, se não passar informação de parametro de consulta pelo usuario
#aplicamos um parametro de consulta default. E como cidade não tem parametro default precisamos criar dois
#formatos de parametro, um com a cidade (caso o usuario passe) e o outro sem a cidade.
def normalize_path_params(cidade=None,
                          estrelas_min = 0,
                          estrelas_max = 5,
                          diaria_min = 0,
                          diaria_max = 10000,
                          limit = 50,
                          offset = 0, 
                          **dados): #recebe **dados desenpacotados pois os valores defaults da função são substituíveis por qualquer valor passado de dados.
    if cidade: #se tiver cidade retorna o dicionario com filtro de consulta adequado para a cidade
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset}
    # se não entrou no if retorna o dicionario sem a especificação da cidade:
    return {
        'estrelas_min': estrelas_min,
        'estrelas_max': estrelas_max,
        'diaria_min': diaria_min,
        'diaria_max': diaria_max,
        'limit': limit,
        'offset': offset}

consulta_sem_cidade = "SELECT * FROM hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?)\
            LIMIT ? OFFSET ?"

consulta_com_cidade = "SELECT * FROM hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?)\
            and cidade = ? LIMIT ? OFFSET ?"