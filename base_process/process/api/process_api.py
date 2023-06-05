import threading
import pandas as pd
from time import sleep
from base_process.http.auth import auth_broker
from base_process.wss.client import WS_Client
from base_process.data_aux.var_aux import URL_WSS
from base_process.process.expirations.expiration_candle import datetime_now
from database.query_database import update_database_sign_result_open_operation
from base_process.data_aux.var_time_active_operations import LIST_MINUTES_STRATEGY_1, LIST_MINUTES_STRATEGY_2, LIST_MINUTES_STRATEGY_3, LIST_MINUTES_STRATEGY_4, LIST_MINUTES_STRATEGY_5, LIST_MINUTES_STRATEGY_6, LIST_MINUTES_STRATEGY_7
from base_process.data_aux.var_time_active_operations import LIST_MINUTES_STRATEGY_1_OPEN_OPERATION, LIST_MINUTES_STRATEGY_2_OPEN_OPERATION, LIST_MINUTES_STRATEGY_3_OPEN_OPERATION, LIST_MINUTES_STRATEGY_4_OPEN_OPERATION, LIST_MINUTES_STRATEGY_5_OPEN_OPERATION, LIST_MINUTES_STRATEGY_6_OPEN_OPERATION, LIST_MINUTES_STRATEGY_7_OPEN_OPERATION


from database.query_database import query_database_api, update_status_api
from base_process.process.prepare_data.channels import ChannelsWSS
from base_process.process.prepare_data.prepareData import PrepareData
from base_process.process.analisys.analyze_strategies import AnalyzeData_Strategies

