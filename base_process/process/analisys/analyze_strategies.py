import pandas as pd

from database.query_database import update_database_sign
from database.query_prod import check_sign_ranking
from database.query_prod import query_operations_resume_M5, update_ranking_M5

from base_process.process.expirations.expiration_candle import expiration_operation_M5

from database.conn import conn_db, conn_db_producao
from config_auth import TABLE_NAME_ESTRATEGIAS, TABLE_NAME_STATUS_API, TABLE_NAME_OPERATIONS

class AnalyzeData_Strategies:
    def process_sup_res(dataframe_candles, status_alert):
        list_estrategies = list(dataframe_candles["estrategias"].drop_duplicates(keep="last"))
        print(f"*********** list_estrategies: {list_estrategies}")

        dataframe_candles["from"] = pd.to_datetime(dataframe_candles["from"], format="%Y-%m-%d %H:%M:%S")
        print("\n\n\n\n\n *************************** DATAFRAME FROM INFO")
        print(dataframe_candles.info())
        
        
        try:
            list_estrategias    = list(dataframe_candles["estrategias"].drop_duplicates(keep="last"))
            list_active_name    = list(dataframe_candles["active_name"].drop_duplicates(keep="last"))
            list_timeframe      = list(dataframe_candles["timeframe"].drop_duplicates(keep="last"))
            print(f"list_estrategias: {list_estrategias}")
            print(f"list_active_name: {list_active_name}")
            print(f"list_timeframe: {list_timeframe}")

            for estrategia in list_estrategias:
                for active in list_active_name:

                    # Definição da base M5 para a estratégia e paridade atual do loop.
                    df_timeframe_5M = dataframe_candles[(dataframe_candles["estrategias"]==estrategia)&(dataframe_candles["active_name"]==active)&(dataframe_candles["timeframe"]=="5M")]
                    tt_candles_m5 = len(df_timeframe_5M["from"].values)
                    # print(f"TT CANDLES : {tt_candles_m5} | BASE:\n{df_timeframe_5M}")

                    # Verificação do status da paridade, checa se está ativo para essa estratégia. Ex: se o valor de tt_candles estiver >= 1 é ativo | se estiver 0 é inativo
                    if tt_candles_m5 >= 1:

                        # listas complementares de suporte e resistência
                        lista_tt_resume = list()
                        # ---
                        lista_tt_res_m15 = list()
                        lista_tt_res_1H = list()
                        lista_tt_res_4H = list()
                        # ---
                        lista_tt_sup_m15 = list()
                        lista_tt_sup_1H = list()
                        lista_tt_sup_4H = list()

                        # loop para percorrer os índices do DataFrame da estratégia e paridade atual.
                        for idx_m5 in df_timeframe_5M.index:
                            active_name         = df_timeframe_5M["active_name"][idx_m5]
                            m5_from             = df_timeframe_5M["from"][idx_m5]
                            m5_max              = df_timeframe_5M["max"][idx_m5]
                            m5_open             = df_timeframe_5M["open"][idx_m5]
                            m5_close            = df_timeframe_5M["close"][idx_m5]
                            m5_min              = df_timeframe_5M["min"][idx_m5]
                            m5_status_candle    = df_timeframe_5M["status_candle"][idx_m5]
                            m5_timeframe        = df_timeframe_5M["timeframe"][idx_m5]
                            # print(f"m5_timeframe: {m5_timeframe} | active_name: {active_name} | m5_from: {m5_from} | m5_max: {m5_max} | m5_open: {m5_open} | m5_close: {m5_close} | m5_min: {m5_min} | m5_status_candle: {m5_status_candle}")

                        

                            # Definição do DataFrame para análise de suporte e resistência, será ignorado o timeframe de M5.
                            temp_resumo_sup_res = list()
                            temp_tt_confluencias_timeframes = list()
                            for timeframe in list_timeframe:

                                if timeframe != "5M":
                                    df_timeframe_sup_res = dataframe_candles[
                                        (dataframe_candles["estrategias"]==estrategia)&
                                        (dataframe_candles["active_name"]==active)&
                                        (dataframe_candles["timeframe"]== timeframe)
                                    ]
                                    tt_candles_sup_res = len(df_timeframe_sup_res["from"].values)
                                    
                                    # Checagem de quantidade de candles do timeframe atual.
                                    if tt_candles_sup_res >= 1:

                                        # loop para percorrer os índices do DataFrame de suporte e resistência da estratégia -> paridade -> timeframe atual.
                                        for idx_sup_res in df_timeframe_sup_res.index:
                                            analise_from             = df_timeframe_sup_res["from"][idx_sup_res]
                                            analise_max              = df_timeframe_sup_res["max"][idx_sup_res]
                                            analise_open             = df_timeframe_sup_res["open"][idx_sup_res]
                                            analise_close            = df_timeframe_sup_res["close"][idx_sup_res]
                                            analise_min              = df_timeframe_sup_res["min"][idx_sup_res]
                                            analise_status_candle    = df_timeframe_sup_res["status_candle"][idx_sup_res]
                                            analise_timeframe        = df_timeframe_sup_res["timeframe"][idx_sup_res]

                                            status_process_sup_res = True
                                            min_M5 = int(m5_from.minute)
                                            min_SUP_RES = int(analise_from.minute)
                                            hora_M5 = int(m5_from.hour)
                                            hora_SUP_RES = int(analise_from.hour)

                                            # Valida se o candle de 5M está dentro do candle candle de M15 atual.
                                            # O intuito é evitar Falso Positivo em confluências de suporte/resistência.
                                            # Motivo: preços atuais próximos ao fechamento do candle anterior podem confluir facilmente e gerar sinais com baixa assertividade.
                                            if analise_timeframe == "15M" and min_M5 <= (min_SUP_RES + 15) and hora_M5 <= hora_SUP_RES:
                                                status_process_sup_res = False
                                            elif analise_timeframe == "1H" and min_M5 <= 10 and hora_M5 == hora_SUP_RES:
                                                status_process_sup_res = False
                                            elif analise_timeframe == "4H" and min_M5 <= 10 and hora_M5 == hora_SUP_RES:
                                                status_process_sup_res = False
                                            
                                            # print(f"""\n\n\n
                                            # ********************************
                                            #     5M: {m5_from.minute} | TM: {analise_timeframe} --> MINUTO: {analise_from.minute}
                                            #     min_M5: {min_M5}
                                            #     min_SUP_RES: {min_SUP_RES}
                                            #     ----------------------------
                                            #     min_M5: {hora_M5}
                                            #     min_SUP_RES: {hora_SUP_RES}
                                            # ********************************""")
                                            if status_process_sup_res == True:
                                                # Verificação de candles de M5 com fechamento em alta.
                                                if m5_status_candle == "alta":
                                                    if m5_max >= analise_max and m5_close < analise_max:
                                                        temp_resumo_sup_res.append(f"1 - RES {analise_timeframe} | analise_from: {analise_from} | TM: {analise_timeframe}")
                                                        temp_tt_confluencias_timeframes.append(f"RES - {analise_timeframe}")
                                                    
                                                # Verificação de candles de M5 com fechamento em baixa.
                                                elif m5_status_candle == "baixa":
                                                    if m5_min <= analise_min and m5_close > analise_min:
                                                        temp_resumo_sup_res.append(f"2 - SUP {analise_timeframe} | analise_from: {analise_from} | TM: {analise_timeframe}")
                                                        temp_tt_confluencias_timeframes.append(f"SUP - {analise_timeframe}")

                            # atualização das listas finais
                            tt_res_15m = temp_tt_confluencias_timeframes.count("RES - 15M")
                            tt_res_1H = temp_tt_confluencias_timeframes.count("RES - 1H")
                            tt_res_4H = temp_tt_confluencias_timeframes.count("RES - 4H")
                            # ---
                            tt_sup_15m = temp_tt_confluencias_timeframes.count("SUP - 15M")
                            tt_sup_1H = temp_tt_confluencias_timeframes.count("SUP - 1H")
                            tt_sup_4H = temp_tt_confluencias_timeframes.count("SUP - 4H")
                            # ---
                            lista_tt_res_m15.append(tt_res_15m)
                            lista_tt_res_1H.append(tt_res_1H)
                            lista_tt_res_4H.append(tt_res_4H)
                            lista_tt_sup_m15.append(tt_sup_15m)
                            lista_tt_sup_1H.append(tt_sup_1H)
                            lista_tt_sup_4H.append(tt_sup_4H)
                            lista_tt_resume.append(temp_resumo_sup_res)

                        print(" *** RESULTADO FINAL DA ANÁLISE DE SUPORTE E RESISTÊNCIA *** ")
                        print(f"lista_tt_res_m15: {lista_tt_res_m15}")
                        print(f"lista_tt_res_1H: {lista_tt_res_1H}")
                        print(f"lista_tt_res_4H: {lista_tt_res_4H}")
                        print(f"lista_tt_sup_m15: {lista_tt_sup_m15}")
                        print(f"lista_tt_sup_1H: {lista_tt_sup_1H}")
                        print(f"lista_tt_sup_4H: {lista_tt_sup_4H}")
                        print(f"lista_tt_resume: {lista_tt_resume}")

                        # atualização do timeframe 5M atual
                        df_timeframe_5M["res_15m_extrato_tm"]   = lista_tt_res_m15
                        df_timeframe_5M["res_1h_extrato_tm"]    = lista_tt_res_1H
                        df_timeframe_5M["res_4h_extrato_tm"]    = lista_tt_res_4H
                        df_timeframe_5M["sup_15m_extrato_tm"]   = lista_tt_sup_m15
                        df_timeframe_5M["sup_1h_extrato_tm"]    = lista_tt_sup_1H
                        df_timeframe_5M["sup_4h_extrato_tm"]    = lista_tt_sup_4H
                        df_timeframe_5M["resume"]               = lista_tt_resume

                        if estrategia == "estrategia_1":
                            try:
                                query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_1")
                                update_ranking_M5(obj_results=query_resume[1])
                            except Exception as e:
                                print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                            estrategia_1(estrategia=estrategia, dataframe=df_timeframe_5M, padrao="PADRAO-M5-V1", version="M5-V1", active=active, status_alert=status_alert)
                        # ----------------------
                        elif estrategia == "estrategia_2":
                            try:
                                query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_2")
                                update_ranking_M5(obj_results=query_resume[1])
                            except Exception as e:
                                print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                            estrategia_2(estrategia=estrategia, dataframe=df_timeframe_5M, padrao="PADRAO-M5-V2", version="M5-V2", active=active, status_alert=status_alert)
                        # ----------------------
                        elif estrategia == "estrategia_3":
                            try:
                                query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_3")
                                update_ranking_M5(obj_results=query_resume[1])
                            except Exception as e:
                                print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                            estrategia_3(estrategia=estrategia, dataframe=df_timeframe_5M, padrao="PADRAO-M5-V3", version="M5-V3", active=active, status_alert=status_alert)
                        # ----------------------
                        elif estrategia == "estrategia_4":
                            try:
                                query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_4")
                                update_ranking_M5(obj_results=query_resume[1])
                            except Exception as e:
                                print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                            estrategia_4(estrategia=estrategia, dataframe=df_timeframe_5M, padrao="PADRAO-M5-V4", version="M5-V4", active=active, status_alert=status_alert)
                        # ----------------------
                        elif estrategia == "estrategia_5":
                            try:
                                query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_5")
                                update_ranking_M5(obj_results=query_resume[1])
                            except Exception as e:
                                print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                            estrategia_5(estrategia=estrategia, dataframe=df_timeframe_5M, padrao="PADRAO-M5-V5", version="M5-V5", active=active, status_alert=status_alert)
                        # ----------------------
                        elif estrategia == "estrategia_6":
                            try:
                                query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_6")
                                update_ranking_M5(obj_results=query_resume[1])
                            except Exception as e:
                                print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                            estrategia_6(estrategia=estrategia, dataframe=df_timeframe_5M, padrao="PADRAO-M5-V6", version="M5-V6", active=active, status_alert=status_alert)
                        # ----------------------
                        elif estrategia == "estrategia_7":
                            try:
                                query_resume = query_operations_resume_M5(active_name=active, estrategia="estrategia_7")
                                update_ranking_M5(obj_results=query_resume[1])
                            except Exception as e:
                                print(f"#### ERRRO PROCESS UPDATE RANK | ERROR: {e} ### ")
                            estrategia_7(estrategia=estrategia, dataframe=df_timeframe_5M, padrao="PADRAO-M5-V7", version="M5-V7", active=active, status_alert=status_alert)
        except Exception as e:
            print(f"ERROR DF: {e}")




def prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h):
    


    dataframe["from"] = dataframe["from"].dt.strftime('%Y-%m-%d %H:%M:%S')
    max_idx = max(list(dataframe.index))
    expiration = expiration_operation_M5(dataframe["from"][max_idx])
    mercado = "-"
    if "OTC" in active:
        mercado = "otc"
    else:
        mercado = "aberto"

    list_tests = ["M5-V6", "M5-V7"] # "M5-V5"
    if version in list_tests:
        status_alert = f"{status_alert}-test"

    if version == "M5-V2":
        try:
            conn = conn_db_producao()
            cursor = None
            if conn["status_conn_db"] == True:
                cursor = conn["conn"].cursor()
                name_strategy = f"{active}-{version}",
                comando_query = f'''
                SELECT
                    id, direction, status_alert
                FROM {TABLE_NAME_OPERATIONS}
                WHERE
                    name_strategy = "{name_strategy}" and expiration_alert = "{expiration["expiration_alert"]}"
                '''
                cursor.execute(comando_query)
                result_query    = cursor.fetchall()
                tt_query = len(result_query)
                print(f"\n\n ### RESULTS CHECK M5-V2 | RESULTS: {result_query}\n\n")
                if tt_query >= 1:
                    direction = result_query[0][1]
                cursor.close()
                conn["conn"].close()
        except Exception as e:
            print(f"\n\n ### ERROR CHECK M5-V2 | ERROR: {e} ### ")
            try:
                cursor.close()
                conn["conn"].close()
            except Exception as e:
                print(f"\n\n ### CHECK M5-V2 | ERRO AO ENCERRAR DB | ERROR: {e} ### ")

    

    obj_to_database = {
        "open_time": expiration["open_time"],
        "alert_datetime": expiration["alert_datetime"],
        "expiration_alert": expiration["expiration_alert"],
        "expiration_alert_timestamp": expiration["expiration_alert_timestamp"],
        "alert_time_update": expiration["alert_time_update"],
        "resultado": expiration["resultado"],
        "status_alert": status_alert,
        "padrao": padrao,
        "version": version,
        "name_strategy": f"{active}-{version}",
        "direction": direction,
        "active": active,
        "mercado": mercado,
        "observation": observation,
        "result_confluencias": result_confluencias,
        "sup_m15": sup_m15,
        "sup_1h": sup_1h,
        "sup_4h": sup_4h,
        "res_m15": res_m15,
        "res_1h": res_1h,
        "res_4h": res_4h,
    }
    if direction == "call" or direction == "put":
        update_database_sign(obj_sign=obj_to_database)
        check_sign_ranking(expiration=expiration["expiration_alert"])
    if result_confluencias == True:
        print(f"\n ------------------------------ Enviar sinal ao banco de dados: SIM | RESULT-CONFLUÊNCIAS: {result_confluencias} ------------------------------ ")
    else:
        print(f"\n ------------------------------ Enviar sinal ao banco de dados: NÃO | RESULT-CONFLUÊNCIAS: {result_confluencias} ------------------------------ ")
    print(f"SIGNAL TO DATABASE ------------------->>>>> {obj_to_database}\n\n")


