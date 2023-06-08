from database.conn import conn_db, conn_db_producao
from base_process.process.prepare_data.prepareData import PrepareData
from base_process.process.expirations.expiration_candle import datetime_now, convert_datetime_to_string
from config_auth import TABLE_NAME_ESTRATEGIAS, TABLE_NAME_STATUS_API, TABLE_NAME_OPERATIONS

# -----------------------------------------
def query_database_actives_all():
    try:
        conn = conn_db_producao()
        cursor = None
        list_actives = []
        list_padroes = []
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
                SELECT active_name from {TABLE_NAME_ESTRATEGIAS}
                '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            tt_query = len(result_query)
            if tt_query >= 1:
                for result in result_query:
                    _active_name = result[0]
                    list_actives.append(_active_name)
                    
        
        cursor.close()
        conn["conn"].close()
        print(" DB - DESCONECTADO ")
        return sorted(list_actives)
    except Exception as e:
        print(f"ERROR QUERY 2 | ERROR: {e}")
# -----------------------------------------
def query_database_estrategia(estrategia, active_name):
    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
                SELECT * from {TABLE_NAME_ESTRATEGIAS} WHERE active_name = "{active_name}"
                '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            print("\n\n----------------------- result query ")
            print(result_query)
            print("-----------------------")
            tt_query = len(result_query)
            print(tt_query)
            if tt_query >=1:
                _active_name = result_query[0][1]
                check_estrategia = None
                value_estrategia_candles = None
                sup_res_m15 = None
                sup_res_1h = None
                sup_res_4h = None
                estrategia_1 = result_query[0][3]
                estrategia_2 = result_query[0][7]
                estrategia_3 = result_query[0][11]
                estrategia_4 = result_query[0][15]
                estrategia_5 = result_query[0][19]
                estrategia_6 = result_query[0][23]
                estrategia_7 = result_query[0][27]
                
                if estrategia == "estrategia_1":
                    check_estrategia = estrategia_1
                    sup_res_m15 = result_query[0][4]
                    sup_res_1h = result_query[0][5]
                    sup_res_4h = result_query[0][6]
                # ---
                elif estrategia == "estrategia_2":
                    check_estrategia = estrategia_2
                    sup_res_m15 = result_query[0][8]
                    sup_res_1h = result_query[0][9]
                    sup_res_4h = result_query[0][10]
                # ---
                elif estrategia == "estrategia_3":
                    check_estrategia = estrategia_3
                    sup_res_m15 = result_query[0][12]
                    sup_res_1h = result_query[0][13]
                    sup_res_4h = result_query[0][14]
                # ---
                elif estrategia == "estrategia_4":
                    check_estrategia = estrategia_4
                    sup_res_m15 = result_query[0][16]
                    sup_res_1h = result_query[0][17]
                    sup_res_4h = result_query[0][18]
                # ---
                elif estrategia == "estrategia_5":
                    check_estrategia = estrategia_5
                    sup_res_m15 = result_query[0][20]
                    sup_res_1h = result_query[0][21]
                    sup_res_4h = result_query[0][22]
                # ---
                elif estrategia == "estrategia_6":
                    check_estrategia = estrategia_6
                    sup_res_m15 = result_query[0][24]
                    sup_res_1h = result_query[0][25]
                    sup_res_4h = result_query[0][26]
                # ---
                elif estrategia == "estrategia_7":
                    check_estrategia = estrategia_6
                    sup_res_m15 = result_query[0][28]
                    sup_res_1h = result_query[0][29]
                    sup_res_4h = result_query[0][30]
                
                data = {
                    "status_query": True,
                    "active_estrategia": estrategia,
                    "active_query": active_name,
                    "check_estrategia": check_estrategia,
                    "active_name":  _active_name,
                    "sup_res_m15":  sup_res_m15,
                    "sup_res_1h":   sup_res_1h,
                    "sup_res_4h":   sup_res_4h,
                    "estrategia_1": estrategia_1,
                    "estrategia_2": estrategia_2,
                    "estrategia_3": estrategia_3,
                    "estrategia_4": estrategia_4,
                    "estrategia_5": estrategia_5,
                    "estrategia_6": estrategia_6,
                    "estrategia_7": estrategia_7,
                }
                try:
                    cursor.close()
                    conn["conn"].close()
                    print(" DB - DESCONECTADO ")
                except Exception as e:
                    print(f"ERROR QUERY 1 | ERROR: {e}")
                return data
            else:
                return {"status_query": False}

    except Exception as e:
        print(f"ERROR QUERY 2 | ERROR: {e}")
