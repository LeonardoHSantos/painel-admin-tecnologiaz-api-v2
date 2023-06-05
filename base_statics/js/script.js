// console.log("script js carregado...");

//
function moveDownScroll(){
    window.scrollBy(0, 2000); 
}



function animation_btn_form(event) {
    document.getElementById(event.target.id).style.display = "none";
    document.querySelector(".content-animation-btn-form").style.display = "flex";
}
// LIBERA INPUTS FORM CONFIG ADMIN
let input_select_estrategia = document.getElementById("input-select-estrategia").value;
let input_select_paridade = document.getElementById("input-select-paridade").value;
if (input_select_estrategia == "selecione_uma_estrategia" & input_select_paridade == "selecione_uma_paridade") {
    // let input_status = document.getElementById('input-status-estrategia');
    // if (input_status.checked == true) {
    //     input_status.value = "1";
    // } else {
    //     input_status.value = "0";
    // }
    document.getElementById('input-select-paridade').disabled = true;
    document.getElementById('input-sup-res-m15').disabled = true;
    document.getElementById('input-sup-res-1h').disabled = true;
    document.getElementById('input-sup-res-4h').disabled = true;
    // document.getElementById('input-status-estrategia').disabled = true;
    document.getElementById('input-qtd-candles-estrategia').disabled = true;
    document.getElementById('search-form-config').disabled = true;
    document.getElementById('search-form-config').style.color = "#f56b6b";
    document.getElementById('search-form-config').style.backgroundColor = "#7b27c5";

    document.getElementById('save-form-config').disabled = true;
    document.getElementById('save-form-config').style.color = "#f56b6b";
    document.getElementById('save-form-config').style.backgroundColor = "#7b27c5";
}

// 
function checkedInputs_Form(){
    let input_select_estrategia = document.getElementById("input-select-estrategia").value;
    let input_select_paridade = document.getElementById("input-select-paridade").value;
    if (input_select_estrategia != "selecione_uma_estrategia") {
        document.getElementById('input-select-paridade').disabled = false;
        document.getElementById('input-sup-res-m15').disabled = false;
        document.getElementById('input-sup-res-1h').disabled = false;
        document.getElementById('input-sup-res-4h').disabled = false;
        // document.getElementById('input-status-estrategia').disabled = false;
        document.getElementById('input-qtd-candles-estrategia').disabled = false;
        document.getElementById('save-form-config').disabled = true;
         
        
        if (input_select_paridade != "selecione_uma_paridade") {
            document.getElementById('search-form-config').disabled = false;
            document.getElementById('search-form-config').style.color = "var(--color-white-1)";
            document.getElementById('search-form-config').style.backgroundColor = "var(--color-dark-1)"; 
        } else {
            document.getElementById('search-form-config').disabled = true;
            document.getElementById('search-form-config').style.color = "#f56b6b";
            document.getElementById('search-form-config').style.backgroundColor = "#7b27c5";
        } 

    } else if (input_select_estrategia == "selecione_uma_estrategia") { 
        document.getElementById('input-select-paridade').disabled = true;
        document.getElementById('input-sup-res-m15').disabled = true;
        document.getElementById('input-sup-res-1h').disabled = true;
        document.getElementById('input-sup-res-4h').disabled = true;
        // document.getElementById('input-status-estrategia').disabled = true;
        document.getElementById('input-qtd-candles-estrategia').disabled = true;
        document.getElementById('save-form-config').disabled = true;
        document.getElementById('search-form-config').disabled = true;
        document.getElementById('search-form-config').style.color = "#f56b6b";
        document.getElementById('search-form-config').style.backgroundColor = "#7b27c5";
    }
}