# ----------------------------------------------------------------------
def estrategia_1(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]]) #, "res_15m_extrato_tm", "sup_15m_extrato_tm", "res_1h_extrato_tm", "sup_1h_extrato_tm", "res_4h_extrato_tm", "sup_4h_extrato_tm"]])
    
    result_confluencias = False
    current_id = max(list_idx)
    id_5 = current_id -4
    id_4 = current_id -3
    id_3 = current_id -2
    id_2 = current_id -1
    id_1 = current_id
    
    direction = "-"
    observation = "-"

  
    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h   = dataframe["res_1h_extrato_tm"][id_1]
    res_4h   = dataframe["res_4h_extrato_tm"][id_1]
    # if dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
    if dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
        if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_1h_extrato_tm"][id_1] >= 1 or  dataframe["sup_4h_extrato_tm"][id_1] >= 1:
            direction = "call"
            result_confluencias = True
        else:
            observation = "call - sem conf. sup res"
    
    # elif dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
    elif dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
        if dataframe["res_15m_extrato_tm"][id_1] == 0 and dataframe["res_1h_extrato_tm"][id_1] == 1 and dataframe["res_4h_extrato_tm"][id_1] == 0:
            observation = "#1 put - sem conf. sup res"
        # ----
        elif dataframe["res_15m_extrato_tm"][id_1] == 1 and dataframe["res_1h_extrato_tm"][id_1] == 1:
            observation = "#2 put - sem conf. sup res"
        # ----
        elif dataframe["res_15m_extrato_tm"][id_1] >= 3 or dataframe["res_1h_extrato_tm"][id_1] >= 1 or  dataframe["res_4h_extrato_tm"][id_1] >= 1:
            direction = "put"
            result_confluencias = True
                
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)