# -----------------------------------------
def update_database_estrategia(obj_update, estrategia, active_name):
    input_sup_res_m15 = obj_update["input_sup_res_m15"]
    input_sup_res_1h = obj_update["input_sup_res_1h"]
    input_sup_res_4h = obj_update["input_sup_res_4h"]
    input_status_estrategia = obj_update["input_status_estrategia"]
    input_candles_estrategia = obj_update["input_candles_estrategia"]

    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
                SELECT * from {TABLE_NAME_ESTRATEGIAS} WHERE active_name = "{active_name}"
                '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            tt_query = len(result_query)
            print("\n\n----------------------- result query | update")
            print(result_query)
            print(f"----------------------- TT QUERY: {tt_query}")
            if tt_query >=1:
                # status_strategy = {input_status_estrategia}
                comando_update = f"""
                UPDATE {TABLE_NAME_ESTRATEGIAS}
                    SET
                        {estrategia}_sup_res_m15 = {input_sup_res_m15},
                        {estrategia}_sup_res_1h = {input_sup_res_1h},
                        {estrategia}_sup_res_4h = {input_sup_res_4h},
                        {estrategia} = {input_candles_estrategia}
                    WHERE
                        active_name = "{active_name}" and
                        id >= 1;
                """
                cursor.execute(comando_update)
                conn["conn"].commit()
                print(comando_update)

                try:
                    cursor.close()
                    conn["conn"].close()
                    print(" DB - DESCONECTADO ")
                except Exception as e:
                    print(f"ERROR UPDATE 2 | ERROR: {e}")
                return {"status_update": True}
            else:
                return {"status_update": False}

    except Exception as e:
        print(f"ERROR UPDATE 2 | ERROR: {e}")
# ------------------------------------------------------------------------------ API
def query_database_api():
    """ QUERY para criar lista de requisições ao servidor websocket da IQ Option. """
    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
                SELECT * from {TABLE_NAME_ESTRATEGIAS}
                '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            print("\n\n----------------------- result query ")
            print(result_query)
            print("-----------------------")
            tt_query = len(result_query)
            print(tt_query)

            if tt_query >=1:
                list_requests = [
                    [], # 0  - _active_name
                    [], # 1  - _active_id
                    [], # 2  - estrategia_1
                    [], # 3  - estrategia_1_sup_res_m15
                    [], # 4  - estrategia_1_sup_res_1h
                    [], # 5  - estrategia_1_sup_res_4h
                    [], # 6  - estrategia_2
                    [], # 7  - estrategia_2_sup_res_m15
                    [], # 8  - estrategia_2_sup_res_1h
                    [], # 9  - estrategia_2_sup_res_4h
                    [], # 10 - estrategia_3
                    [], # 11 - estrategia_3_sup_res_m15
                    [], # 12 - estrategia_3_sup_res_1h
                    [], # 13 - estrategia_3_sup_res_4h
                    [], # 14 - estrategia_4
                    [], # 15 - estrategia_4_sup_res_m15
                    [], # 16 - estrategia_4_sup_res_1h
                    [], # 17 - estrategia_4_sup_res_4h

                    [], # 18 - estrategia_5
                    [], # 19 - estrategia_5_sup_res_m15
                    [], # 20 - estrategia_5_sup_res_1h
                    [], # 21 - estrategia_5_sup_res_4h
                    # ----
                    [], # 22 - estrategia_6
                    [], # 23 - estrategia_6_sup_res_m15
                    [], # 24 - estrategia_6_sup_res_1h
                    [], # 25 - estrategia_6_sup_res_4h
                    # ----
                    [], # 26 - estrategia_7
                    [], # 27 - estrategia_7_sup_res_m15
                    [], # 28 - estrategia_7_sup_res_1h
                    [], # 29 - estrategia_7_sup_res_4h
                ]

                for idx in range(tt_query):
                    list_requests[0].append(result_query[idx][1])
                    list_requests[1].append(result_query[idx][2])
                    list_requests[2].append(result_query[idx][3])
                    list_requests[3].append(result_query[idx][4])
                    list_requests[4].append(result_query[idx][5])
                    list_requests[5].append(result_query[idx][6])
                    list_requests[6].append(result_query[idx][7])
                    list_requests[7].append(result_query[idx][8])
                    list_requests[8].append(result_query[idx][9])
                    list_requests[9].append(result_query[idx][10])
                    list_requests[10].append(result_query[idx][11])
                    list_requests[11].append(result_query[idx][12])
                    list_requests[12].append(result_query[idx][13])
                    list_requests[13].append(result_query[idx][14])
                    list_requests[14].append(result_query[idx][15])
                    list_requests[15].append(result_query[idx][16])
                    list_requests[16].append(result_query[idx][17])
                    list_requests[17].append(result_query[idx][18])

                    list_requests[18].append(result_query[idx][19])
                    list_requests[19].append(result_query[idx][20])
                    list_requests[20].append(result_query[idx][21])
                    list_requests[21].append(result_query[idx][22])
                    # ----
                    list_requests[22].append(result_query[idx][23])
                    list_requests[23].append(result_query[idx][24])
                    list_requests[24].append(result_query[idx][25])
                    list_requests[25].append(result_query[idx][26])
                    # ----
                    list_requests[26].append(result_query[idx][27])
                    list_requests[27].append(result_query[idx][28])
                    list_requests[28].append(result_query[idx][29])
                    list_requests[29].append(result_query[idx][30])
                try:
                    cursor.close()
                    conn["conn"].close()
                    print(" DB - DESCONECTADO ")
                except Exception as e:
                    print(f"ERROR QUERY REQUEST 1 | ERROR: {e}")
                    return {"status_query": False}
                return PrepareData.create_dataframe_request(list_requests)
            else:
                return {"status_query": False}

    except Exception as e:
        print(f"ERROR QUERY REQUEST 2 | ERROR: {e}")
