function createDashboardConfigVisaoGeral(url, estrategia) {
    // clearCanvas();
    let body = {
        "estrategia": estrategia,
    }
    fetch(url, {
        method: "POST",
        body: JSON.stringify(body)
    }).then((data)=>{
        return data.json();
    }).then((data)=>{
        let estrategia_filtrada = data["estrategia"];
        let obj_estrategia = `obj_${estrategia_filtrada}`
        document.querySelector(".block-table-config-visao-geral table tbody").remove();
        document.querySelector(".block-table-config-visao-geral table").innerHTML += "<tbody></tbody>"
        let btns_filtros = document.querySelectorAll(".filtros-visao-geral-config button");
        for (let btn in btns_filtros) {
            try {
                if (btns_filtros[btn].className.includes("btn-estrategia") & btns_filtros[btn].className.replace("btn-", "") == estrategia_filtrada) {
                    document.querySelector(`.${btns_filtros[btn].className}`).style.backgroundColor = "var(--color-dark-1)";
                } else {
                    document.querySelector(`.${btns_filtros[btn].className}`).style.backgroundColor = "var(--color-base-1)";
                }
            } catch (error) {}
        }
        
        let table_visao_geral = document.querySelector(".block-table-config-visao-geral table tbody");
        for (let registro in data[obj_estrategia]) {
            table_visao_geral.innerHTML += `
                <tr class="${estrategia_filtrada}-${registro}-tr">
                    
                    <td>
                        <span>
                            <p class="name-ative-header"> ${registro} <p/>
                        </span>
                    </td>
                    <td>
                        <span>
                            <input type="text" value="${data[obj_estrategia][registro]["candles_M5"]}" />
                        </span>
                    </td>
                    <td>
                        <span>
                            <input type="text" value="${data[obj_estrategia][registro]["sup_res_M15"]}" />
                        </span>
                    </td>
                    <td>
                        <span>
                            <input type="text" value="${data[obj_estrategia][registro]["sup_res_1H"]}" />
                        </span>
                    </td>
                    <td>
                        <span>
                            <input type="text" value="${data[obj_estrategia][registro]["sup_res_4H"]}" />
                        </span>
                    </td>

                    <td class="acoes-config-visao-geral">
                        <span>
                            <i class="fa-solid fa-pen-to-square" id="${estrategia_filtrada}-${registro}-edit"  onclick="edit_registro(event);"></i>
                        </span>

                        <span>
                            <i class="fa-solid fa-chart-simple"></i>
                        </span>

                        <span>
                            <i class="fa-solid fa-code-compare"></i>
                        </span>
                    
                    </td>
                </tr>
            `;
        };
        // createGraficosVisaoGeral();
        // createDashboardConfigVisaoGeral_2();
    })
}

function saveConfig(url, event) {
    let classNameEdit = event.target.id.replace("-edit", "");
    let split_class_name = classNameEdit.split("-");
    console.log(classNameEdit)
    let tr_registro = document.querySelectorAll(`.${classNameEdit}-tr td span input`);
    let candles_M5 =    parseInt(tr_registro[0].value);
    let sup_res_M15 =   parseInt(tr_registro[1].value);
    let sup_res_1H =    parseInt(tr_registro[2].value);
    let sup_res_4H =    parseInt(tr_registro[3].value);
    let estrategia = split_class_name[0];
    let name_active = null
    if ( split_class_name.includes("OTC")) {
        name_active = `${split_class_name[1]}-${split_class_name[2]}`
    } else {
        name_active = split_class_name[1]
    }
    let body = {
        "candles_M5": candles_M5,
        "sup_res_M15": sup_res_M15,
        "sup_res_1H": sup_res_1H,
        "sup_res_4H": sup_res_4H,
        "estrategia": estrategia,
        "active_name": name_active,
    }
    document.querySelector(".salvado-registro").style.display = "flex";
    fetch(url, {
        method: "POST",
        body: JSON.stringify(body)
    }).then((data)=>{
        return data.json();
    }).then((data)=>{
        // console.log(data);
        document.querySelector(".salvado-registro").style.display = "none";
        if (data["status_update"] == true){
            document.querySelector(".success-registro-salvo").style.display = "flex";
            setTimeout(()=>{
                document.querySelector(".success-registro-salvo").style.display = "none";
            }, 3000);
        } else {
            document.querySelector(".error-registro-salvo").style.display = "flex";
            setTimeout(()=>{
                document.querySelector(".error-registro-salvo").style.display = "none";
            }, 3000);
        }
    })
}