# -----------------------------------------------------------------------
def estrategia_2(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    result_confluencias = False
    direction = "-"
    observation = "-"
    current_id = max(list_idx)
    id_7 = current_id -6
    id_6 = current_id -5
    id_5 = current_id -4
    id_4 = current_id -3
    id_3 = current_id -2
    id_2 = current_id -1
    id_1 = current_id -0

    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h  = dataframe["res_1h_extrato_tm"][id_1]
    res_4h  = dataframe["res_4h_extrato_tm"][id_1]


    if dataframe["status_candle"][id_7] == "baixa" and dataframe["status_candle"][id_6] == "alta" and dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "baixa":
        if dataframe["sup_15m_extrato_tm"][id_1] == 1 or dataframe["sup_1h_extrato_tm"][id_1] == 1 or  dataframe["sup_4h_extrato_tm"][id_1] == 1:
            direction = "call"
            result_confluencias = True
        else:
            observation = "call - sem conf. sup res"

    elif dataframe["status_candle"][id_7] == "alta" and dataframe["status_candle"][id_6] == "baixa" and dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "alta":
        if dataframe["res_1h_extrato_tm"][id_1] >= 1:
            observation = "put - sem conf. sup res"
        elif dataframe["res_15m_extrato_tm"][id_1] >= 1 or dataframe["res_1h_extrato_tm"][id_1] >= 1:
            observation = "put - sem conf. sup res"
        elif dataframe["res_15m_extrato_tm"][id_1] == 1 or dataframe["res_1h_extrato_tm"][id_1] == 0 and dataframe["res_4h_extrato_tm"][id_1] >= 1:
            direction = "put"
            result_confluencias = True
        else:
            observation = "put - sem conf. sup res"
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)