# ------------------------------------------------------------------------------ API
def query_visao_geral_config_database_api():
    """ QUERY para página de visão geral das configurações da API. """
    obj_estrategia_1 = dict()
    obj_estrategia_2 = dict()
    obj_estrategia_3 = dict()
    obj_estrategia_4 = dict()
    obj_estrategia_5 = dict()
    obj_estrategia_6 = dict()
    obj_estrategia_7 = dict()
    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
                SELECT * from {TABLE_NAME_ESTRATEGIAS} ORDER BY active_name
                '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            print("\n\n----------------------- result query ")
            print(result_query)
            print("-----------------------")
            tt_query = len(result_query)
            print(tt_query)

            for registro in result_query:
                obj_estrategia_1.update({registro[1]: {
                    "candles_M5": registro[3],
                    "sup_res_M15": registro[4],
                    "sup_res_1H": registro[5],
                    "sup_res_4H": registro[6],
                    }
                })
                obj_estrategia_2.update({registro[1]: {
                    "candles_M5": registro[7],
                    "sup_res_M15": registro[8],
                    "sup_res_1H": registro[9],
                    "sup_res_4H": registro[10],
                    }
                })
                obj_estrategia_3.update({registro[1]: {
                    "candles_M5": registro[11],
                    "sup_res_M15": registro[12],
                    "sup_res_1H": registro[13],
                    "sup_res_4H": registro[14],
                    }
                })
                obj_estrategia_4.update({registro[1]: {
                    "candles_M5": registro[15],
                    "sup_res_M15": registro[16],
                    "sup_res_1H": registro[17],
                    "sup_res_4H": registro[18],
                    }
                })
                obj_estrategia_5.update({registro[1]: {
                    "candles_M5": registro[19],
                    "sup_res_M15": registro[20],
                    "sup_res_1H": registro[21],
                    "sup_res_4H": registro[22],
                    }
                })
                obj_estrategia_6.update({registro[1]: {
                    "candles_M5": registro[23],
                    "sup_res_M15": registro[24],
                    "sup_res_1H": registro[25],
                    "sup_res_4H": registro[26],
                    }
                })
                obj_estrategia_7.update({registro[1]: {
                    "candles_M5": registro[27],
                    "sup_res_M15": registro[28],
                    "sup_res_1H": registro[29],
                    "sup_res_4H": registro[30],
                    }
                })
            
            
            try:
                cursor.close()
                conn["conn"].close()
                print(" DB - DESCONECTADO ")
            except Exception as e:
                print(f"ERROR QUERY REQUEST 1 | ERROR: {e}")
            return {
                "obj_estrategia_1": obj_estrategia_1,
                "obj_estrategia_2": obj_estrategia_2,
                "obj_estrategia_3": obj_estrategia_3,
                "obj_estrategia_4": obj_estrategia_4,
                "obj_estrategia_5": obj_estrategia_5,
                "obj_estrategia_6": obj_estrategia_6,
                "obj_estrategia_7": obj_estrategia_7
            }
           

    except Exception as e:
        print(f"ERROR QUERY REQUEST 2 | ERROR: {e}")
