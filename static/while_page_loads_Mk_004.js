// https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_loader5
// https://www.w3schools.com/howto/howto_css_loader.asp

var myVar;

function myFunction() {
  myVar = setTimeout(showPage, 3000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
}