# ----------------------------------------------------------------------
def estrategia_3(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    confluencia_1 = "no"
    confluencia_2 = "no"
    confluencia_3 = "no"
    result_confluencias = False
    observation = "-"
    direction = "-"
    observation_2 = "#"
    sup_m15 = None
    sup_1h = None
    sup_4h = None
    res_m15 = None
    res_1h = None
    res_4h = None
    for current_id in dataframe.index:
        if current_id == 2:
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0
            if dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
                confluencia_1 = "yes"

            elif dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
                confluencia_1 = "yes"
        # ----------------------------
        elif current_id == 5:
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0
            if dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
                confluencia_2 = "yes"

            elif dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
                confluencia_2 = "yes"
        # ----------------------------
        elif current_id == 8:
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0
            if dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
                confluencia_3 = "yes"

            elif dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
                confluencia_3 = "yes"
        # ----------------------------
        elif current_id == 11:
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0
            sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
            sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
            sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
            res_m15  = dataframe["res_15m_extrato_tm"][id_1]
            res_1h  = dataframe["res_1h_extrato_tm"][id_1]
            res_4h  = dataframe["res_4h_extrato_tm"][id_1]
            if dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
                if dataframe["res_15m_extrato_tm"][id_1] >= 2 or dataframe["res_1h_extrato_tm"][id_1] >= 1 or  dataframe["res_4h_extrato_tm"][id_1] >= 1:
                    direction = "put"
                else:
                    observation_2 = "put - sem conf. sup res"

            elif dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
                if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_1h_extrato_tm"][id_1] >= 1 or  dataframe["sup_4h_extrato_tm"][id_1] >= 1:
                    direction = "call"
                else:
                    observation_2 = "call - sem conf. sup res"
    
    observation = f"Q1: {confluencia_1} - Q2: {confluencia_2} - Q3: {confluencia_3} - {observation_2}"
    if confluencia_1 == "no" and confluencia_2 == "no" and confluencia_3 == "no":
        if direction == "put" or direction == "call":
            result_confluencias = True
    else:
        if "call" in direction:
            direction = "operation-canceled-call"
        elif "put" in direction:
            direction = "operation-canceled-put"
        else:
            direction = "-"
    
    print(f"\n\n -----> CONFLUÊNCIAS {active} | RESULTADO: {result_confluencias} | OBS: {observation}")
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)

