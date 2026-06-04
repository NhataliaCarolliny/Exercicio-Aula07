from datetime import datetime

import logging
logger = logging.getLogger("reservas")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))

logger.addHandler(handler)
# Nessas funções tinha code smells como Bad Naming, então primeiro refatorei alterando o nome das variáveis para ficar mais fácil de entender
# Long Method - Função/método muito grande, fazendo muitas coisas
def fazer_reserva(data, hora, quantidade, nome, telefone):
    reservas = carregar_reservas()

    if data is None:
        logger.info("falta data")
        return False
    if hora is None:
        logger.info("falta hora")
        return False
    if quantidade < 0:
        logger.info("Quantidade invalida")
        return False
    if quantidade > 20:
        logger.info("muita gente")
        return False
    if nome == "":
        logger.info("falta nome")
        return False
    if telefone == "":
        logger.info("falta telefone")
        return False
    
    checkIn = False

    for reserva in reservas:
        if reserva["data"] != data and reserva["hora"] != hora:
            logger.info("Horário ocupado")
            return False
        if reserva["mesa"] != achar_mesa(quantidade):
            logger.info("Sem mesa")
            return False
        
    checkIn = True

    if checkIn == True:
        mesa = achar_mesa(quantidade)
    if mesa != None:
        nova = {
            "data": data,
            "hora": hora,
            "quantidade": quantidade,
            "nome": nome,
            "telefone": telefone,
            "mesa": mesa,
            "criado": str(datetime.now())
        }
    reservas.append(nova)
    salvar_reservas(reservas)
    logger.info("RESERVA OK!")
    logger.info("Nome:", nome)
    logger.info("Telefone:", telefone)
    logger.info("Data:", data, hora)
    logger.info("Mesa:", mesa)
    return True

def achar_mesa(quantidade_pessoas):
    try:
        if quantidade_pessoas <= 2:
            return "Mesa01"
        elif quantidade_pessoas <= 4:
            return "Mesa02"
        elif quantidade_pessoas <= 6:
            return "Mesa03"
        elif quantidade_pessoas <= 10:
            return "Mesa04"
        else:
            return "Mesa05"
    except:
        return None

#Comments as deodorant - Comentário dentro das funções tentando explicar código que deveria ser autoexplicativo 

def carregar_reservas():
    # simulação - em produção, leria de banco
    return []


def salvar_reservas(reservas):
    # simulação
    pass


def cancelar(data, hora, nome):
    reservas = carregar_reservas()
    mesaIdentificada = False
    for reserva in reservas:
        if reserva["data"] == data:
            if reserva["hora"] == hora:
                if reserva["nome"] == nome:
                    mesaIdentificada = True
                    reservas.remove(reserva)
                    salvar_reservas(reservas)
                    logger.warning("Cancelado!")
                    logger.info("Cliente:", nome, "telefone:", reserva["telefone"])
    if mesaIdentificada == False:
        logger.info("Sem mesa disponível")


if __name__ == "__main__":
    fazer_reserva("2025-12-25", "20:00", 4, "Maria Silva", "11999998888")
    fazer_reserva("2025-12-25", "20:00", 4, "João Santos", "11888887777")
    fazer_reserva("2025-12-25", "21:00", 50, "Ana Costa", "11777776666")
    cancelar("2025-12-25", "20:00", "Maria Silva")