function testeBTN(){
    document.querySelector(".salvado-registro").style.display = "flex";
    setTimeout(()=>{
        document.querySelector(".salvado-registro").style.display = "none";
        document.querySelector(".error-registro-salvo").style.display = "flex";
    }, 3000);
    setTimeout(()=>{
        document.querySelector(".error-registro-salvo").style.display = "none";
        document.querySelector(".success-registro-salvo").style.display = "flex";
    }, 6000);
    setTimeout(()=>{
        document.querySelector(".success-registro-salvo").style.display = "none";
    }, 9000);

}
function clearCanvas(){
    let list_elementsCanvasContent =  [".dashboard-visao-geral-resultados-paridades-dash-1", ".dashboard-visao-geral-resultados-paridades-dash-2"];
    let list_elements_canvas = ["myChart", "myChart-2"]
    
    for (let e in list_elements_canvas){
        document.getElementById(list_elements_canvas[e]).remove();
    };
    setTimeout(()=>{
        for (let new_id in list_elements_canvas){
            document.querySelector(list_elementsCanvasContent[new_id]).innerHTML += `
                <canvas id="${list_elements_canvas[new_id]}"></canvas>
            `;
        }
    }, 3000);
}
function createGraficosVisaoGeral() {
    
    // dados de temporários
    let actives = [
        "AUDCAD", "AUDCAD-OTC", "AUDCHF", "AUDJPY", "AUDNZD", "AUDSGD", "AUDUSD", "CADCHF", "CADJPY", "CHFJPY", "CHFSGD", "EURAUD", "EURCAD", "EURCHF", "EURGBP", "EURGBP-OTC", "EURJPY", "EURJPY-OTC", "EURNOK", "EURNZD", "EURSGD", "EURUSD", "EURUSD-OTC", "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPJPY-OTC", "GBPNZD", "GBPUSD", "GBPUSD-OTC", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD", "NZDUSD-OTC", "USDCAD", "USDCHF", "USDCHF-OTC", "USDJPY", "USDJPY-OTC", "USDNOK"
    ]
    let results_actives_win = [
        10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 15, 16
    ]
    let results_actives_loss = [
        19, 4, 23, 2, 8, 19, 3, 13, 18, 2, 19, 4, 23, 2, 8, 19, 3, 13, 18, 2, 19, 4, 23, 2, 8, 19, 3, 13, 18, 2, 19, 4, 23, 2, 8, 19, 3, 13, 18, 2, 12, 3
    ]


    const ctx_2 = document.getElementById('myChart-2');

    const data_base = {
        labels: actives,
        datasets: [
            {
                label: 'Win',
                data: results_actives_win,
                backgroundColor: '#00ff0d',
            },
            {
            label: 'Loss',
            data: results_actives_loss,
            backgroundColor: '#ff0000',
            },
        ]
    };
    // 
    new Chart(ctx_2, {
        type: 'bar',
        data: data_base,
        options: {
        plugins: {
            title: {
            display: true,
            text: 'Resultado - WIN x LOSS (Hora)',
            font: {
                size: 15,
            }
            },
        },
        responsive: true,
        scales: {
            x: {
            stacked: true,
            },
            y: {
            stacked: true
            }
        }
        }
    });
}
function createDashboardConfigVisaoGeral_2() {
    const ctx = document.getElementById('myChart');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Estratégia 1', 'Estratégia 2', 'Estratégia 3', 'Estratégia 4', 'Estratégia 5'],
            datasets: [{
              label: 'Resultados - Estratégias',
              data: [12, 19, 3, 5],
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)'
                ],
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
}