# ----------------------------------------------------------------------
def estrategia_4(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    result_confluencias = False
    current_id = max(list_idx)
    id_7 = current_id -6
    id_6 = current_id -5
    id_5 = current_id -4
    # id_4 = current_id -3
    id_3 = current_id -2
    # id_2 = current_id -1
    id_1 = current_id -0
    
    direction = "-"
    observation = "-"
    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    # ---
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h  = dataframe["res_1h_extrato_tm"][id_1]
    res_4h  = dataframe["res_4h_extrato_tm"][id_1]

    if dataframe["status_candle"][id_7] == "baixa" and dataframe["status_candle"][id_6] == "alta" and dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_3] == "baixa":
        if dataframe["res_15m_extrato_tm"][id_1] >= 2 or dataframe["res_1h_extrato_tm"][id_1] >= 1 == dataframe["res_4h_extrato_tm"][id_1] >= 1:
            direction = "put"
            result_confluencias = True
        else:
            observation = "put - sem conf. sup res"

    elif dataframe["status_candle"][id_7] == "alta" and dataframe["status_candle"][id_6] == "baixa" and dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_3] == "alta":
        if dataframe["sup_1h_extrato_tm"][id_1] == 0:
            if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_4h_extrato_tm"][id_1] >= 1:
                direction = "call"
                result_confluencias = True
            else:
                observation = "#1 call - sem conf. sup res"
        else:
            observation = "#2 call - sem conf. sup res"
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)

# ----------------------------------------------------------------------
def estrategia_5(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    result_confluencias = False
    current_id = max(list_idx)
    
    id_4 = current_id -3
    id_3 = current_id -2
    id_2 = current_id -1
    id_1 = current_id -0
    
    direction = "-"
    observation = "-"
    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    # ---
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h  = dataframe["res_1h_extrato_tm"][id_1]
    res_4h  = dataframe["res_4h_extrato_tm"][id_1]

    if dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "alta":
        if dataframe["res_15m_extrato_tm"][id_1] >= 2 or dataframe["res_1h_extrato_tm"][id_1] >= 1 == dataframe["res_4h_extrato_tm"][id_1] >= 1:
            direction = "put"
            result_confluencias = True
        else:
            observation = "put - sem conf. sup res"

    elif dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "baixa":
        if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_1h_extrato_tm"][id_1] >= 1 == dataframe["sup_4h_extrato_tm"][id_1] >= 1:
            direction = "call"
            result_confluencias = True
        else:
            observation = "1 call - sem conf. sup res"
        
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)

