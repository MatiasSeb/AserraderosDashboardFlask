var pwd = document.getElementById("pwd");
var c_pwd = document.getElementById("c_pwd");

c_pwd.onkeyup = function() {
  if (pwd.value !== c_pwd.value) {
    c_pwd.setCustomValidity("Las contraseñas deben coincidir!");
  } else {
    c_pwd.setCustomValidity('');
  }
  c_pwd.reportValidity();
};

var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");

pwd.onkeyup = function() {
  var lowerCaseLetters = /[a-z]/g;
  if(pwd.value.match(lowerCaseLetters)) {  
    letter.classList.remove("text-danger");
    letter.classList.add("text-success");
  } else {
    letter.classList.remove("text-success");
    letter.classList.add("text-danger");
  }

  var upperCaseLetters = /[A-Z]/g;
  if(pwd.value.match(upperCaseLetters)) {  
    capital.classList.remove("text-danger");
    capital.classList.add("text-success");
  } else {
    capital.classList.remove("text-success");
    capital.classList.add("text-danger");
  }

  var numbers = /[0-9]/g;
  if(pwd.value.match(numbers)) {  
    number.classList.remove("text-danger");
    number.classList.add("text-success");
  } else {
    number.classList.remove("text-success");
    number.classList.add("text-danger");
  }

  if(pwd.value.length >= 8) {
    length.classList.remove("text-danger");
    length.classList.add("text-success");
  } else {
    length.classList.remove("text-success");
    length.classList.add("text-danger");
  }
  if(letter.classList.contains("invalid") || capital.classList.contains("invalid") || number.classList.contains("invalid") || length.classList.contains("invalid")) {
    pwd.setCustomValidity = "Tu contraseña no cumple con los requisitos.";
  } else {
    pwd.setCustomValidity = "La contraseña cumple con los requisitos.";
  }
  pwd.reportValidity();
}

