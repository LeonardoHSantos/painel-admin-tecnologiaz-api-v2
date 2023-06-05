import pandas as pd
from database.conn import conn_db_producao
from base_process.process.expirations.expiration_candle import datetime_now, convert_datetime_to_string
from config_auth import TABLE_NAME_OPERATIONS, TABLE_NAME_ESTRATEGIAS, TABLE_RANK_OPERATIONS_M5

obj_name_strategies = {
    "estrategia_1":  "PADRAO-M5-V1",
    "estrategia_2":  "PADRAO-M5-V2",
    "estrategia_3":  "PADRAO-M5-V3",
    "estrategia_4":  "PADRAO-M5-V4",
    "estrategia_5":  "PADRAO-M5-V5",
    "estrategia_6":  "PADRAO-M5-V6",
    "estrategia_7":  "PADRAO-M5-V7"
}


# def query_database_prod_estrategia(data_inicio, data_fim):
def query_database_prod_estrategia(string_query):
    try:
        conn = conn_db_producao()
        cursor = None
        dict_results = dict()
        resume_results = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
                SELECT
                    id, mercado, active, padrao, direction, resultado, status_alert,
                    alert_datetime, expiration_alert, alert_time_update,
                    name_strategy,
                    sup_m15, sup_1h, sup_4h, res_m15, res_1h, res_4h
                 from
                    {TABLE_NAME_OPERATIONS}
                {string_query}
                '''
            # WHERE
            #         expiration_alert >= "{data_inicio}" and expiration_alert <= "{data_fim}"
            print(comando_query)
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            tt_query = len(result_query)
            print("\n\n----------------------- PROD | result query ")
            # print(result_query)
            print(f"TT QUERY PROD: {tt_query}")
            print("FIM PROD -----------------------")
            tt_call = 0
            tt_put = 0
            list_results = []
            tt_win_call = 0
            tt_loss_call = 0
            tt_win_put = 0
            tt_loss_put = 0

            if tt_query >= 1:
                for registro in result_query:
                    _id                 = registro[0]
                    _mercado            = registro[1]
                    _active             = registro[2]
                    _padrao             = registro[3]
                    _direction          = registro[4]
                    _resultado          = registro[5]
                    _status_alert       = registro[6]
                    _alert_datetime     = registro[7]
                    _expiration_alert   = registro[8]
                    _alert_time_update  = registro[9]
                    _name_strategy      = registro[10]
                    # --------------------------------
                    _sup_m15            = registro[11]
                    _sup_1h             = registro[12]
                    _sup_4h             = registro[13]
                    _res_m15            = registro[14]
                    _res_1h             = registro[15]
                    _res_4h             = registro[16]

                    _result_temp = None
                    className = "result-empate"
                    if _resultado == "win":
                        _result_temp = "win"
                        className = "result-win"
                    # ------------------------------
                    elif _resultado == "loss":
                        _result_temp = "loss"
                        className = "result-loss"
                   
                    className_direction = "direction-comum"
                    if _direction == "call":
                        tt_call = tt_call + 1
                        className_direction = "direction-call"
                        if _result_temp == "win":
                            tt_win_call = tt_win_call + 1
                        elif _result_temp == "loss":
                            tt_loss_call = tt_loss_call + 1
                    # -----------------------------------------
                    elif _direction == "put":
                        tt_put = tt_put + 1
                        className_direction = "direction-put"
                        if _result_temp == "win":
                            tt_win_put = tt_win_put + 1
                        elif _result_temp == "loss":
                            tt_loss_put = tt_loss_put + 1
                    
                    
                        
                    
                    data = {
                        f"{_id}": {
                            "id": _id,
                            "mercado": _mercado,
                            "active": _active,
                            "padrao": _padrao,
                            "direction": _direction,
                            "resultado": _resultado,
                            "expiration_alert": convert_datetime_to_string(_expiration_alert),
                            "status_alert": _status_alert,
                            "class_name": className,
                            "className_direction": className_direction,
                            "sup_m15": _sup_m15,
                            "sup_1h": _sup_1h,
                            "sup_4h": _sup_4h,
                            "res_m15": _res_m15,
                            "res_1h": _res_1h,
                            "res_4h": _res_4h,
                            "alert_datetime": convert_datetime_to_string(_alert_datetime),
                            "alert_time_update": convert_datetime_to_string(_alert_time_update),
                        }
                    }
                    # print(data)
                    dict_results.update(data)
                resume_results = {
                    "tt_query": int(tt_query),
                    "tt_call": tt_call,
                    "tt_put": tt_put,
                    "tt_win": tt_win_call + tt_win_put,
                    "tt_loss": tt_loss_call + tt_loss_put,

                    "tt_win_call": tt_win_call,
                    "tt_loss_call": tt_loss_call,

                    "tt_win_put": tt_win_put,
                    "tt_loss_put": tt_loss_put,
                }
                
                    # print(f"_id: {_id} | _mercado: {_mercado} | _active: {_active} | _padrao: {_padrao} | _direction: {_direction} | _resultado: {_resultado} | _expiration_alert: {_expiration_alert}")
        try:
            cursor.close()
            conn["conn"].close()
            print(" DB - DESCONECTADO ")
        except Exception as e:
            print(f"ERROR QUERY 1 | ERROR: {e}")
        return dict_results, resume_results
    except Exception as e:
        print(f"ERROR QUERY 2 | ERROR: {e}")

# -----------------------------------------------
def edit_registro_visao_geral(body):
    estrategia =    body["estrategia"]
    active_name =   body["active_name"]
    candles_M5 =    int(body["candles_M5"])
    sup_res_M15 =   int(body["sup_res_M15"])
    sup_res_1H =    int(body["sup_res_1H"])
    sup_res_4H =    int(body["sup_res_4H"])
    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_update = f"""
            UPDATE {TABLE_NAME_ESTRATEGIAS}
                SET
                    {estrategia} = {candles_M5},
                    {estrategia}_sup_res_m15 = {sup_res_M15},
                    {estrategia}_sup_res_1h = {sup_res_1H},
                    {estrategia}_sup_res_4h = {sup_res_4H}
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
            return {"status_update": True}
        except Exception as e:
            print(f"ERROR UPDATE - VISÃO GERAL | ERROR: {e}")
            return {"status_update": False}
    except Exception as e:
        print(f"ERROR UPDATE 2 - VISÃO GERAL | ERROR: {e}")
        return {"status_update": False}

# --------------------------------------------------------------  
# query - ranking results
def query_operations_resume_M5(active_name, estrategia):
    try:
        conn = conn_db_producao()
        cursor = None
        dict_resume = dict()
        resume_results = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
            SELECT 
                id, active, direction, resultado, mercado, status_alert, padrao, name_strategy
            FROM
                {TABLE_NAME_OPERATIONS}
            where active = "{active_name}" and  padrao = "{obj_name_strategies[estrategia]}";
            '''
            print(comando_query)
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            tt_query = len(result_query)
            results = None
            #  -------
            if tt_query >= 1 :
                tt_win = 0
                tt_loss = 0
                tt_empate = 0
                tt_resume = 0
                perc_win = 0.0
                perc_loss = 0.0
                retroativo = 5
                results = result_query[len(result_query)-retroativo:]
                for result in results:
                    if result[3] == "win":
                        tt_win += 1
                    elif result[3] == "loss":
                        tt_loss += 1
                    elif result[3] == "empate":
                        tt_empate += 1
                tt_resume = tt_win + tt_loss + tt_empate

                if tt_win >= 1:
                    perc_win = float(tt_win / tt_resume)
                else:
                    perc_win = 0.0
                # -------------------------
                if tt_loss >= 1:
                    perc_loss = float(tt_loss / tt_resume)
                else:
                    perc_loss = 0.0
                data = {
                    "active_name": active_name,
                    "estrategia": estrategia,
                    "tt_win":tt_win,
                    "tt_loss":tt_loss,
                    "tt_empate":tt_empate,
                    "tt_resume":tt_resume,
                    "perc_win":perc_win,
                    "perc_loss":perc_loss
                }
                dict_resume.update(data)
            else:
                data = {
                    "active_name": active_name,
                    "estrategia": estrategia,
                    "tt_win": 0,
                    "tt_loss": 0,
                    "tt_empate": 0,
                    "tt_resume": 0,
                    "perc_win": 0.0,
                    "perc_loss": 0.0
                }
                dict_resume.update(data)
        try:
            cursor.close()
            conn["conn"].close()
            print(" DB - DESCONECTADO ")
        except Exception as e:
            print(f"ERROR DESCONNECT 1 | ERROR: {e}")
        
        return results, dict_resume
          
    except Exception as e:
        print(f"ERROR QUERY RANK 1 | ERROR: {e}")
        try:
            cursor.close()
            conn["conn"].close()
            print(" DB - DESCONECTADO ")
        except Exception as e:
            print(f"ERROR DESCONNECT 2 | ERROR: {e}")

