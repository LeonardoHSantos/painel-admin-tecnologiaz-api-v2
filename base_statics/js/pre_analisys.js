// console.log("pre_analysis.js carregado...");


function updateList(event){
    // let elementID = event.target.id;
    if (event.target.value != "todos"){
        let elementsToAnalyze = document.querySelectorAll(".elements-to-analyze");
        // console.log(elementsToAnalyze)
        let checkInsert = true;
        for(i=0; i < elementsToAnalyze.length; i++){
            let elementCheck = elementsToAnalyze[i].className.split(" ");
            if (elementCheck[0] == `element-${event.target.value}`){
                checkInsert = false;
            }
        }
        if (checkInsert == true){
        document.querySelector(".block-actives-to-analyze").innerHTML += `
        <span class="element-${event.target.value} elements-to-analyze">
            <p id="element-${event.target.value}"  onclick="removeActiveToAnalyze(event)">${event.target.value}</p>
        </span`;
        }
        document.getElementById("all-actives").selected = true;
    }
}
function removeActiveToAnalyze(event){
    document.querySelector(`.${event.target.id}`).remove();
}


// -----------------------------------------------------


async function get_data_pre_analise(url){

    
    document.querySelector(".animation-process-pre-analise").getElementsByClassName.display = "flex";
    try {
        let input_data_inicial = document.getElementById("input-data-inicial").value;
        let input_data_final = document.getElementById("input-data-final").value;
        let data_inicial_post = input_data_inicial;
        let data_final_post = input_data_final;
        // ---------
        let input_ativo = document.getElementById("input-ativo").value;
        let input_estrategia = document.getElementById("input-estrategia").value;
        // ---------
        let sup_res_m15 = document.getElementById("sup-res-m15").value;
        let sup_res_1h = document.getElementById("sup-res-1h").value;
        let sup_res_4h = document.getElementById("sup-res-4h").value;
        // ---------
        let input_email_broker = document.getElementById("input-email-broker").value;
        let input_password_broker = document.getElementById("input-password-broker").value;
        let input_token_painel = document.getElementById("input-token-painel").value;
        // -------
        let valid_dates = await checkDates(input_data_inicial, input_data_final);
        // --------
        if (input_email_broker == "" | input_password_broker == "" | input_token_painel == ""){
            showModalAuth();
        } else {
            let status_process = false
            if (valid_dates == true){status_process = true;};

            // --------------------------------------------------------------
            let listActives = [];
            let elementsToAnalyze = document.querySelectorAll(".elements-to-analyze");
            for(i=0; i < elementsToAnalyze.length; i++){
                let elementCheck = elementsToAnalyze[i].className.split(" ");
                listActives.push(elementCheck[0].replace("element-", ""))
            }
            console.log(listActives);
            if (listActives.length < 1){
                status_process = false;
            }
            // --------------------------------------------------------------
            // if (input_ativo == "todos") {status_process = false;};
            if (input_estrategia == "todos"){status_process = false;};
            
            
            // ---------------------------
            if (status_process == true){
    
                input_data_inicial = await convert_datetime_filtro(input_data_final, 0);
                input_data_final = await convert_datetime_filtro(input_data_final, 0);
        
                console.log(`
                    input_data_inicial: ${input_data_inicial}
                    input_data_final: ${input_data_final}
                    ------
                    data_inicial_post: ${data_inicial_post}
                    data_final_post: ${data_final_post}
                    -----
                    input_ativo: ${input_ativo}
                `);
                // "identifier": "leonardotradeiq@gmail.com",
                //  "password": "ContaTesteTrade",
                //  "token": "BLie7UNAvMRU6-Z0xMwXM-SUl42SQ7eiKays5XuQxDo",
                
                let data_post = {
                    "identifier": input_email_broker,
                    "password": input_password_broker,
                    "token": input_token_painel,
                    "estrategia": input_estrategia,
                    "list_active_names": listActives,
                    "data_inicio": data_inicial_post,
                    "data_fim": data_final_post,
                    "sup_res_m15": sup_res_m15,
                    "sup_res_1h": sup_res_1h,
                    "sup_res_4h": sup_res_4h,
                }
    
                // **************************************************************************************
                showModalNotificationProcess();
                // document.querySelector(".animation-process-pre-analise").style.display = "flex";
        
        
                fetch(url, {
                    method: "POST",
                    body: JSON.stringify(data_post)
                }).then((data)=>{
                    return data.json();
                }).then((data)=>{
                    data_post_final = data
                    // console.log(data)
                    if (JSON.parse(data_post_final["code-process"] == 200)){
                        let data_to_html = JSON.parse(data_post_final['data_to_html']);
                        // console.log(data_post_final);
                        // console.log(data_to_html);
                        
                        // // ---------------------
                        // document.getElementById("input-data-inicial").min = data_inicial_post;
                        // document.getElementById("input-data-inicial").max = data_final_post;
                        document.getElementById("input-data-inicial-filtro").min = data_inicial_post;
                        document.getElementById("input-data-inicial-filtro").max = data_final_post;
                        // ------------
                        // document.getElementById("input-data-final").min = data_inicial_post;
                        // document.getElementById("input-data-final").max = data_final_post;
                        document.getElementById("input-data-final-filtro").min = data_inicial_post;
                        document.getElementById("input-data-final-filtro").max = data_final_post;
                        // // ---------------------
            
                        create_table_results(data_to_html);
                        // document.querySelector(".animation-process-pre-analise").style.display = "none";
                        hideModalNotificationProcess();
                        try {localStorage.removeItem("base_analisada");} catch (error) {};
                        try {localStorage.setItem("base_analisada", JSON.stringify(data_to_html));} catch (error) {};
                        return
                    } else {
                        hideModalNotificationProcess();
                        showModalAuth();
                    }
                });
            } else {
                showModalNotificationError();
            }


        }
    } catch (error) {
        hideModalNotificationProcess();
    }
}

