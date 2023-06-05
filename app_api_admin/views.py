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


# -------------------
def register_user_admin(request):
    if request.method == "GET":
        get_user = User.objects.all()
        print(f" GET | USERS --->>> {get_user}")
        return render(request, "app/register_user.html")
    if request.method == "POST":
        # print(request.POST)
        username   = request.POST.get("username")
        email       = request.POST.get("email_user")
        password    = request.POST.get("password_user")
        password_2  = request.POST.get("password_user_2")

        if password != password_2:
            context = {
                "username": username,
                "email": email,
                "password_user": password,
                "password__user_2": password_2,
                "password_error": True
            }
            return render(request, "app/register_user.html", context=context)
        if len(password) <= 5:
            context = {
                "username": username,
                "email": email,
                "password_user": password,
                "password__user_2": password_2,
                "password_error_tam": True
            }
            return render(request, "app/register_user.html", context=context)
        
        get_user = User.objects.all()
        print(f" POST | USERS --->>> {get_user}")

        filter_user = User.objects.filter(username=username) #, password=password)
        filter_email = User.objects.filter(email=email) #, password=password)
        print(f" ------------------>> filter_user: {filter_user} | TT: {len(filter_user)}")
        print(f" ------------------>> filter_email: {filter_email} | TT: {len(filter_email)}")
        if len(filter_user) >= 1 or len(filter_email) >= 1:
            context = {
                "username": username,
                "email": email,
                "password": password,
                "password_2": password_2,
                "user_unavailable": True
            }
            return render(request, "app/register_user.html", context=context)
        
        User.objects.create_user(username=username, email=email, password=password)
        print("\n\n ************************** Conta Criada Com Sucesso!!! **************************")
        return redirect("login_admin")
# -------------------
def login_user_admin(request):
    if request.method == "GET":
        get_user = User.objects.all()
        print(get_user)
        return render(request, "app/login.html")
    if request.method == "POST":
        email       = request.POST.get("email_user") # email_user
        password    = request.POST.get("password_user") # password_user
        print(f"POST ------------------> {request.POST}")

        # get_user = User.objects.all()
        filter_user = User.objects.filter(username=email)
        # filter_email = User.objects.filter(email=email)
        print(f"FILTER USER -------------->> {filter_user}")
        
        _user = authenticate(username=email, passoword=password)
        if _user is None:
            context = {
                "email": email,
                "password": password,
                "user_unavailable": True
            }
            return render(request, "app/login.html", context=context)
        else:
            login(request=request, user=_user)
            return redirect("home")
# -------------------
def logout_user(request):
    logout(request=request)
    return redirect("login_admin")
# -------------------
@login_required(login_url="login_admin")
def home(request):
    # print(f"USER ----------------> {str(request.user)}")
    if request.method == "GET":
        query = query_database_actives_all()
        print(query)
        list_actives = query
        list_padroes = [""]
        # print(f"---------------->>> ACTIVES ALL: {list_actives}")
        context = {
            "list_actives": list_actives,
            "list_padroes": LIST_PADROES,
            "list_alertas": LIST_ALERTAS,
        }
        return render(request, "app/home.html", context=context)      
# -------------------
@login_required(login_url="login_admin")
def config_admin(request):
    q = query_status_api()
    # print(f"\n\n\n ################# GET CONFIG ADMIN:  {q}")
    bool_status_api = False
    if q["status_api"] == 1:
        bool_status_api = True
    
    list_actives = query_database_actives_all()
    context = {
        "bool_status_api": bool_status_api,
        "status_api": q["status_api"],
        "list_actives": list_actives,
    }
    return render(request, "app/config_admin.html", context)
# -------------------
@csrf_exempt
def config_admin_get(request):
    data = json.loads(request.body)
    # print(data)
    input_select_estrategia = data["input_select_estrategia"]
    input_select_paridade = data["input_select_paridade"]
    # print(f"input_select_estrategia: {input_select_estrategia}")
    # print(f"input_select_paridade: {input_select_paridade}")

    data = query_database_estrategia(estrategia=input_select_estrategia, active_name=input_select_paridade)
    # print(f"GET DATA: {data}")
    query_results = query_database_results_calc(active_name=input_select_paridade, strategy_name=input_select_estrategia)
    print(f"\n\n\n---------------------------->>>>RESULTS: {query_results}")
    return JsonResponse({"data":data, "query_results": json.dumps(query_results)})
# -------------------
@csrf_exempt
def config_admin_post(request):
    data = json.loads(request.body)
    # print(data)

    input_select_estrategia = data["input_select_estrategia"]
    input_select_paridade = data["input_select_paridade"]
    input_sup_res_m15 = data["input_sup_res_m15"]
    input_sup_res_1h = data["input_sup_res_1h"]
    input_sup_res_4h = data["input_sup_res_4h"]
    input_status_estrategia = data["input_status_estrategia"]
    input_candles_estrategia = data["input_qtd_candles_estrategia"]

    obj_update = {
        "input_sup_res_m15": int(input_sup_res_m15),
        "input_sup_res_1h": int(input_sup_res_1h),
        "input_sup_res_4h": int(input_sup_res_4h),
        "input_status_estrategia": int(input_status_estrategia),
        "input_candles_estrategia": int(input_candles_estrategia),
    }
    data = update_database_estrategia(obj_update=obj_update, estrategia=input_select_estrategia, active_name=input_select_paridade)
    return JsonResponse(data)