# ----------------------------------------------------------------------
def estrategia_6(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    result_confluencias = False
    current_id = max(list_idx)
    
    id_4 = current_id -3
    id_3 = current_id -2
    id_2 = current_id -1
    id_1 = current_id -0
    
    direction = "-"
    observation = "-"
    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    # ---
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h  = dataframe["res_1h_extrato_tm"][id_1]
    res_4h  = dataframe["res_4h_extrato_tm"][id_1]

    if dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_3] == "alta" and dataframe["status_candle"][id_2] == "baixa" and dataframe["status_candle"][id_1] == "alta":
        if dataframe["res_15m_extrato_tm"][id_1] >= 2 or dataframe["res_1h_extrato_tm"][id_1] >= 1 == dataframe["res_4h_extrato_tm"][id_1] >= 1:
            direction = "put"
            result_confluencias = True
        else:
            observation = "put - sem conf. sup res"

    elif dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_3] == "baixa" and dataframe["status_candle"][id_2] == "alta" and dataframe["status_candle"][id_1] == "baixa":
        if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_1h_extrato_tm"][id_1] >= 1 == dataframe["sup_4h_extrato_tm"][id_1] >= 1:
            direction = "call"
            result_confluencias = True
        else:
            observation = "1 call - sem conf. sup res"
        
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)
    
# ----------------------------------------------------------------------
def estrategia_7(estrategia, dataframe, status_alert, padrao, version, active):
    list_idx = list(range(0, len(dataframe.index)))
    dataframe.index = list_idx
    print(f"-------------------------------------------------------> estratégia: {estrategia}")
    print(dataframe[["from", "active_name", "status_candle"]])
    
    result_confluencias = False
    current_id = max(list_idx)
    
    
    id_6 = current_id -5
    id_5 = current_id -4
    id_4 = current_id -3
    id_3 = current_id -2
    id_2 = current_id -1
    id_1 = current_id -0
    
    direction = "-"
    observation = "-"
    sup_m15  = dataframe["sup_15m_extrato_tm"][id_1]
    sup_1h   = dataframe["sup_1h_extrato_tm"][id_1]
    sup_4h   = dataframe["sup_4h_extrato_tm"][id_1]
    # ---
    res_m15  = dataframe["res_15m_extrato_tm"][id_1]
    res_1h  = dataframe["res_1h_extrato_tm"][id_1]
    res_4h  = dataframe["res_4h_extrato_tm"][id_1]

    if dataframe["status_candle"][id_6] == "baixa" and dataframe["status_candle"][id_5] == "baixa" and dataframe["status_candle"][id_4] == "alta" and dataframe["status_candle"][id_1] == "baixa":
        if dataframe["status_candle"][id_3] == "alta" or dataframe["status_candle"][id_2] == "alta":
            if dataframe["res_15m_extrato_tm"][id_1] >= 2 or dataframe["res_1h_extrato_tm"][id_1] >= 1 == dataframe["res_4h_extrato_tm"][id_1] >= 1:
                direction = "put"
                result_confluencias = True
            else:
                observation = "#1 -put - sem conf. sup res"
        else:
            observation = "#2 -put - sem conf. sup res"

    if dataframe["status_candle"][id_6] == "alta" and dataframe["status_candle"][id_5] == "alta" and dataframe["status_candle"][id_4] == "baixa" and dataframe["status_candle"][id_1] == "alta":
        if dataframe["status_candle"][id_3] == "baixa" or dataframe["status_candle"][id_2] == "baixa":
            if dataframe["sup_15m_extrato_tm"][id_1] >= 2 or dataframe["sup_1h_extrato_tm"][id_1] >= 1 == dataframe["sup_4h_extrato_tm"][id_1] >= 1:
                direction = "call"
                result_confluencias = True
            else:
                observation = "#1 -call - sem conf. sup res"
        else:
            observation = "#2 -call - sem conf. sup res"
        
    
    prepare_signal_to_database(dataframe, direction, status_alert, padrao, version, active, observation, result_confluencias,
                               sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h)
