document.addEventListener("DOMContentLoaded", function () {
    // Show the default page (Dashboard)
    showPage('dashboard');
});

function showPage(pageId,id) {
    // Hide all pages
    let pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    let btn1 =  document.querySelectorAll(".sid");
    btn1.forEach(btn1 => btn1.classList.remove('active-btn'));

    // Show the selected page
    let selectedPage = document.getElementById(pageId);
    selectedPage.classList.add('active');
    let btn =  document.getElementById(id);
    btn.classList.add('active-btn')
}


// function showorderdetails(pageid,id){
//     let pages = document.querySelectorAll('.page');
//     pages.forEach(page => page.classList.remove('active'));
//     let btn1 =  document.querySelectorAll(".sid");
//     btn1.forEach(btn1 => btn1.classList.remove('active-btn'));


//     let selectedPage = document.getElementById(pageid);
//     selectedPage.classList.add('active');
//     let btn =  document.getElementById(id);
//     btn.classList.add('active-btn')
// }

