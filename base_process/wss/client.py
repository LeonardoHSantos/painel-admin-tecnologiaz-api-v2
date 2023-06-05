import websocket

from base_process.process.prepare_data.prepareData import PrepareData
from base_process.process.prepare_data.prepare_actives_open import process_open_actives

class WS_Client:
    def __init__(self, url) -> None:
        self.status_wss = False
        self.status_msg = False
        self.check_timestamp = None

        self.dataframe_actives_open = None
        self.status_process_actives_open = False

        self.dataframes_candles = []

        self.wss = websocket.WebSocketApp(
            url=url,
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error
        )
    
    def on_message(self, message):
        message = PrepareData.convert_data_to_json(message)
        self.status_msg = True
        # print(message["name"])
        if message["name"] == "timeSync":
            self.check_timestamp = message["msg"]
        
        elif message["name"] == "initialization-data":
            self.dataframe_actives_open = process_open_actives(dados=message["msg"])
            self.status_process_actives_open = True

        elif message["name"] == "candles":
            df = PrepareData.convert_data_to_dataframe_candles(message=message, request_id=message["request_id"])
            self.dataframes_candles.append(df)
            
    
    def on_open(self):
        self.status_wss = True
        print(f" ### CONNECTION OPEN WEBSOCKET ### | STATUS WSS: {self.status_wss}")
    def on_close(self):
        self.wss.close()
        self.status_wss = False
        self.status_msg = False
        print(f" ### CONNECTION CLOSED WEBSOCKET ### | STATUS WSS: {self.status_wss} | STATUS MSg: {self.status_msg}")
    def on_error(self, error):
        print(f" *** ERROR WSS | ERROR: {error} *** ")