function showlogin(){
    document.getElementById("signupform").style.display = "none";
    document.getElementById("loginform").style.display = "flex";
    document.getElementById("loginbtn").style.backgroundColor = "#282828";
    document.getElementById("loginbtn").style.color = "white";
    document.getElementById("signupbtn").style.backgroundColor = "white";
    document.getElementById("signupbtn").style.color = "#282828";
    document.getElementById("signupbtn").style.border = "solid 2px #282828";



}

function showsignup(){
    document.getElementById("loginform").style.display = "none";
    document.getElementById("signupform").style.display = "flex";
    document.getElementById("signupbtn").style.backgroundColor = "#282828";
    document.getElementById("signupbtn").style.color = "white";
    document.getElementById("loginbtn").style.backgroundColor = "white";
    document.getElementById("loginbtn").style.color = "#282828";
    document.getElementById("loginbtn").style.border = "solid 2px #282828";



}


document.querySelectorAll('[onclick]').forEach(function(element) {
    element.style.cursor = 'pointer';
});

showlogin()