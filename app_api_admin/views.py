import json
import bcrypt
import threading
import requests

from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from base_process.data_aux import var_aux
from config_auth import LIST_PADROES, LIST_ALERTAS, IP_SERVER_API_PRE_ANALISE

from base_process.process.api.process_api import ProcessAPI
from base_process.process.expirations.expiration_candle import datetime_now
from database.query_prod import query_database_prod_estrategia, edit_registro_visao_geral
from database.query_database import query_database_estrategia, update_database_estrategia, update_status_api, query_status_api, query_database_actives_all, query_database_results_calc, query_visao_geral_config_database_api


from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

CONTROL_API = None

@csrf_exempt
def get_data_pre_estrategia(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            identifier = data["identifier"]
            password = data["password"]
            token = data["token"]
            estrategia = data["estrategia"]
            list_active_names = data["list_active_names"]
            data_inicio = data["data_inicio"]
            data_fim = data["data_fim"]
            print(f"""
                ----------------------- POST - PAINEL
                --> identifier: {identifier}
                --> password: {password}
                --> token: {token}
                --> estrategia: {estrategia}
                --> list_active_names: {list_active_names}
                --> data_inicio: {data_inicio}
                --> data_fim: {data_fim}
            """)
            data = json.loads(requests.post(url=f"http://{IP_SERVER_API_PRE_ANALISE}/run-analysis/", data= json.dumps(data)).content)
            
            # import pandas as pd
            # obj_to_html = json.loads(data["data_to_html"])
            # df = pd.DataFrame(obj_to_html)
            # df.to_excel("analise.xlsx")
            # print(df)
            
            return JsonResponse(data)
        except Exception as e:
            print(f" #### ERRO AO PROCESSAR PRE ANÁLISE | ERROR: {e}")
            return JsonResponse({"code-process": 400, "msg": "erro ao processar pré análise."})

# -------------------
@login_required(login_url="login_admin")
def autenticao_iqoption(request):
    if request.method == "GET":
        # print(f"REQUEST/GET: {request.GET}")
        q = query_status_api()
        bool_status_api = False
        if q["status_api"] == 1:
            bool_status_api = True
        context = {
            "bool_status_api": bool_status_api,
            "status_api": q["status_api"],
            "email": q["email"]
        }
        return render(request, "app/autenticacao_broker.html", context)
    elif request.method == "POST":
        print(f" ---> REQUEST / POST: {request.POST}")
        email       = request.POST.get("username-iqoption")
        password    = request.POST.get("password-iqoption")
        _status_api  = request.POST.get("status-api")
        print(f"email: {email} | password: {password} | status_api: {_status_api}")
        process_api_on = None
        process_api_off = None
        q = query_status_api()
        if int(_status_api) == 0 and q["status_api"] == 1:
            process_api_on = stop_api(status_api=_status_api, email=email)
            if process_api_on["code"] == 200:
                process_api_on = "run-sucess"
                update_status_api(status_api=0, email=email)
            else:
                process_api_on = "run-failed"
                update_status_api(status_api=1, email=email)

        elif int(_status_api) == 1 and q["status_api"] == 0:
            process_api_off = start_api(status_api=_status_api, identifier=email, password=password)
            if process_api_off["code"] == 200:
                process_api_off = "stop-sucess"
                update_status_api(status_api=1, email=email)
            else:
                process_api_off = "stop-failed"
                update_status_api(status_api=0, email=email)

        context = {
            "status_api": _status_api,
            "email": email,
            "process_api_on": process_api_on,
            "process_api_off": process_api_off,
            "msg_status": True
        }
        return render(request, "app/autenticacao_broker.html", context)
# -------------------
@csrf_exempt
def start_api(request):
    data = json.loads(request.body)
    status_api = data["status_api"]
    identifier = data["email"]
    password = data["password"]

    try:
        var_aux.CONTROL_STATUS_API = ProcessAPI(identifier=identifier, password=password)
        _start = var_aux.CONTROL_STATUS_API.start_api()
        print(f"************************************************ START API: {_start}")
        if _start["auth_status"] == True:
            update_status_api(status_api=status_api, email=identifier)
            return JsonResponse({"code": 200, "status_api": "run-success", "control_api": 1})
        else:
            update_status_api(status_api=0, email=identifier)
            return JsonResponse({"code": 400, "status_api": "run-failed", "control_api": 0})
    except Exception as e:
        print(f"ERROR START API | ERROR: {e}")
        return JsonResponse({"code": 500, "msg": str(e).replace("'", "")})
# -------------------
@csrf_exempt
def stop_api(request):
    data = json.loads(request.body)
    # print("data ----> ", data)
    email = data["email"]
    status_api = data["status_api"]
    try:
        threading.Thread(target=update_status_api(status_api=status_api, email=email)).start()
        threading.Thread(target=var_aux.CONTROL_STATUS_API.stop_process_api()).start()
        return JsonResponse({"code": 200, "status_api": "stop-success", "control_api": 0})
    except Exception as e:
        print(f"ERROR STOP API | ERROR: {e}")
        return JsonResponse({"code": 500, "status_api": str(e).replace("'", ""), "control_api": 0})