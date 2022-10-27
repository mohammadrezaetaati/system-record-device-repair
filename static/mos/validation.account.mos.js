let mainForm = document.querySelector('#signup_form');
let nameElm = document.querySelector('.mos-input #first_name');
let lastnameElm = document.querySelector('.mos-input #last_name')
let usernameElm = document.querySelector('.mos-input #username');
let passwordElm = document.querySelector('.mos-input #password');
let repasswordElm = document.querySelector('.mos-input #re_password');


mainForm.onsubmit = (e) => {
    e.preventDefault();
    if (nameElm.value.length <= 0) {
        document.querySelector('input#first_name + .mos-alert').classList.add('active');
    }
    if (lastnameElm.value.length <= 0) {
        document.querySelector('input#last_name + .mos-alert').classList.add('active');
    }
    if (usernameElm.value.length <= 0) {
        document.querySelector('input#username + .mos-alert').classList.add('active');
    }
}


