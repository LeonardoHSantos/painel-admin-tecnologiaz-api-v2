from . import views
from django.urls import path

urlpatterns = [
    path("register-user-admin/", views.register_user_admin, name="register_user_admin"),
    path("login-admin/", views.login_user_admin, name="login_admin"),
    path("logout-user", views.logout_user, name="logout_user"),
    path("", views.home, name="home"),
    path("query-results-operations-get-data-dashboard/", views.query_results_operations_get_data_dashboard, name="query_results_operations_get_data_dashboard"),
    path("autenticacao-iqoption/", views.autenticao_iqoption, name="autenticacao_iqoption"),
    path("start-api/", views.start_api, name="start_api"),
    path("stop-api/", views.stop_api, name="stop_api"),
    # path("config-admin/", views.config_admin, name="config_admin"),
    path("config-admin-get/", views.config_admin_get, name="config_admin_get"),
    path("config-admin-post/", views.config_admin_post, name="config_admin_post"),
    path("config-visao-geral/", views.visao_geral_config, name="config_visao_geral"),
    path("edit-config-visao-geral/", views.edit_visao_geral_config, name="edit_config_visao_geral"),
    path("pre-analise/", views.pre_analise, name="pre_analise"),
    path("get-data-pre-analise/", views.get_data_pre_estrategia, name="get_data_pre_estrategia"),


    # path("painel-config-test/", views.painel_config_test, name="painel_config_test"),
    # path("get-data-temp/", views.get_data_temp, name="get_data_temp"),
    # path("instrucoes-painel/", views.instrucoes_painel, name="instrucoes_painel"),
]