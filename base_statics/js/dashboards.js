Chart.defaults.font.size = 16;
Chart.defaults.font.family = "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif";
var dash_1;
var dash_2;
function createDashboardResults(list_hours, list_results_win, list_results_loss, tt_win, tt_loss){
    const ctx = document.getElementById('myChart');
    const ctx_2 = document.getElementById('myChart-2');
    try {dash_1.destroy();} catch (error) {}
    try {dash_2.destroy();} catch (error) {}

    let data = {
        datasets: [{
            type: 'bar',
            label: 'win',
            data: list_results_win,
            backgroundColor: '#00ff0d',
        }, {
            type: 'bar',
            label: 'loss',
            data: list_results_loss,
            backgroundColor: '#ff0000',
        }],
        labels: list_hours
    }
    let data_2 = {
        labels: ["win", "loss"],
        datasets: [{
            type: 'doughnut',
            data: [tt_win, tt_loss],
            backgroundColor: [
                '#00ff0d','#ff0000'
            ],
        }],
    }

    // ------------------------------
    dash_1 = new Chart(ctx, {
        data: data,
        options: {
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                }
            },
        },
    });
    dash_2 = new Chart(ctx_2, {
        type: 'doughnut',
        data: data_2,
    });
}


// --------------------------
function compareNumbers(a, b) {
    return a - b;
}
  
function prepareDataToDashboard(obj_results){
    let lista_horarios = [];
    const PromisseA = new Promise((resolve, reject)=>{
        
        let tt_win = 0;
        let tt_loss = 0;
        let obj_results_final = {};
        for (i=0; i < obj_results.length; i++){
            if (obj_results[i]["result"] == "win"){
                tt_win = tt_win +1;
            }
            else if (obj_results[i]["result"] == "loss"){
                tt_loss = tt_loss +1;
            }
            // ------------------------------------------------------
            if (!lista_horarios.includes(obj_results[i]["hora"])){
                lista_horarios.push(obj_results[i]["hora"]);
                if (obj_results[i]["result"] == "win"){
                    obj_results_final[`${obj_results[i]["hora"]}`] = {"win":1, "loss":0};
                } else {
                    obj_results_final[`${obj_results[i]["hora"]}`] = {"win":0, "loss":1};
                }
            } else {
                try {
                    if (obj_results[i]["result"] == "win"){
                        obj_results_final[`${obj_results[i]["hora"]}`]["win"] =  obj_results_final[`${obj_results[i]["hora"]}`]["win"] +1;
                    } else if (obj_results[i]["result"] == "loss") {
                        obj_results_final[`${obj_results[i]["hora"]}`]["loss"] =  obj_results_final[`${obj_results[i]["hora"]}`]["loss"] +1;
                    }
                } catch (error){
                    console.log(error)
                }
            }
        }
        // ------------------------------------------------------
        let list_results_win = [];
        let list_results_loss = []
        for (let i in obj_results_final){
            // soma +0 para caso não exita win ou loss para o horário atual do loop.
            list_results_win.push(obj_results_final[i]["win"] +0);
            list_results_loss.push(obj_results_final[i]["loss"] +0);
        }
        obj_results_final["tt_win"] = tt_win;
        obj_results_final["tt_loss"] = tt_loss;
        obj_results_final["list_results_win"] = list_results_win;
        obj_results_final["list_results_loss"] = list_results_loss;
        obj_results_final["horarios"] = lista_horarios.sort(compareNumbers)
        resolve(obj_results_final)
    })
    
    PromisseA.then((obj_results_final)=>{
        return {
            "horario": obj_results_final["horarios"],
            "list_results_win": obj_results_final["list_results_win"],
            "list_results_loss": obj_results_final["list_results_loss"],
            "tt_win": obj_results_final["tt_win"],
            "tt_loss": obj_results_final["tt_loss"],
        }
    }).then((data_process)=>{
        createDashboardResults(
            data_process["horario"],
            data_process["list_results_win"],
            data_process["list_results_loss"],
            data_process["tt_win"],
            data_process["tt_loss"]
        )
    })
}