// https://www.w3schools.com/howto/howto_js_responsive_navbar_dropdown.asp
// https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_responsive_navbar_dropdown

function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}