from base_process.process.prepare_data.prepareData import PrepareData

TIMEFRAMES_NAME = {
	30:  	"30S",
	60:  	"1M",
	300:  	"5M",
	900: 	"15M",
	3600:  	"1H",
	14400:	"4H",
}
class ChannelsWSS:
    def get_actives_open():
        name = 'sendMessage'
        message = {'name': 'get-initialization-data', 'version': '3.0', 'body': {}}
        request_id = 'get-underlying-list'
        msg = PrepareData.create_message_websocket(name=name, msg=message, request_id=request_id)
        return PrepareData.convert_data_to_string(data=msg)
    
    # -------------------------------------------------------------------------------------------
    def get_candles(list_requests, expiration):
        try:
            name = 'sendMessage'
            list_msg_requests = []
            for _msg in list_requests:
                for idx in range(len(_msg["timeframes"])):
                    print(idx, _msg["active_id"], _msg["active_name"], _msg["timeframes"][idx], _msg["amounts_sup_res"][idx])
                    if int(_msg["amounts_sup_res"][idx]) >= 1:
                        message = {
                            'name': 'get-candles',
                            'version': '2.0',
                            'body': {
                                'active_id': int(_msg["active_id"]),
                                'size': int(_msg["timeframes"][idx]),
                                'to': int(expiration),
                                'count': int(_msg["amounts_sup_res"][idx]),
                            }
                        }
                        request_id = f"{_msg['active_name']} - {_msg['estrategia']} - {TIMEFRAMES_NAME[int(_msg['timeframes'][idx])]}"
                        msg_GET_CANDLES = PrepareData.create_message_websocket(name=name, msg=message, request_id=request_id)
                        list_msg_requests.append(PrepareData.convert_data_to_string(msg_GET_CANDLES))
            return list_msg_requests
        except Exception as e:
            print(f"\n ### ERROR CREATE GET CANDLES PROCESS ChannelsWSS.get_candles | ERROR: {e} ### \n")
            return None
    
    # -------------------------------------------------------------------------------------------
    def get_candles_check_results_open_operations(list_requests, expiration):
        name = 'sendMessage'
        list_msg_requests = []
        # active_id
        # active_name
        # timeframes
        # amounts_sup_res
        for _msg in list_requests:
            print(_msg["active_id"], _msg["active_name"], _msg["timeframes"], _msg["amounts_sup_res"])        
            message = {
                'name': 'get-candles',
                'version': '2.0',
                'body': {
                    'active_id': int(_msg["active_id"]),
                    'size': int(_msg["timeframes"]),
                    'to': int(expiration),
                    'count': int(_msg["amounts_sup_res"]),
                }
            }
            request_id = f"check-results - {_msg['active_name']} - {TIMEFRAMES_NAME[int(_msg['timeframes'])]}"
            msg_GET_CANDLES = PrepareData.create_message_websocket(name=name, msg=message, request_id=request_id)
            list_msg_requests.append(PrepareData.convert_data_to_string(msg_GET_CANDLES))
        return list_msg_requests
