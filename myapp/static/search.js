const form = document.getElementById('form');
const zone = document.getElementById('zone');
const full_name = document.getElementById('full_name');


form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (full_name.value === '') {
        showerror(full_name, 'Please enter your name');
    }
    else {
        let data = new FormData(); // 2
        data.append("full_name", full_name.value)
        data.append("zone", zone.value)
        data.append("csrfmiddlewaretoken", '{{csrf_token}}')
        axios.post('search_user', data)
            .then(res => location.href = 'searchsuccess') // 5
            .catch(errors => console.log(errors))

    }
});




function showerror(input, message) {
    const formControl = input.parentElement;
    formControl.className = 'form-control error';
    const small = formControl.querySelector('small');
    small.innerText = message;
}


function showsuccess(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}