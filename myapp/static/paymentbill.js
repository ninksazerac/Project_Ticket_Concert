const form=document.getElementById('form');

const file=document.getElementById('file');


form.addEventListener('submit',function(e){
    e.preventDefault();
    if(file.value=== ''){
        showerror(file,'Please choose file');
    }else{
        showsuccess(file);
        window.location.replace('success');
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