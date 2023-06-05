// console.log("control_api.js carregado...");

let status_api = document.getElementById("status-api");
for (let i=0; i < status_api.options.length; i++){
    if (status_api.className == status_api.options[i].value) {
        status_api.options[i].selected = true;
    } else {
        status_api.options[i].selected = false;
    }
}
// 
function controlAPI(url_start_api, url_stop_api) {
    //
    let control_form_email = false;
    let control_form_password = false;
    let control_form_status = false;
    // let btn_status_api = document.getElementById("save-form-control-api");
    let form = document.getElementById("form-config-admin-auth");
    form.addEventListener("submit", (event) =>{
        event.preventDefault();
    });
    let status_api = document.getElementById("status-api");
    let username_iqoption = document.getElementById("username-iqoption");
    let password_iqoption = document.getElementById("password-iqoption");
    
    if ( username_iqoption.value.length >= 18 & username_iqoption.value.length <= 60) {
        if(username_iqoption.value.slice(username_iqoption.value.length-4) == ".com") {
            // console.log(username_iqoption.value.slice(username_iqoption.value.length-4));
            control_form_email = true;
        } else if (username_iqoption.value.slice(username_iqoption.value.length-7) == ".com.br" ) {
            console.log(username_iqoption.value.slice(username_iqoption.value.length-7));
            control_form_email = true;
        }
    }
    if ( password_iqoption.value.length >= 5 & password_iqoption.value.length <= 25) {
        control_form_password = true;
    }
    if (status_api.value == 0 || status_api.value == 1) {
        control_form_status = true;
    }
    
    // ---------------------------------------
    if (control_form_email == false) {
        username_iqoption.classList.add("border-erro-input");
        username_iqoption.classList.remove("border-success-input");
    } else {
        username_iqoption.classList.add("border-success-input");
        username_iqoption.classList.remove("border-erro-input");
    }
    // ---------------------------------------
    if (control_form_password == false) {
        password_iqoption.classList.add("border-erro-input");
        password_iqoption.classList.remove("border-success-input");
    } else {
        password_iqoption.classList.add("border-success-input");
        password_iqoption.classList.remove("border-erro-input");
    }

    let body = {
        "status_api": status_api.value,
        "email": username_iqoption.value,
        "password": password_iqoption.value,
    }
    if (control_form_email == true & control_form_password == true & control_form_status == true) {
        if (status_api.value == 1) {
            fetch(url_start_api, {
                method: "POST",
                body: JSON.stringify(body)
            }).then((data) =>{
                return data.json();
            }).then((data)=> {
                // console.log(data)
                if(data["code"] == 200){
                    document.querySelector(".msg-control-status-api").style.display = "flex";
                    document.querySelector(".msg-control-success-start").style.display = "flex";
                    setTimeout(()=>{
                        document.querySelector(".msg-control-status-api").style.display = "none";
                        document.querySelector(".msg-control-success-start").style.display = "none";
                    }, 3000);
                }
                else {
                    document.querySelector(".msg-control-status-api").style.display = "flex";
                    document.querySelector(".msg-control-error-start").style.display = "flex";
                    setTimeout(()=>{
                        document.querySelector(".msg-control-status-api").style.display = "none";
                        document.querySelector(".msg-control-error-start").style.display = "none";
                    }, 3000);
                }
            });
        }
        else if (status_api.value == 0) {
            fetch(url_stop_api, {
                method: "POST",
                body: JSON.stringify(body)
            }).then((data) =>{
                return data.json();
            }).then((data)=>{
                // console.log(data)
                document.querySelector(".msg-control-status-api").style.display = "flex";
                document.querySelector(".msg-control-save-sucess").style.display = "flex";
                setTimeout(()=>{
                    document.querySelector(".msg-control-status-api").style.display = "none";
                    document.querySelector(".msg-control-save-sucess").style.display = "none";
                }, 3000);
            });
        }
    }
}
// 
function alterSelectInputs(event) {
    let input_select = document.getElementById(event.target.id);
    // console.log(input_select.value);
    if (input_select.value == 1) {
        let inputs = document.querySelector(".inputs-credencials-user-iqoption-password");
        inputs.style.display = "flex";
    } else {
        let inputs = document.querySelector(".inputs-credencials-user-iqoption-password");
        inputs.style.display = "none";
    }
}
// 
function showInpuPassword(event){
    let inputs = document.querySelector(".inputs-credencials-user-iqoption-password");
    inputs.style.display = "flex";
}

// 
function show_password(event) {
    let icon_password = document.getElementById("password-iqoption");
    let name_class = event.target.classList;
    console.log(name_class);
    console.log(name_class[1]);
    console.log(icon_password);
    if (name_class[1] == "fa-lock") {
        icon_password.setAttribute("type", "text");
        document.querySelector(".icons-password i").classList.add("fa-unlock");
        document.querySelector(".icons-password i").classList.remove("fa-lock");
    }
    else if (name_class[1] == "fa-unlock") {
        icon_password.setAttribute("type", "password");
        document.querySelector(".icons-password i").classList.add("fa-lock");
        document.querySelector(".icons-password i").classList.remove("fa-unlock");
    }
}