// --------
async function remove_element(element_tag){
    try {document.querySelector(element_tag).remove();} catch (error) {};
    return
}
// --------
async function add_element(element_tag, element){
    try {document.querySelector(element_tag).innerHTML += `<${element}></${element}>`;} catch (error) {};
    return
}
// --------
async function convert_datetime_filtro(input_data, add){
    input_data = new Date(input_data);
    let ano = input_data.getFullYear();
    let mes = input_data.getMonth();
    let dia = input_data.getDate();
    input_data = new Date(ano, mes, dia+add);
    return input_data
}
async function convert_datetime_final(input_data_final){
    input_data_final = new Date(input_data_final)
    return input_data_final.setDate(input_data_final.getDate() + 1);
}
// --------
async function convert_string_to_datetime(dt_string){
    let datetime = new Date(dt_string);
    return datetime;
}
// --------
async function create_table_results(data){
    await remove_element(".table-results-resume tbody");
    await add_element(".table-results-resume", "tbody");
    let table = document.querySelector(".table-results-resume tbody");

    let cont_aux = 1;
    let tt_win = 0;
    let tt_loss = 0;
    for (let i in data) {
        let result = data[i]["results"];
        if(result == "win"){
            tt_win = tt_win +1;
        } else if (result == "loss"){
            tt_loss = tt_loss +1;
        }

        try {
            let classObserver = "observer-data";
            if (i>=10){
                classObserver = "observer-data-off";
            }
            table.innerHTML += `
            <tr class="observer-data-${i} data-obs ${classObserver}">
                <td>${cont_aux}</td>
                <td>${data[i]["from"]}</td>
                <td>${data[i]["estrategia"]}</td>
                <td>${data[i]["active_name"]}</td>
                <td>${data[i]["status_candle"]}</td>
                <td class=${data[i]["class_name_direction"]}>${data[i]["sign"]}</td>
                <td class="${data[i]["class_name_results"]}" id="table-${i}" onmouseover="show_resume_pre_analise(event);" onmouseout="hide_resume_pre_analise(event);">
                    ${result}
                    <span class="resume-results-pre-analise data-table-${i}">
                        <p>${data[i-1]["from"]}</p>
                        <p>RES M15: ${data[i-1]["res_15m_extrato_tm"]}</p>
                        <p>RES 1H: ${data[i-1]["res_1h_extrato_tm"]}</p>
                        <p>RES 4H: ${data[i-1]["res_4h_extrato_tm"]}</p>

                        <p>SUP M15: ${data[i-1]["sup_15m_extrato_tm"]}</p>
                        <p>SUP 1H: ${data[i-1]["sup_1h_extrato_tm"]}</p>
                        <p>SUP 4H: ${data[i-1]["sup_4h_extrato_tm"]}</p>
                    </span>
                </td>

                <td>${data[i]["res_15m_extrato_tm"]}</td>
                <td>${data[i]["res_1h_extrato_tm"]}</td>
                <td>${data[i]["res_4h_extrato_tm"]}</td>
                <td>${data[i]["sup_15m_extrato_tm"]}</td>
                <td>${data[i]["sup_1h_extrato_tm"]}</td>
                <td>${data[i]["sup_4h_extrato_tm"]}</td>
            </tr>`;
            cont_aux = cont_aux + 1;
            document.querySelector(".content-card-tt-results").textContent = cont_aux-1;
            document.querySelector(".content-card-results-consolidado").textContent = tt_win + tt_loss;
            document.querySelector(".content-card-results-consolidado-win").textContent = tt_win;
            document.querySelector(".content-card-results-consolidado-loss").textContent = tt_loss;
        } catch (error) {}
    }
    createInterSectionElements();
}
// --------

