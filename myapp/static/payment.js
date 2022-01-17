document.getElementById("submit").addEventListener("click", function (event) {
    event.preventDefault();

    checkData();
});


var full_name = document.getElementById("full_name");
var email = document.getElementById("email");
var phone_number = document.getElementById("phone_number");
var seat = document.getElementById("seat");
var zone = document.getElementById("zone");

function checkData() {
    var full_nameValue = full_name.value.trim();
    var emailValue = email.value.trim();
    var phone_numberValue = phone_number.value.trim();
    var seatValue = seat.value.trim();
    var zoneValue = zone.value.trim();


    if (full_nameValue == "") {
        setError(full_name, "Full name can't be blank");
    }
    else {
        setSuccess(full_name);
    }
    
    if (emailValue == "") {
        setError(email, "Email can't be blank");
    }
    else if (!isEmail(emailValue)) {
        setError(email, "Email is not Valid");
    }
    else {
        setSuccess(email);
    }



    if (phone_numberValue == "") {
        setError(phone_number, "Phone number can't be blank");
    }
    else {
        setSuccess(phone_number);
    }


   

    if ((full_nameValue != "") && (emailValue != "") && (isEmail(emailValue)) && (phone_numberValue != "") ){
        let data = new FormData(); // 2
        data.append("full_name", full_name.value)
        data.append("seat", seat.value)
        data.append("zone", zone.value)
        data.append("csrfmiddlewaretoken", '{{csrf_token}}')

        axios.post('addpayment', data)// 4

            .then(res => location.href = 'paymentbill') // 5
            .catch(errors => console.log(errors)) 
    }

}


function setError(u, msg) {
    var parentBox = u.parentElement;
    parentBox.className = "input-field error";
    var span = parentBox.querySelector("span");
    span.innerText = msg;
}

function setSuccess(u) {
    var parentBox = u.parentElement;
    parentBox.className = "input-field success";
}

function isEmail(e) {
    var reg = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return reg.test(e);
}