# -------------------
@csrf_exempt
@login_required(login_url="login_admin")
def visao_geral_config(request):
    if request.method == "GET":
        
        return render(request, "app/config_visao_geral.html")
    elif request.method == "POST":
        body = json.loads(request.body)
        estrategia = body["estrategia"]
        print(f"\n\n\n-------------------------> BODY POST: {estrategia}")
        base_config = query_visao_geral_config_database_api()
        context = {
            "estrategia": estrategia,
            "obj_estrategia_1": base_config["obj_estrategia_1"],
            "obj_estrategia_2": base_config["obj_estrategia_2"],
            "obj_estrategia_3": base_config["obj_estrategia_3"],
            "obj_estrategia_4": base_config["obj_estrategia_4"],  
            "obj_estrategia_5": base_config["obj_estrategia_5"], 
            "obj_estrategia_6": base_config["obj_estrategia_6"], 
        }
        return JsonResponse(context)
# -------------------
@csrf_exempt
def edit_visao_geral_config(request):
    body = json.loads(request.body)
    print(body)
    edit = edit_registro_visao_geral(body)
    return JsonResponse(edit)
# -------------------
@csrf_exempt
@login_required(login_url="login_admin")
def pre_analise(request):
    if request.method == "GET":
        query = query_database_actives_all()
        print(query)
        list_actives = query
        list_padroes = [""]
        # print(f"---------------->>> ACTIVES ALL: {list_actives}")
        context = {
            "list_actives": list_actives,
            "list_padroes": LIST_PADROES,
        }
        return render(request, "app/pre_analise.html", context=context)
# ---
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

def process_pre_analise():
    return 

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
# -------------------
@csrf_exempt
def query_results_operations_get_data_dashboard(request):
    data_inicio = None
    data_fim = None
    if request.method == "POST":
        data = json.loads(request.body)
        data_inicio = data["data_inicio"]
        data_fim = data["data_fim"]
        # print(f"\n\n\nBODY --------------------->>>>> {data}")
        if data_inicio == None or data_inicio == "":
            data_inicio = datetime_now(tzone="America/Sao Paulo") + timedelta(days=-1)
            data_inicio.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
        else:
            data_inicio = data_inicio + f" 00:00:00"
        # ------------------------------------
        if data_fim == None or data_fim == "":
            data_fim = datetime_now(tzone="America/Sao Paulo").replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
        else:
            data_fim = data_fim + f" 23:59:59"
        # ------------------------------------
        string_query = "WHERE "
        for k, v in data.items():
            # print(f"------------------------>>> K: {k} | V: {v}")
            if k != "data_inicio" and k != "data_fim":
                if v != "todos" and v != "":
                    if string_query == "WHERE ":
                        string_query = string_query + f' {k} = "{v}"'
                    else:
                        string_query = string_query + f' and {k} = "{v}"'
                    # print(string_query)
        
        # string_query.replace("WHERE  and", "WHERE ")
        if string_query == "WHERE ":
            string_query = string_query + f'expiration_alert >= "{data_inicio}" and expiration_alert <= "{data_fim}"'
        elif string_query != "WHERE ":
            string_query = string_query + f' and expiration_alert >= "{data_inicio}" and expiration_alert <= "{data_fim}"'
        # print(f"QUERY -------->>> {string_query}")
        
        try:
            # data = query_results_operations(string_query=string_query)
            data = query_database_prod_estrategia(string_query)
            # print(f"DATA RESULT -------------> {data}")
            return JsonResponse({"code": 200, "data": json.dumps(data[0]), "resume_results": data[1]})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400})

# -------------------
@login_required(login_url="login_admin")
def painel_config_test(request):
    if request.method == "GET":
        query = query_database_actives_all()
        print(query)
        list_actives = query
        context = {
            "list_actives": list_actives,
            "list_padroes": LIST_PADROES,
            "list_alertas": LIST_ALERTAS,
        }
        
        return render(request, "app/painel_test.html", context=context)
# ---
# @login_required(login_url="login_admin")
def get_data_temp(request): # request
    print(request.POST)
    print(request.body)
    import pandas as pd
    data = pd.read_excel("analise.xlsx")
    print(data.info())
    data_to_html = dict()
    for i in data.index:
        valor = {
            f"{i}":
            {
                "from": data["from"][i],
                "active_name": data["active_name"][i],
                "status_candle": data["status_candle"][i],
                "sign": data["sign"][i],
                "results": data["results"][i],
                "estrategia": data["estrategia"][i],
                "class_name_results": data["class_name_results"][i],
                "class_name_direction": data["class_name_direction"][i],
                "res_15m_extrato_tm": int(data["res_15m_extrato_tm"][i]),
                "res_1h_extrato_tm": int(data["res_1h_extrato_tm"][i]),
                "res_4h_extrato_tm": int(data["res_4h_extrato_tm"][i]),
                "sup_15m_extrato_tm": int(data["sup_15m_extrato_tm"][i]),
                "sup_1h_extrato_tm": int(data["sup_1h_extrato_tm"][i]),
                "sup_4h_extrato_tm": int(data["sup_4h_extrato_tm"][i]),
            }}
        data_to_html.update(valor)
    # print(data_to_html)
    return JsonResponse(data_to_html)