async function checkDates(input_data_inicial, input_data_final){
    if (input_data_inicial != "" & input_data_final != "") {
        input_data_inicial = input_data_inicial + " 00:00:00";
        input_data_final = input_data_final + " 23:59:59";

        input_data_inicial = await convert_datetime_filtro(input_data_inicial, 0);
        input_data_final = await convert_datetime_filtro(input_data_final, 0);
        
        if (input_data_inicial <= input_data_final){
            return true;

        } else {
            return false
        }
    } else {
        return false
    }
}

async function execFiltros(){

    let input_data_inicial = document.getElementById("input-data-inicial-filtro").value;
    let input_data_final = document.getElementById("input-data-final-filtro").value;
    
    let status_process = false;
    let valid_dates = await checkDates(input_data_inicial, input_data_final);
    if(valid_dates == true) {
        document.querySelector(".error-inputs-date-valid").style.display = "none";
        document.getElementById("btn-filtrar-pre-analise").style.display = "none";
        document.querySelector(".animation-btn-process").style.display = "flex"; 
        filtrar_registros_pre_analise();
        setTimeout(()=>{
            createInterSectionElements();
        }, 3000);
    } else {
        document.querySelector(".error-inputs-date-valid").style.display = "flex";
    }
       
}
// --------
async function filtrar_registros_pre_analise(){
    let input_data_inicial = document.getElementById("input-data-inicial-filtro").value;
    let input_data_final = document.getElementById("input-data-final-filtro").value;
    // ---------
    // let input_ativo = document.getElementById("input-ativo").value;
    let input_direcao = document.getElementById("input-direcao").value;
    let input_resultado = document.getElementById("input-resultado").value;
    // ---------

    if (input_data_inicial != "" & input_data_final != "") {
        input_data_inicial = input_data_inicial + " 00:00:00";
        input_data_final = input_data_final + " 23:59:59";
        
        await remove_element(".table-results-resume tbody");
        await add_element(".table-results-resume", "tbody");

        input_data_inicial = await convert_datetime_filtro(input_data_inicial, 0);
        input_data_final = await convert_datetime_filtro(input_data_final, 1);
        
        if (input_data_inicial <= input_data_final){

            let table = document.querySelector(".table-results-resume tbody");
            let data_post_final_storage = JSON.parse(localStorage.getItem("base_analisada"));
            // console.log(data_post_final_storage);

            let cont_aux = 1;
            let tt_win = 0;
            let tt_loss = 0;
            let tt_empate = 0;
            let tt_confluencias = 0;
            let list_index = [];

            let progress_filter = 0;
            const PromisseProcessTable = new Promise((resolve, reject)=>{
                for (let i in data_post_final_storage) {
                    const convertExpiration = new Promise((resolve, reject)=>{
                        let datetime_expiration = convert_string_to_datetime(data_post_final_storage[i]["from"]);
                        resolve(datetime_expiration);
                    }).then((datetime_expiration)=>{
                        // let observer = new IntersectionObserver(entries =>{
                        //     console.log(entries);
                        // });
                        if ( datetime_expiration >= input_data_inicial & datetime_expiration <= input_data_final ) {
                            list_index.push(i);
    
                            let direction = data_post_final_storage[i]["sign"];
                            let result = data_post_final_storage[i]["results"];
                            
                            let insert_table = false;
                            if (input_direcao == "todos"){
                                insert_table = true;
                            } else {
                                if (input_direcao == "call_put") {
                                    if (direction == "call" | direction == "put"){
                                        insert_table = true;
                                    }
                                }
                                else if (input_direcao != "call_put" & input_direcao == direction) {
                                    insert_table = true;
                                }
                            }
                            // check input resultado
                            if (input_resultado != "todos") {
                                if (input_resultado == "win_loss"){
                                    if (result == "-") {
                                        insert_table = false;
                                    }
                                }
                                else if (input_resultado != result) {
                                    insert_table = false;
                                }
                            }
    
                            if (insert_table == true){
                                let observer_status = "observer-data";
                                if (i >= 10){
                                    observer_status = "observer-data-off";
                                }
                                try {
                                    table.innerHTML += `
                                    <tr class="observer-data-${i} data-obs ${observer_status}">
                                        <td>${cont_aux}</td>
                                        <td>${data_post_final_storage[i]["from"]}</td>
                                        <td>${data_post_final_storage[i]["estrategia"]}</td>
                                        <td>${data_post_final_storage[i]["active_name"]}</td>
                                        <td>${data_post_final_storage[i]["status_candle"]}</td>
                                        <td class="${data_post_final_storage[i]["class_name_direction"]}">${direction}</td>
                                        <td class="${data_post_final_storage[i]["class_name_results"]}" id="table-${i}" onmouseover="show_resume_pre_analise(event);" onmouseout="hide_resume_pre_analise(event);">
                                            ${result}
                                            <span class="resume-results-pre-analise data-table-${i}">
                                                <p>${data_post_final_storage[i-1]["from"]}</p>
                                                <p>RES M15: ${data_post_final_storage[i-1]["res_15m_extrato_tm"]}</p>
                                                <p>RES 1H: ${data_post_final_storage[i-1]["res_1h_extrato_tm"]}</p>
                                                <p>RES 4H: ${data_post_final_storage[i-1]["res_4h_extrato_tm"]}</p>
    
                                                <p>SUP M15: ${data_post_final_storage[i-1]["sup_15m_extrato_tm"]}</p>
                                                <p>SUP 1H: ${data_post_final_storage[i-1]["sup_1h_extrato_tm"]}</p>
                                                <p>SUP 4H: ${data_post_final_storage[i-1]["sup_4h_extrato_tm"]}</p>
                                            </span>
                                        </td>
        
                                        <td>${data_post_final_storage[i]["res_15m_extrato_tm"]}</td>
                                        <td>${data_post_final_storage[i]["res_1h_extrato_tm"]}</td>
                                        <td>${data_post_final_storage[i]["res_4h_extrato_tm"]}</td>
                                        <td>${data_post_final_storage[i]["sup_15m_extrato_tm"]}</td>
                                        <td>${data_post_final_storage[i]["sup_1h_extrato_tm"]}</td>
                                        <td>${data_post_final_storage[i]["sup_4h_extrato_tm"]}</td>
        
                                    </tr>`;
                                    if(result == "win"){
                                        tt_win = tt_win +1;
                                    } else if (result == "loss"){
                                        tt_loss = tt_loss +1;
                                    } else if (result == "empate"){
                                        tt_empate = tt_empate +1;
                                    }
                                    tt_confluencias =  tt_win + tt_loss + tt_empate;
                                    document.querySelector(".content-card-tt-results").textContent = cont_aux;
                                    document.querySelector(".content-card-results-consolidado").textContent = tt_confluencias;
                                    document.querySelector(".content-card-results-consolidado-win").textContent = tt_win;
                                    document.querySelector(".content-card-results-consolidado-loss").textContent = tt_loss;
                                    cont_aux = cont_aux + 1;
    
                                    
                                  
                            
                                } catch (error) {
                                    // hide_filter_block();
                                }
                            }
                        }
                    })
                }
                resolve(true)
            })
            PromisseProcessTable.then((status_process)=>{
                // createInterSectionElements();
                // console.log("acionado observer...")
                hide_filter_block();
            })
        } else {
            console.log("status da validação de datas: data inicial maior que data final.");
            console.log(input_data_inicial);
            console.log(input_data_final);
        }
    } else {
        console.log("status da validação de datas: todos os campos de datas devem ser preenchidos.");
    }
   
    document.getElementById("btn-filtrar-pre-analise").style.display = "flex";
    document.querySelector(".animation-btn-process").style.display = "none";
    let obj_results = [
        {"hora": 9, "result": "loss"},
        {"hora": 9, "result": "loss"},
        {"hora": 9, "result": "win"},
        {"hora": 9, "result": "win"},
        {"hora": 3, "result": "win"},
        {"hora": 0, "result": "win"},
        {"hora": 0, "result": "win"},
        {"hora": 1, "result": "loss"},
        {"hora": 1, "result": "win"},
        {"hora": 1, "result": "win"},
        {"hora": 1, "result": "win"},
        {"hora": 1, "result": "win"},
        {"hora": 1, "result": "win"},
        {"hora": 2, "result": "loss"},
        {"hora": 2, "result": "win"},
        {"hora": 2, "result": "loss"},
        {"hora": 2, "result": "loss"},
        {"hora": 7, "result": "loss"},
        {"hora": 7, "result": "win"},
        {"hora": 7, "result": "win"},
        {"hora": 7, "result": "win"},
        {"hora": 2, "result": "win"},
        {"hora": 2, "result": "loss"},
        {"hora": 3, "result": "loss"},
        {"hora": 3, "result": "win"},
    
        {"hora": 10, "result": "win"},
        {"hora": 10, "result": "loss"},
        {"hora": 10, "result": "loss"},
        {"hora": 11, "result": "win"},
        {"hora": 11, "result": "loss"},
        {"hora": 11, "result": "loss"},
        {"hora": 20, "result": "win"},
        {"hora": 20, "result": "loss"},
        {"hora": 20, "result": "loss"},
        {"hora": 20, "result": "win"},
        {"hora": 20, "result": "loss"},
        {"hora": 20, "result": "loss"},
    
        {"hora": 21, "result": "win"},
        {"hora": 21, "result": "loss"},
        {"hora": 21, "result": "loss"},
        {"hora": 22, "result": "win"},
        {"hora": 22, "result": "loss"},
        {"hora": 22, "result": "loss"},
        {"hora": 23, "result": "win"},
        {"hora": 23, "result": "loss"},
        {"hora": 23, "result": "loss"},
        {"hora": 23, "result": "win"},
        {"hora": 23, "result": "loss"},
        {"hora": 23, "result": "loss"},
    ];

    // criação do dashboard - em desenvolvimento
    // prepareDataToDashboard(obj_results);
    
}

