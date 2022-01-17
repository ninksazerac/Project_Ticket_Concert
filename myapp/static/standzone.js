const form=document.getElementById('form');
const standzonejs=document.getElementById('zone');
const full_namejs=document.getElementById('full_name');
const seat=document.getElementById('seat');

form.addEventListener('submit',function(e){
    e.preventDefault();
    if(full_namejs.value=== ''){
        showerror(full_name,'Please enter your name');
    }
    else {
        showsuccess(full_name);
        let data = new FormData(); // 2
        data.append("full_name", full_namejs.value)
        data.append("seat", seat.value)
        data.append("zone", standzonejs.value)
        data.append("csrfmiddlewaretoken", '{{csrf_token}}')
        axios.post('addreserve', data)// 4

         .then(res => location.href='payment') // 5
         .catch(errors => console.log(errors)) // 6
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