function checkedInputs_Form_SUP_RES(){
    document.getElementById('save-form-config').disabled = false;
    document.getElementById('save-form-config').style.color = "var(--color-white-1)";
    document.getElementById('save-form-config').style.backgroundColor = "var(--color-dark-1)"; 
}
// 
function alter_status_estrategia() {
    checkedInputs_Form_SUP_RES();
    // let input_status = document.getElementById('input-status-estrategia');
    // if (input_status.checked == true) {
    //     input_status.value = "1";
    // } else {
    //     input_status.value = "0";
    // }
}
// 
function GetConfigAdmin(url) {
    let input_select_estrategia = document.getElementById("input-select-estrategia").value;
    let input_select_paridade = document.getElementById("input-select-paridade").value;
    if (input_select_estrategia != "selecione_uma_estrategia" & input_select_paridade != "selecione_uma_paridade") {
        
        let input_select_paridade = document.getElementById('input-select-paridade').value;       
        // console.log(`input_select_estrategia: ${input_select_estrategia}`);
        // console.log(`input_select_paridade: ${input_select_paridade}`);
    
        let body = {
            "input_select_estrategia": input_select_estrategia,
            "input_select_paridade": input_select_paridade
        }
        fetch(url, {
            method: 'POST',
            body: JSON.stringify(body),
        }).then((data)=>{
            return data.json();
        }).then((data)=>{
            console.log(data);
            data_filter = data["data"];
            data_results = JSON.parse(data["query_results"]);
            console.log(data_filter)
            console.log(data_results)
            if (data_filter["status_query"] == true) {
                document.getElementById('input-sup-res-m15').value = data_filter["sup_res_m15"];
                document.getElementById('input-sup-res-1h').value = data_filter["sup_res_1h"];
                document.getElementById('input-sup-res-4h').value = data_filter["sup_res_4h"];
                document.getElementById('input-qtd-candles-estrategia').value = data_filter["check_estrategia"];
                
                document.querySelector(".table-results-resume tbody").remove();
                document.querySelector(".table-results-resume").innerHTML += "<tbody></tbody>";
                let table_resume = document.querySelector(".table-results-resume tbody");
                for(let idx in data_results) {
                    table_resume.innerHTML += `
                        <tr>
                            <td>${idx}</td>
                            <td>${data_results[idx]["expiration_alert"]}</td>
                            <td class="${data_results[idx]["className_direction"]}">${data_results[idx]["direction"]}</td>
                            <td class="${data_results[idx]["className"]}">${data_results[idx]["resultado"]}</td>
                        </tr>
                    `;
                }







                // if (parseInt(data["check_estrategia"]) >= 1){
                //     document.getElementById("input-status-estrategia").value = 1;
                //     document.getElementById("input-status-estrategia").checked = true;
                // }
                // else if (parseInt(data["check_estrategia"]) == 0){
                //     document.getElementById("input-status-estrategia").value = 0;
                //     document.getElementById("input-status-estrategia").checked = false;
                // }
            }
        })
    }
}
// 
function sendFormConfigAdmin(url) {
    let input_select_estrategia = document.getElementById('input-select-estrategia').value;
    let input_select_paridade = document.getElementById('input-select-paridade').value;
    let input_sup_res_m15 = document.getElementById('input-sup-res-m15').value;
    let input_sup_res_1h = document.getElementById('input-sup-res-1h').value;
    let input_sup_res_4h = document.getElementById('input-sup-res-4h').value;
    // let input_status_estrategia = document.getElementById('input-status-estrategia').value;
    let input_qtd_candles_estrategia = document.getElementById('input-qtd-candles-estrategia').value;
    
    
    let body = {
        "input_select_estrategia": input_select_estrategia,
        "input_select_paridade": input_select_paridade,
        "input_sup_res_m15": input_sup_res_m15,
        "input_sup_res_1h": input_sup_res_1h,
        "input_sup_res_4h": input_sup_res_4h,
        // "input_status_estrategia": input_status_estrategia,
        "input_status_estrategia": 0,
        "input_qtd_candles_estrategia": input_qtd_candles_estrategia,
    }
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(body),
    }).then((data)=>{
        document.getElementById('save-form-config').disabled = true;
        document.getElementById('save-form-config').style.color = "#f56b6b";
        document.getElementById('save-form-config').style.backgroundColor = "#7b27c5";
        return data.json();
    }).then((data)=>{
        // console.log(data);
        if (data["status_update"] == true) {
            document.querySelector(".content-msg-sucess-save").style.display = "flex";
            document.querySelector(".content-msg-sucess-save").innerHTML += `
            <div class="content-msg-sucess">
                <p>Alterações Salvas!</p>
            </div>
            `;
            setTimeout(()=>{
                document.querySelector(".content-msg-sucess-save").style.display = "none";
                document.querySelector(".content-msg-sucess").remove()
            }, 1800);
        }
        else if (data["status_update"] == false) {
            document.querySelector(".content-msg-sucess-save").style.display = "flex";
            document.querySelector(".content-msg-sucess-save").style.backgroundColor = "#f56b6b";
            
            document.querySelector(".content-msg-sucess-save").innerHTML += `
            <div class="content-msg-sucess">
                <p>Falha ao salvar!</p>
            </div>
            `;
            setTimeout(()=>{
                document.querySelector(".content-msg-sucess-save").style.display = "none";
                document.querySelector(".content-msg-sucess").remove()
            }, 1800);
        }
    })
}