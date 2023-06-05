// console.log("scriptDashboard.js carregado...");

function getDataDashboardPrincipal(url) {
    // console.log("getDataDashboardPrincipal acionado...");

    let input_data_inicial = document.getElementById("input-data-inicial").value;
    let input_data_final = document.getElementById("input-data-final").value;
    let input_mercado = document.getElementById("input-mercado").value;
    let input_ativo = document.getElementById("input-ativo").value;
    let input_direcao = document.getElementById("input-direcao").value;
    let input_resultado = document.getElementById("input-resultado").value;
    let input_estrategia = document.getElementById("input-estrategia").value;
    let input_alerta = document.getElementById("input-alerta").value;
    let data = {
        "data_inicio": input_data_inicial,
        "data_fim": input_data_final,
        "mercado": input_mercado,
        "active": input_ativo,
        "direction": input_direcao,
        "resultado": input_resultado,
        "padrao": input_estrategia,
        "status_alert": input_alerta
    }
    // console.log(data);

    fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
    }).then((data)=>{
        return data.json();
    }).then((data)=> {
        // console.log(`resultados aqui: `, data);
        document.querySelector(".content-card-results-consolidado").textContent = data["resume_results"]["tt_query"];
        
        document.querySelector(".card-result-geral-direction-result-call").textContent = data["resume_results"]["tt_call"];
        document.querySelector(".card-result-geral-direction-result-put").textContent = data["resume_results"]["tt_put"];
        
        document.querySelector(".content-card-results-consolidado-win").textContent = data["resume_results"]["tt_win"];
        document.querySelector(".content-card-results-consolidado-loss").textContent = data["resume_results"]["tt_loss"];
        
        // call
        document.querySelector(".card-result-extrato-win-call").textContent = data["resume_results"]["tt_win_call"];
        document.querySelector(".card-result-extrato-loss-call").textContent = data["resume_results"]["tt_loss_call"];
        // put
        document.querySelector(".card-result-extrato-win-put").textContent = data["resume_results"]["tt_win_put"];
        document.querySelector(".card-result-extrato-loss-put").textContent = data["resume_results"]["tt_loss_put"];
        
        // ------------------------- CREATE TABLE RESULTS -------------------------
        let data_results = JSON.parse(data["data"]);
        document.querySelector(".table-results-resume tbody").remove()
        document.querySelector(".table-results-resume").innerHTML += `<tbody></tbody>`;
        let table_results = document.querySelector(".table-results-resume tbody");
        let cont = 0;
        for (let data_idx in data_results) {
            table_results.innerHTML += `
                <tr>
                    <td class="result-comum">${data_idx}</td>

                    <td class="result-comum resume-operation">
                        <p class="result-data-${cont}" onmouseover="MouseMoveOver(event);" onmouseout="MouseMoveOut(event);">${data_results[data_idx]["expiration_alert"]}</p>
                        
                        <span class="resume-operation-alert result-${cont}">
                            <p class="destaque-expiration">${data_results[data_idx]["expiration_alert"]}</p>
                            <div class="content-destaque-expirations">
                                <p>início:</p> <p> ${data_results[data_idx]["alert_datetime"]}</p>
                            </div>
                            <div class="content-destaque-expirations">
                                <p>confir.:</p> <p> ${data_results[data_idx]["alert_time_update"]}</p>
                            </div>
                        </span>
                    </td>

                    <td class="result-comum">${data_results[data_idx]["padrao"]}</td>
                    <td class="result-comum">${data_results[data_idx]["status_alert"]}</td>
                    <td class="result-comum">${data_results[data_idx]["mercado"]}</td>
                    <td class="result-comum">${data_results[data_idx]["active"]}</td>
                    <td class="${data_results[data_idx]["className_direction"]}">${data_results[data_idx]["direction"]}</td>
                    <td class="${data_results[data_idx]["class_name"]}">${data_results[data_idx]["resultado"]}</td>

                    <td class="result-comum">${data_results[data_idx]["sup_m15"]}</td>
                    <td class="result-comum">${data_results[data_idx]["sup_1h"]}</td>
                    <td class="result-comum">${data_results[data_idx]["sup_4h"]}</td>
                    <td class="result-comum">${data_results[data_idx]["res_m15"]}</td>
                    <td class="result-comum">${data_results[data_idx]["res_1h"]}</td>
                    <td class="result-comum">${data_results[data_idx]["res_4h"]}</td>
                </tr>
            `;
            cont = cont +1;

        }
    })
}

function MouseMoveOver(event) {
    let classNameTarget = event.target.className.split("-");
    let classNameEdit = classNameTarget[0] + "-" + classNameTarget[2];
    const x = event.clientX;
    const y = event.clientY;
    document.querySelector(`.${classNameEdit}`).style.display = "flex";
    document.querySelector(`.${classNameEdit}`).style.top = `${y-60}px`;
}
function MouseMoveOut(event) {
    let classNameTarget = event.target.className.split("-");
    let classNameEdit = classNameTarget[0] + "-" + classNameTarget[2];
    const x = event.clientX;
    const y = event.clientY;
    document.querySelector(`.${classNameEdit}`).style.display = "none";
    // document.querySelector(".resume-operation-alert ").style.display = "none";
}