// ------------------------- observer
function createInterSectionElements(){
    let observer = new IntersectionObserver(entries =>{
        // console.log(entries);
        // console.log(entries[0].isIntersecting);


        let next_value = parseInt(entries[0].target.className.split(" ")[0].split("-")[2]) +1
        let cont = 0;
        for(let i in document.querySelectorAll(".observer-data-off")){
            if (cont <= 10){
                try {
                    document.querySelectorAll(".observer-data-off")[i].classList.remove("observer-data-off"); 
                    cont += 1;
                } catch (error) {}
            }
        }
    }, {
        threshold: [0, .1, .5, 1]
    });
    Array.from(document.querySelectorAll(".data-obs")).forEach( element =>{
        try {
            if (element != undefined){
                // let elemnt_class = element.className.split(" ");
                elemnt_class = document.querySelector(`.${element.className.split(" ")[0]}`)
                observer.observe(elemnt_class);
                // console.log(elemnt_class);
            }
        } catch (error) {
            console.log(error) 
        }
    });  
}
// TABLE PRE ANALISE
function show_resume_pre_analise(event){
    try {
        let element = document.querySelector(`.data-${event.target.id}`);
        const x = event.clientX;
        const y = event.clientY;
        element.style.display = "flex";
        element.style.top = `${y+115}px`;
        element.style.left = `${x+55}px`;
    } catch (error) {}
}
function hide_resume_pre_analise(event) {
    try {
        let element = document.querySelector(`.data-${event.target.id}`);
        element.style.display = "none";
    } catch (error) {}
}

// ----------
function show_block_filters(){
    document.querySelector(".inputs-filters-pre-analise").style.display = "flex";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}
function hide_filter_block(){
    document.querySelector(".inputs-filters-pre-analise").style.display = "none";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}
// ----------
function show_block_auth_user(){
    document.querySelector(".inputs-auth-user").style.display = "flex";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}
function hide_block_auth_user(){
    document.querySelector(".inputs-auth-user").style.display = "none";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}
// ----------
function showModalNotificationProcess(){
    document.querySelector(".animation-process-pre-analise").style.display = "flex";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}
function hideModalNotificationProcess(){
    document.querySelector(".animation-process-pre-analise").style.display = "none";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}

// ----------
function showModalNotificationError(){
    document.querySelector(".notification-error-filters-process").style.display = "flex";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}
function hideModalNotificationError(){
    document.querySelector(".notification-error-filters-process").style.display = "none";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}
// ----------
function showModalAuth(){
    document.querySelector(".notification-error-filters-process-auth").style.display = "flex";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}
function hideModalAuth(){
    document.querySelector(".notification-error-filters-process-auth").style.display = "none";
    document.querySelector(".container-analise").classList.toggle("visible-content");
}