# -----------------------------------------
def update_status_api(status_api, email):
    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()
            comando_update = f"""
            UPDATE {TABLE_NAME_STATUS_API}
                SET
                    status_api = {status_api},
                    email = "{email}"
                WHERE
                    id = 2;
            """
            cursor.execute(comando_update)
            conn["conn"].commit()
            print(comando_update)

            try:
                cursor.close()
                conn["conn"].close()
                print(" DB - DESCONECTADO ")
            except Exception as e:
                print(f"ERROR UPDATE 2 | ERROR: {e}")
            return {"status_update": True}
        else:
            return {"status_update": False}

    except Exception as e:
        print(f"ERROR UPDATE 2 | ERROR: {e}")
# -----------------------------------------
def query_status_api():
    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()
            comando_query = f'''
                SELECT * from {TABLE_NAME_STATUS_API}
                '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            print("\n\n----------------------- result query ")
            print(result_query)
            try:
                cursor.close()
                conn["conn"].close()
                print(" DB - DESCONECTADO ")
            except Exception as e:
                print(f"ERROR UPDATE 2 | ERROR: {e}")
            
            return {"status_api": result_query[0][1], "email": result_query[0][2]}
        else:
            return {"status_api": False}

    except Exception as e:
        print(f"ERROR UPDATE 2 | ERROR: {e}")
# -----------------------------------------
def update_database_sign(obj_sign):
    observation = obj_sign["observation"]
    open_time = obj_sign["open_time"]
    alert_datetime = obj_sign["alert_datetime"]
    expiration_alert = obj_sign["expiration_alert"]
    expiration_alert_timestamp = obj_sign["expiration_alert_timestamp"]
    alert_time_update = obj_sign["alert_time_update"]
    resultado = obj_sign["resultado"]
    status_alert = obj_sign["status_alert"]
    padrao = obj_sign["padrao"]
    mercado = obj_sign["mercado"]
    active = obj_sign["active"]
    direction = obj_sign["direction"]
    name_strategy = obj_sign["name_strategy"]
    # ---
    sup_m15 = obj_sign["sup_m15"]
    sup_1h  = obj_sign["sup_1h"]
    sup_4h  = obj_sign["sup_4h"]
    # ---
    res_m15 = obj_sign["res_m15"]
    res_1h  = obj_sign["res_1h"]
    res_4h  = obj_sign["res_4h"]
    # ---

    list_open_types = ["alert-open-operation", "alert-open-operation-test"]
    if status_alert not in list_open_types and status_alert != "canceled":
        open_time = open_time
        resultado = "process"
    elif status_alert in list_open_types and direction == "put" or direction == "call":
        open_time = open_time
        resultado = "open"
    elif status_alert in list_open_types and direction != "put" and direction != "call":
        open_time = open_time
        status_alert = "canceled"
    
    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
                SELECT 
                    id, direction, status_alert
                FROM {TABLE_NAME_OPERATIONS}
                WHERE
                    name_strategy = "{name_strategy}" and expiration_alert = "{expiration_alert}"
                '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            tt_query = len(result_query)
            print("\n\n----------------------- result query | update")
            print(result_query)
            print(f"----------------------- TT QUERY: {tt_query}")
            if tt_query >= 1:
                try:
                    id_register = result_query[0][0]
                    # direction = result_query[0][1]

                    comando_update = f"""
                    UPDATE {TABLE_NAME_OPERATIONS}
                    SET
                        direction = "{direction}",
                        alert_time_update = "{alert_time_update}",
                        status_alert = "{status_alert}",
                        obs_analysis = "{observation}",
                        resultado = "{resultado}",
                        sup_m15 = {sup_m15},
                        sup_1h = {sup_1h},
                        sup_4h = {sup_4h},
                        res_m15 = {res_m15},
                        res_1h = {res_1h},
                        res_4h = {res_4h}
                    WHERE
                        id >= {id_register};
                    """
                    cursor.execute(comando_update)
                    conn["conn"].commit()
                    print("\n\n ### ALERTA ATUALIZADO COM SUCESSO ### ")
                    print(comando_update)
                except Exception as e:
                    print(f"\n ### ERROR 1 UPDATE ALERT | ERROR: {e} ###\n")
            
            elif tt_query == 0:
                try:
                    if status_alert not in list_open_types and status_alert not in ["alert-1min", "alert-1min-test"]:
                        comando_insert_alert = f'''
                            INSERT INTO {TABLE_NAME_OPERATIONS}
                                (
                                    obs_analysis,
                                    open_time, alert_datetime, expiration_alert, expiration_alert_timestamp, alert_time_update,
                                    resultado, status_alert, padrao,
                                    mercado, active, direction, name_strategy,
                                    sup_m15, sup_1h, sup_4h,
                                    res_m15, res_1h, res_4h
                                )
                            VALUES
                                (
                                    "{observation}",
                                    "{open_time}", "{alert_datetime}", "{expiration_alert}", "{expiration_alert_timestamp}", "{alert_time_update}",
                                    "{resultado}", "{status_alert}", "{padrao}",
                                    "{mercado}", "{active}", "{direction}", "{name_strategy}",
                                    {sup_m15}, {sup_1h}, {sup_4h},
                                    {res_m15}, {res_1h}, {res_4h}
                                )
                        '''
                        cursor.execute(comando_insert_alert)
                        conn["conn"].commit()
                        print("\n\n ### ALERTA INSERIDO COM SUCESSO ### ")
                        print(comando_insert_alert)
                    else:
                        print(f"SINAL NÃO INSERIDO NO BANCO DE DADOS | PRIMEIRO SINAL --> OPEN-OPERATION")
                except Exception as e:
                    print(f"\n ### ERROR 2 INSERT ALERT | ERROR: {e} ###\n")
        try:
            cursor.close()
            conn["conn"].close()
            print(" INSERT/UPDATE OK - DB - DESCONECTADO ")
            return {"status_update_alert": True}
        except Exception as e:
            print(f"ERROR INSERT / UPDATE ALERT 3 | ERROR: {e}")
    except Exception as e:
        print(f"ERROR INSERT / UPDATE ALERT 4 | ERROR: {e}")
# -----------------------------------------
def update_database_sign_result_open_operation(list_actives_check_results, dataframe_candles):
    print(" ------------------------------- CHECK RESULTS | dataframe_candles ------------------------------- ")
    print(dataframe_candles)
    print(list_actives_check_results)
    try:
        conn = conn_db_producao()
        cursor = None
        # -------------------------------------------------
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            for active in list_actives_check_results:
                print(f"ACTIVE CHECK: {active}")
                df_check = dataframe_candles[dataframe_candles["active_name"]== active]
                df_check.index = list(range(len(df_check.index)))
                print(df_check)
                expiration_alert    = df_check["from"][1]
                status_candle      = df_check["status_candle"][0]

                
                list_versions = ["M5-V1", "M5-V2", "M5-V3", "M5-V4", "M5-V5", "M5-V6", "M5-V7"]
                for version in list_versions:
                    
                    name_strategy = f'{active}-{version}'
                    
                    comando_query = f'''
                        SELECT 
                            id, direction, status_alert, expiration_alert, direction, resultado, name_strategy
                        FROM {TABLE_NAME_OPERATIONS}
                        WHERE
                            name_strategy = "{name_strategy}" and expiration_alert = "{expiration_alert}"
                        '''
                    cursor.execute(comando_query)
                    result_query    = cursor.fetchall()
                    tt_query = len(result_query)
                    print(result_query)
                    dt_now = datetime_now(tzone="America/Sao Paulo")
                    print(f"RESULT BROKER | from: {expiration_alert} | active_name: {active} | status_candle: {status_candle} | name_strategy: {name_strategy}")
                    print(f"COMADO QUERY CHECK RESULTS: {comando_query}")
                    print(f"----------------------- result query | update | TT QUERY: {tt_query}")
                    if tt_query >= 1:
                        for i in range(tt_query):
                            id_result = result_query[i][0]
                            direction_sign = result_query[i][1]
                            status_alert_sign = result_query[i][2]
                            exp_db = result_query[i][3]
                            print(f"DT NOW: {dt_now} | EXPIRATION DB: {expiration_alert}")
                            print(f"DT NOW MINUTES: {dt_now.minute} | EXPIRATION DB MINUTES: {exp_db.minute}\n\n")

                            resultado = "-"
                            if dt_now.minute == exp_db.minute:
                                if status_candle == "sem mov.":
                                    resultado = "empate"
                                elif direction_sign == "put" and status_candle == "baixa":
                                    resultado = "win"
                                elif direction_sign == "put" and status_candle == "alta":
                                    resultado = "loss"
                                elif direction_sign == "call" and status_candle == "alta":
                                    resultado = "win"
                                elif direction_sign == "call" and status_candle == "baixa":
                                    resultado = "loss"

                                # alert_time_update = "{dt_now.strftime("%Y-%m-%d %H:%M:%S")}"
                                comando_update_check_result = f'''
                                    UPDATE {TABLE_NAME_OPERATIONS}
                                        SET
                                            resultado = "{resultado}"
                                        WHERE
                                            id = {id_result};
                                '''
                                cursor.execute(comando_update_check_result)
                                conn["conn"].commit()
                                print(comando_update_check_result)
                                print("\n\n ### RESULTADO ATUALIZADO COM SUCESSO ### ")

                        

                    else:
                        print("CHECK RESULTS | NENHUM REGISTRO ENCONTRADO PARA ATUALIZAR.\n\n")
            try:
                cursor.close()
                conn["conn"].close()
                print(" DB - DESCONECTADO ")
            except Exception as e:
                print(f"ERROR UPDATE CHECK RESULTS 1 | ERROR: {e}")
    except Exception as e:
        print(f"ERROR UPDATE CHECK RESULTS 2 | ERROR: {e}")
    return {"status_update_alert": True}
# -----------------------------------------
def query_database_results_calc(active_name, strategy_name):
    print(f" ------------------------------- QUERY RESULTS | FOR DASHBOARDS | {active_name} | {strategy_name} ------------------------------- ")
    try:
        conn = conn_db_producao()
        cursor = None
        # -------------------------------------------------
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            obj_estrategias = {
                "estrategia_1": f"{active_name}-M5-V1",
                "estrategia_2": f"{active_name}-M5-V2",
                "estrategia_3": f"{active_name}-M5-V3",
                "estrategia_4": f"{active_name}-M5-V4",
                "estrategia_5": f"{active_name}-M5-V5",
                "estrategia_6": f"{active_name}-M5-V6",
                "estrategia_7": f"{active_name}-M5-V7"
            }
            
            name_strategy =  obj_estrategias[strategy_name]
                
            comando_query = f'''
                SELECT
                    id, direction, status_alert, expiration_alert, direction, resultado, name_strategy
                FROM {TABLE_NAME_OPERATIONS}
                WHERE
                    name_strategy = "{name_strategy}"
                '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            tt_query = len(result_query)
            print(result_query)
            print(f"TT QUERY ALL: {tt_query}")
            print("************************************************")
            if tt_query > 10:
                result_query = result_query[tt_query-10:]
                print(result_query)
                print(f"TT QUERY FATIA: {len(result_query)}")
                print(comando_query)
            obj_results = dict()
            for registro in result_query:
                _id                 = registro[0]
                direction           = registro[1]
                status_alert        = registro[2]
                expiration_alert    = registro[3]
                direction           = registro[4]
                resultado           = registro[5]
                name_strategy       = registro[6]

                className = "result-empate"
                if resultado == "win":
                    className = "result-win"
                elif resultado == "loss":
                    className = "result-loss"

                className_direction = "direction-comum"
                if direction == "call":
                    className_direction = "direction-call"
                elif direction == "put":
                    className_direction = "direction-put"
            
                valor = {_id: {
                    "expiration_alert": convert_datetime_to_string(expiration_alert),
                    "direction": direction,
                    "resultado": resultado,
                    "status_alert": status_alert,
                    "className": className,
                    "className_direction": className_direction,
                    }
                }
                obj_results.update(valor)
            try:
                cursor.close()
                conn["conn"].close()
                print(" DB - DESCONECTADO ")
            except Exception as e:
                print(f"ERROR UPDATE CHECK RESULTS 1 | ERROR: {e}")
            return obj_results
    except Exception as e:
        print(f"ERROR UPDATE CHECK RESULTS 2 | ERROR: {e}")
    return {"status_update_alert": True}