def update_ranking_M5(obj_results):
    active_name = obj_results["active_name"]
    estrategia = obj_results["estrategia"]
    tt_win = obj_results["tt_win"]
    tt_loss = obj_results["tt_loss"]
    tt_empate = obj_results["tt_empate"]
    tt_resume = obj_results["tt_resume"]
    perc_win = obj_results["perc_win"]
    perc_loss = obj_results["perc_loss"]
    try:
        conn = conn_db_producao()
        cursor = None
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()
            comando_update = f'''
            UPDATE
                {TABLE_RANK_OPERATIONS_M5}
            SET
                {estrategia}_tt_win = {tt_win},
                {estrategia}_tt_loss = {tt_loss},
                {estrategia}_tt_empate = {tt_empate},
                {estrategia}_perc_win = {perc_win},
                {estrategia}_perc_loss = {perc_loss}
            WHERE
                active_name = "{active_name}" and id >= 1
            '''
            print(comando_update)
            cursor.execute(comando_update)
            conn["conn"].commit()
            print("SUCCESS UPDATE RANK STRATEGIES")

        try:
            cursor.close()
            conn["conn"].close()
            print(" DB - DESCONECTADO ")
            return {"status_update": True}
        except Exception as e:
            print(f"ERROR UPDATE - VISÃO GERAL | ERROR: {e}")
            return {"status_update": False}


    except Exception as e:
        print(f"ERROR UPDATE RANKING OPERATIONS | ERROR: {e}")
        return {"status_update": False}