class ProcessAPI:
    def __init__(self, identifier, password) -> None:
        self.identifier = identifier
        self.password = password
        self.obj_wss = None
        self.threading_wss = None
        self.threading_process = None
        self.control_bool_api = False

    def auth(self):
        SSID = None
        CHECK_CREDENCIALS = False
        auth = auth_broker(self.identifier, self.password)

        if auth["code"] != "success":
            SSID = None
            CHECK_CREDENCIALS = False
            print(f'ERROR AUTH | CHECK_CREDENCIALS: {CHECK_CREDENCIALS} | ERROR: {auth["message"]}')
            return False
        
        elif auth["code"] == "success":
            SSID = auth["ssid"]
            CHECK_CREDENCIALS = True
            print(auth)
            print(f'SUCCESS AUTH | CHECK_CREDENCIALS: {CHECK_CREDENCIALS} | CODE: {auth["code"]}\n')
            return auth["ssid"]

    def connect_wss(self):
        try:
            self.obj_wss.on_close()
            print(" ########## API FINALIZADA ########## ")
        except Exception as e:
            print(e)
        auth = self.auth()
        print(f"AUTH: {auth}")
        if auth == False:
            return {"auth_status": False}
        else:
            self.obj_wss = WS_Client(url=URL_WSS)
            self.threading_wss = threading.Thread(target=self.obj_wss.wss.run_forever).start()
            msg_SSID = PrepareData.create_message_websocket(name="ssid", msg=auth, request_id="")
            msg_SSID = PrepareData.convert_data_to_string(msg_SSID)
            print(f"MSG SSID: {msg_SSID}")
            while True:
                if self.obj_wss.status_msg != False:
                    break
            self.obj_wss.wss.send(msg_SSID)
            return {"auth_status": True} 
    # --------------------
    def stop_process_api(self):
        try:
            print("-------->>> INÍCIO PROCESSO CLOSE WSS")
            self.obj_wss.on_close()
            self.control_bool_api = False
            
            print(" ### API FINALIZADA ### ")
        except Exception as e:
            print(f" *** ERROR CLOSE WSS | ERROR: {e} *** ")       
    # --------------------
    def start_api(self):
        self.control_bool_api = True
        return self.admin_process()
    # --------------------
    def admin_process(self):
        _auth = self.connect_wss()
        if _auth["auth_status"] == True:
            self.threading_process = threading.Thread(target=self.threading_process_api)
            self.threading_process.start()
            return _auth
        else:
            return _auth
    # --------------------
    def threading_process_api(self):
        list_check_tm = []
        try:
            while True:
                if self.control_bool_api == True:
                    dt_now = datetime_now(tzone="America/Sao Paulo")
                    _seconds = dt_now.second
                    _minutes = dt_now.minute
                    sleep(1)
                    try:
                        # print(f"check: {self.obj_wss.check_timestamp}")
                        list_check_tm.append(self.obj_wss.check_timestamp)
                        if list_check_tm.count(self.obj_wss.check_timestamp) >= 4:
                            print("#### TENTANDO SE RECONECTAR AO WEBSOCKET ####")
                            sleep(3)
                            self.start_api()
                        
                        elif list_check_tm.count(self.obj_wss.check_timestamp) < 4:
                            if _seconds >= 3 and _seconds <= 4:
                                self.process_check_results_operations()
                            elif _seconds >= 12 and _seconds <= 13:
                                self.process_operation(minutes=_minutes, type_process="process_comum")
                            elif _seconds >= 40 and _seconds <= 41:
                                self.process_operation(minutes=_minutes, type_process="process_open_operation")
                    except Exception as e:
                        print(e)
                else:
                    break
        except Exception as e:
            update_status_api(0)
    
    # --------------------------------------------------------------------------- CHECK PROCESS OPERATIONS
    def process_operation(self, minutes, type_process):
        # -------------------------------------------------------------- COLETA DADOS DO BANCO
        actives_database = query_database_api()
        print(actives_database)
        # -------------------------------------------------------------- COLETA DADOS DA CORRETORA
        msg_GET_ACTIVES_OPEN = ChannelsWSS.get_actives_open()
        self.obj_wss.wss.send(msg_GET_ACTIVES_OPEN)
        print(msg_GET_ACTIVES_OPEN)
        while True:
            if self.obj_wss.status_process_actives_open == True:
                break
        self.obj_wss.status_process_actives_open = False
        print(f"\n\n\n# STATUS PROCESS DATAFRAME: {self.obj_wss.status_process_actives_open}")
        
        print("DATAFRAME --------------------------------------------------")
        dataframe_actives_open = self.obj_wss.dataframe_actives_open
        print(dataframe_actives_open)
        print("FIM DATAFRAME --------------------------------------------------")

        # ----------------------------------------------------------------------------------------- DEFINIÇÃO DE QUAIS ESTRATÉGIAS SERÃO ANALISADAS
        list_estrategias = []
        check_status_alert = "process"
        if type_process == "process_comum":
            # if minutes in LIST_MINUTES_STRATEGY_1.keys():
            #     list_estrategias.append("estrategia_1")
            #     check_status_alert = LIST_MINUTES_STRATEGY_1[minutes]
            # # ---
            # if minutes in LIST_MINUTES_STRATEGY_2.keys():
            #     list_estrategias.append("estrategia_2")
            #     check_status_alert = LIST_MINUTES_STRATEGY_2[minutes]
            # # ---
            # if minutes in LIST_MINUTES_STRATEGY_3.keys():
            #     list_estrategias.append("estrategia_3")
            #     check_status_alert = LIST_MINUTES_STRATEGY_3[minutes]
            # # ---
            # if minutes in LIST_MINUTES_STRATEGY_4.keys():
            #     list_estrategias.append("estrategia_4")
            #     check_status_alert = LIST_MINUTES_STRATEGY_4[minutes]
            # # ---
            if minutes in LIST_MINUTES_STRATEGY_5.keys():
                list_estrategias.append("estrategia_5")
                check_status_alert = LIST_MINUTES_STRATEGY_5[minutes]
            # ---
            if minutes in LIST_MINUTES_STRATEGY_6.keys():
                list_estrategias.append("estrategia_6")
                check_status_alert = LIST_MINUTES_STRATEGY_6[minutes]
            # ---
            if minutes in LIST_MINUTES_STRATEGY_7.keys():
                list_estrategias.append("estrategia_7")
                check_status_alert = LIST_MINUTES_STRATEGY_7[minutes]
            # ------------------------------------------
        
        elif type_process == "process_open_operation":
            # if minutes in LIST_MINUTES_STRATEGY_1_OPEN_OPERATION.keys():
            #     list_estrategias.append("estrategia_1")
            #     check_status_alert = LIST_MINUTES_STRATEGY_1_OPEN_OPERATION[minutes]
            # # ---
            # if minutes in LIST_MINUTES_STRATEGY_2_OPEN_OPERATION.keys():
            #     list_estrategias.append("estrategia_2")
            #     check_status_alert = LIST_MINUTES_STRATEGY_2_OPEN_OPERATION[minutes]
            # # ---
            # if minutes in LIST_MINUTES_STRATEGY_3_OPEN_OPERATION.keys():
            #     list_estrategias.append("estrategia_3")
            #     check_status_alert = LIST_MINUTES_STRATEGY_3_OPEN_OPERATION[minutes]
            # # ---
            # if minutes in LIST_MINUTES_STRATEGY_4_OPEN_OPERATION.keys():
            #     list_estrategias.append("estrategia_4")
            #     check_status_alert = LIST_MINUTES_STRATEGY_4_OPEN_OPERATION[minutes]
            # ---
            if minutes in LIST_MINUTES_STRATEGY_5_OPEN_OPERATION.keys():
                list_estrategias.append("estrategia_5")
                check_status_alert = LIST_MINUTES_STRATEGY_5_OPEN_OPERATION[minutes]
            # ---
            if minutes in LIST_MINUTES_STRATEGY_6_OPEN_OPERATION.keys():
                list_estrategias.append("estrategia_6")
                check_status_alert = LIST_MINUTES_STRATEGY_6_OPEN_OPERATION[minutes]
            # ---
            if minutes in LIST_MINUTES_STRATEGY_7_OPEN_OPERATION.keys():
                list_estrategias.append("estrategia_7")
                check_status_alert = LIST_MINUTES_STRATEGY_7_OPEN_OPERATION[minutes]
            # ------------------------------------------
        
        print(f"\n\n ########### SERÁ ANALISADO OS PADRÃOES: {list_estrategias} ########### \n\n")
        # list_estrategias=["estrategia_1", "estrategia_2", "estrategia_3", "estrategia_4", "estrategia_5"]

        # -----------------------------------------------------------------------------------------
        if len(list_estrategias) >= 1:
            list_requests = PrepareData.create_list_requests_candles(
                list_estrategias=list_estrategias,
                actives_database=actives_database,
                dataframe_actives_open=dataframe_actives_open
            )
            expiration = int(datetime_now(tzone="America/Sao Paulo").timestamp())
            list_msg_requests = ChannelsWSS.get_candles(list_requests, expiration)

            cont_requests = 0
            for msg in list_msg_requests:
                print(msg)
                self.obj_wss.wss.send(msg)
                cont_requests += 1
            while True:
                if len(self.obj_wss.dataframes_candles) == cont_requests:
                    break
            
            dataframe_candles = pd.concat(self.obj_wss.dataframes_candles)
            index_df = list(range(0, len(dataframe_candles.index)))
            dataframe_candles.index = index_df
            print(dataframe_candles)
            # status_alert = LIST_MINUTES_STRATEGY[minutes]
            AnalyzeData_Strategies.process_sup_res(dataframe_candles=dataframe_candles, status_alert=check_status_alert)
        else:
            print("---> CICLO SEM PADRÃO PARA ANALISAR - AGUARDAR...")
        # dataframe_candles.to_excel("base teste.xlsx")
        self.obj_wss.dataframes_candles.clear()
    
    # --------------------------------------------------------------------------- CHECK RESULTS OPERATIONS
    def process_check_results_operations(self):
        # -------------------------------------------------------------- COLETA DADOS DO BANCO
        actives_database = query_database_api()
        print(actives_database)
        # -------------------------------------------------------------- COLETA DADOS DA CORRETORA
        msg_GET_ACTIVES_OPEN = ChannelsWSS.get_actives_open()
        self.obj_wss.wss.send(msg_GET_ACTIVES_OPEN)
        print(msg_GET_ACTIVES_OPEN)
        while True:
            if self.obj_wss.status_process_actives_open == True:
                break
        self.obj_wss.status_process_actives_open = False
        print(f"\n\n\n# CHECK RESULTS OPEN OPERATIONS | STATUS PROCESS DATAFRAME: {self.obj_wss.status_process_actives_open}")
        
        print("DATAFRAME ACTIVES OPEN --------------------------------------------------")
        dataframe_actives_open = self.obj_wss.dataframe_actives_open
        print(dataframe_actives_open)
        print("FIM DATAFRAME --------------------------------------------------")

        # ----------------------------------------------------------------------------------------- COLETA DE DADOS DA CORRETORA
        list_requests = PrepareData.create_list_requests_candles_check_results_operations(
            dataframe_actives_open=dataframe_actives_open,
            actives_database=actives_database,
        )
        expiration = int(datetime_now(tzone="America/Sao Paulo").timestamp())
        list_msg_requests = ChannelsWSS.get_candles_check_results_open_operations(list_requests, expiration)

        cont_requests = 0
        for msg in list_msg_requests:
            print(msg)
            self.obj_wss.wss.send(msg)
            cont_requests += 1
        while True:
            if len(self.obj_wss.dataframes_candles) == cont_requests:
                break
        
        print("DATAFRAMES - CONCATENADOS --------------------------------------------------")
        dataframe_candles = pd.concat(self.obj_wss.dataframes_candles)
        index_df = list(range(0, len(dataframe_candles.index)))
        dataframe_candles.index = index_df
        print(dataframe_candles)
        list_actives_check_results = list(dataframe_candles["active_name"].drop_duplicates(keep="last").values)
        update_database_sign_result_open_operation(list_actives_check_results, dataframe_candles)

        self.obj_wss.dataframes_candles.clear()








