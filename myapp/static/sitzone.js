const form=document.getElementById('form');
const sitzone2=document.getElementById('zone');
const seat2=document.getElementById('seat');
const full_namejs = document.getElementById('full_name');





//check ว่า data เท่ากับ ''  ?
form.addEventListener('submit',function(e){
    e.preventDefault();

    

    if(seat2.value=== ''){
        showerror(seat2,'Please enter your seat');
    }
    
    else if(full_namejs.value=== ''){
        showerror(full_namejs,'Please enter your name');
    }
    
    else if(full_namejs.value=== '' && seat2.value=== ''){
        showerror(full_namejs,'Please enter your name');
    } 
    else{
            

            // send data to view.py (addsitzone) 
            let data = new FormData(); // 2
            data.append("full_name", full_namejs.value)
            data.append("seat", seat2.value)
            data.append("zone", sitzone2.value)
            data.append("csrfmiddlewaretoken", '{{csrf_token}}')
            axios.post('addreserve', data)// 4
            
            .then(res => location.href = 'payment') // 5
            .catch(errors => console.log(errors)) 
            
        }
        


    });
    
function showerror(input,message){
    const formControl=input.parentElement;
    formControl.className='form-control error';
    const small=formControl.querySelector('small');
    small.innerText=message;
}


function showsuccess(input){
    const formControl=input.parentElement;
    formControl.className='form-control success';
}


// function postAdd() {
//   var xhttp = new XMLHttpRequest();
//   xhttp.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//       document.getElementById('full_name').innerHTML = this.responseText;
//         // document.getElementById('full_name').innerHTML = this.responseText;
//     }
//   };
//   xhttp.open('POST', 'addsitzone', true);
//   xhttp.setRequestHeader("Content-type",'application/json');
//   xhttp.send
  // xhttp.send(JSON.stringify({
  //     name: "Deska",
  //     email: "deska@gmail.com",
  //     phone: "342234553"
  //   }));



  // xhr.send(JSON.stringify({
  //   name: "Deska",
  //   email: "deska@gmail.com",
  //   phone: "342234553"
  // }));
  // xhr.onload = function() {
  //     var data = JSON.parse(this.responseText);
  //     console.log(data);
  // };

// }

// $(document).ready(function() {
//   $.ajax({
//       method: 'POST',
//       url: 'add',
//       data: {'full_name': full_name},
      // success: function (data) {
      //      //this gets called when server returns an OK response
      //      alert("it worked!");
      // },
      // error: function (data) {
      //      alert("it didnt work");
      // }
//   });
// });


// post('addsitzone', {full_name: "wtf"});

// function post(path, params, method='post') {

//     const form = document.createElement('form');
//     form.method = method;
//     form.action = path;
  
//     for (const key in params) {
//       if (params.hasOwnProperty(key)) {
//         const hiddenField = document.createElement('input');
//         hiddenField.type = 'hidden';
//         hiddenField.name = key;
//         hiddenField.value = params[key];
  
//         form.appendChild(hiddenField);
//       }
//     }
  
//     document.body.appendChild(form);
//     form.submit();
//   }

// let xhr = new XMLHttpRequest();
  
// // open() method to pass request
// // type, url and async true/false 
// xhr.open('GET',
//     'http://127.0.0.1:8000/addsitzone', true);
// let userinfo = {
//     'full_name' : full_name,
//     }    
// // onload function to get data 
// xhr.onload = function () {
//     if (this.status === 200) {
//         console.log(JSON.stringify(userinfo));
//     }
// }
  
// // Send function to send data
// xhr.send()
  