# checagem de sinal -> verifica se existe um sinal para a expiração atual.
# O resultado será utilizado para classificar qual paridade será continuada na operação atual.
def check_sign_ranking(expiration):
    """
        1) consulta sinais com próximas entradas para expirar em 5M;\n
        2) classifica o melhor resultado;\n
        3) se houver mais de um sinal, a melhor estratégia com a melhor paridade terá o status-alert continuado;\n
        4) os demais sinais com a mesma expiração terá o status-alert modificado para "canceled-double-signal".\n
        Objetivo do processo:\n
        - Evitar 2 ou mais sinais ao mesmo tempo.
    """
    try:
        list_signs = list()
        
        conn = conn_db_producao()
        cursor = None
        # -------------------------------------------------
        if conn["status_conn_db"] == True:
            cursor = conn["conn"].cursor()

            comando_query = f'''
            SELECT 
                id, active, direction, status_alert, padrao, name_strategy, alert_datetime, expiration_alert, alert_time_update
            FROM
                {TABLE_NAME_OPERATIONS}
            WHERE
                expiration_alert = "{expiration}"
            '''
            cursor.execute(comando_query)
            result_query    = cursor.fetchall()
            tt_query = len(result_query)
            # print(result_query)
            print(f" *** TT QUERY | CHECK EXPIRATIONS SIGN: {tt_query} *** ")
            _obj_name_strategies = {
                "PADRAO-M5-V1": "estrategia_1",
                "PADRAO-M5-V2": "estrategia_2",
                "PADRAO-M5-V3": "estrategia_3",
                "PADRAO-M5-V4": "estrategia_4",
                "PADRAO-M5-V5": "estrategia_5",
                "PADRAO-M5-V6": "estrategia_6",
                "PADRAO-M5-V7": "estrategia_7"
            }
            if tt_query >= 1:
                for sign in result_query:
                    if sign[1] not in list_signs:
                    
                        comando_query = f'''
                        SELECT 
                            id, active_name, {_obj_name_strategies[sign[4]]}_perc_win
                        FROM
                            {TABLE_RANK_OPERATIONS_M5}
                        WHERE
                            active_name = "{sign[1]}"
                        '''
                        cursor.execute(comando_query)
                        result_query_rank = cursor.fetchall()
                        list_signs.append(
                            {
                                "id_sign": sign[0],
                                "active_name":result_query_rank[0][1],
                                "perc_win": result_query_rank[0][2],
                                "padrao": _obj_name_strategies[sign[4]],
                                "status_alert": sign[3]
                            }
                        )
            
            df = pd.DataFrame(list_signs).sort_values(by="perc_win", ascending=False)
            df.index = list(range(0, len(df.index)))
            # ----------------------
            check_2 = df[df["status_alert"]=="alert-open-operation"]
            check_2.index = list(range(0, len(check_2.index)))
            
            if len(check_2.index) > 1:
                for idx in check_2.index:
                    if idx >= 1:
                        check_2["status_alert"][idx] = "alert-canceled-double-signal"

                        comando_update_sign = f'''
                        UPDATE
                            {TABLE_NAME_OPERATIONS}
                        SET
                            status_alert = "alert-signal-double-canceled"
                        WHERE
                            id = {check_2["id_sign"][idx]}
                        '''
                        cursor.execute(comando_update_sign)
                        conn["conn"].commit()
                        print(comando_update_sign)
            try:
                cursor.close()
                conn["conn"].close()
                print(" DB - DESCONECTADO ")
            except Exception as e:
                print(f"ERROR CHECK RESULTS 1 | ERROR: {e}")
            return check_2
    except Exception as e:
        print(f"ERROR CHECK RESULTS 2 | ERROR: {e}")
        try:
            cursor.close()
            conn["conn"].close()
            print("#2 DB - DESCONECTADO ")
        except Exception as e:
            print(f"ERROR CHECK RESULTS 1 | ERROR: {e}")
    return {"status_get_results": False}

