
function getData_Test(url, cookiesPost){
    let data_post = {
        "date_test": "test-post-temp",
        "X-CSRFToken": cookiesPost,
    }
    console.log("token --> ", data_post)
    fetch(url, {
        method: "POST",
        body: JSON.stringify(data_post),
        headers: {"X-CSRFToken": cookiesPost}
    }).then((data)=>{
        return data.json();
    }).then((data)=>{
        console.log(data)
        let table = document.querySelector(".table-results").getElementsByTagName("tbody")[0];
        // table.querySelector("tbody").remove();
        let newRow = table.insertRow().insertCell();
        // let newCell = newRow.insertCell();
        
        
        for (i in data){
            let newRow = table.insertRow();
            for (j in data[i]){
                let newCell = newRow.insertCell();
                newCell.append(document.createTextNode(data[i][j]));
                newCell.classList.add("class-test");
                newCell.innerHTML += `<span>teste</span>`;
                newCell.querySelector("span").style.color = "yellow";
            }
        }
    })
}