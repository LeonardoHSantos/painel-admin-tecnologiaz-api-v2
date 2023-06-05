import json
import pandas as pd

from dateutil import tz
import datetime
from datetime import datetime

def convert_to_json(data):
    return json.loads(data)


def timesTemp_converter (timestamp):
    hora = datetime.strptime(datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))
    return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

class PrepareData:
    def create_message_websocket(name, msg, request_id):
        return dict(name=name, msg=msg, request_id=request_id)
    
    def convert_data_to_string(data):
        return json.dumps(data).replace("'", '"')
    
    def convert_data_to_json(data):
        return json.loads(data)

    def create_dataframe_request(list_requests):
        return pd.DataFrame(
            list(zip(
                list_requests[0], list_requests[1], list_requests[2], list_requests[3], list_requests[4], list_requests[5], list_requests[6], list_requests[7], list_requests[8], list_requests[9],
                list_requests[10], list_requests[11], list_requests[12], list_requests[13], list_requests[14], list_requests[15], list_requests[16], list_requests[17],
                list_requests[18], list_requests[19], list_requests[20], list_requests[21], # padrão 5
                list_requests[22], list_requests[23], list_requests[24], list_requests[25], # padrão 6
                list_requests[26], list_requests[27], list_requests[28], list_requests[29], # padrão 7
            )),
            columns=[
            "active_name", "active_id",
            "estrategia_1", "estrategia_1_sup_res_m15", "estrategia_1_sup_res_1h", "estrategia_1_sup_res_4h",
            "estrategia_2", "estrategia_2_sup_res_m15", "estrategia_2_sup_res_1h", "estrategia_2_sup_res_4h",
            "estrategia_3", "estrategia_3_sup_res_m15", "estrategia_3_sup_res_1h", "estrategia_3_sup_res_4h",
            "estrategia_4", "estrategia_4_sup_res_m15", "estrategia_4_sup_res_1h", "estrategia_4_sup_res_4h",
            "estrategia_5", "estrategia_5_sup_res_m15", "estrategia_5_sup_res_1h", "estrategia_5_sup_res_4h",
            "estrategia_6", "estrategia_6_sup_res_m15", "estrategia_6_sup_res_1h", "estrategia_6_sup_res_4h",
            "estrategia_7", "estrategia_7_sup_res_m15", "estrategia_7_sup_res_1h", "estrategia_7_sup_res_4h"
            ]
        )
    
    def create_list_requests_candles(list_estrategias, dataframe_actives_open, actives_database):
        list_requests = []
        list_actives_open = list(dataframe_actives_open["ticker"].values)
        print(" ************* LIST ACTIVES OPEN ************* ")
        print(list_actives_open)
        lista_timeframes = [60*5, 60*15, 60*60, 60*(60*4)]
        for idx_db in actives_database.index:
            active_name = actives_database["active_name"][idx_db]
            if active_name in list_actives_open:
                # for timeframe in lista_timeframes:
                for estrategia in list_estrategias:
                    
                    if int(actives_database[estrategia][idx_db]) >= 1:
                        # CHECAGEM DOS STATUS DA ESTRATEGIA - >= 1: ANALISAR | < 1: NÃO ANALISA
                        list_requests.append(
                            {
                                "estrategia": estrategia,
                                "active_name": actives_database["active_name"][idx_db],
                                "active_id": actives_database["active_id"][idx_db],
                                "timeframes": lista_timeframes,
                                "amounts_sup_res": [
                                    actives_database[estrategia][idx_db],
                                    actives_database[f"{estrategia}_sup_res_m15"][idx_db],
                                    actives_database[f"{estrategia}_sup_res_1h"][idx_db],
                                    actives_database[f"{estrategia}_sup_res_4h"][idx_db]
                                ],
                            }
                        )
        print(" *************************** LIST RQUESTS *************************** ")
        print(list_requests)
        for i in list_requests:
            print(i)
        return list_requests

    def create_list_requests_candles_check_results_operations(dataframe_actives_open, actives_database):
        list_requests = []
        list_actives_open = list(dataframe_actives_open["ticker"].values)
        list_actives_database = list(actives_database["active_name"].drop_duplicates(keep="last").values)
        print("\n\n ************* LIST ACTIVES OPEN | CHECK RESULTS OPERATIONS ************* ")
        print(list_actives_open)
        print("\n\n ************* LIST ACTIVES DATABSE | CHECK RESULTS OPERATIONS ************* ")
        print(list_actives_database)

        for idx in dataframe_actives_open.index:
            active_id   = dataframe_actives_open["id"][idx]
            active_name = dataframe_actives_open["ticker"][idx]
            if active_name in list_actives_database:
                # "amounts_sup_res": 2 --> para coletar apenas 2 candles com expirações atual e anterior para depara de resultados.
                list_requests.append(
                    {
                        "active_id": active_id,
                        "active_name": active_name,
                        "timeframes": 60*5,
                        "amounts_sup_res": 2
                    }
                )
        print(" *************************** LIST RQUESTS | CHECK RESULTS OPEN OPERATION *************************** ")
        print(list_requests)
        for i in list_requests:
            print(i)
        return list_requests

    def convert_data_to_dataframe_candles(message, request_id):
        # list_from = list(map(lambda x: timesTemp_converter(int(x)), dataframe["from"].values))
        request_id = request_id.split()
        print(f"request_id: {request_id}")
        dataframe = pd.DataFrame(message["msg"]["candles"])
        list_temp = [
            [], # 0 - ?
            [], # 1 - ?
            [], # 2 - ?
            [], # 3 - ?
            [], # 4 -  status candle --> if [0] != check-results
        ]
        if request_id[0] == "check-results":
            for idx in dataframe.index:
                list_temp[0].append(timesTemp_converter(timestamp=dataframe["from"][idx]))
                list_temp[1].append(request_id[2])
                list_temp[2].append(request_id[4])
                result = None
                if dataframe["close"][idx] > dataframe["open"][idx]:
                    result = "alta"
                elif dataframe["close"][idx] < dataframe["open"][idx]:
                    result = "baixa"
                else:
                    result = "sem mov."
                list_temp[3].append(result)

            # list_actives = list(map(lambda x: , dataframe["from"].values))
            dataframe["from"]           = list_temp[0]
            dataframe["active_name"]    = list_temp[1]
            dataframe["timeframe"]      = list_temp[2]
            dataframe["status_candle"]  = list_temp[3]
            # print(dataframe)
            return dataframe
        
        elif request_id[0] != "check-results":
            for idx in dataframe.index:
                list_temp[0].append(timesTemp_converter(timestamp=dataframe["from"][idx]))
                list_temp[1].append(request_id[0])
                list_temp[2].append(request_id[2])
                list_temp[3].append(request_id[4])
                result = None
                if dataframe["close"][idx] > dataframe["open"][idx]:
                    result = "alta"
                elif dataframe["close"][idx] < dataframe["open"][idx]:
                    result = "baixa"
                else:
                    result = "sem mov."
                list_temp[4].append(result)


            # list_actives = list(map(lambda x: , dataframe["from"].values))
            dataframe["from"]           = list_temp[0]
            dataframe["active_name"]    = list_temp[1]
            dataframe["estrategias"]     = list_temp[2]
            dataframe["timeframe"]      = list_temp[3]
            dataframe["status_candle"]  = list_temp[4]
            # print(dataframe)
            return dataframe