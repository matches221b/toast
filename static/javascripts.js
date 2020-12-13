
// https://www.w3schools.com/howto/howto_js_collapsible.asp
// Make content collapsible
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

// Global Search
// http://jsfiddle.net/dfsq/7BUmG/1133/
var $rows = $('#release_price_table tbody tr');
$('#search').keyup(function() {

    var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
        reg = RegExp(val, 'i'),
        text;

    $rows.show().filter(function() {
        text = $(this).text().replace(/\s+/g, ' ');
        return !reg.test(text);
    }).hide();
});

// https://www.w3schools.com/howto/howto_js_navbar_sticky.asp
// When the user scrolls the page, execute myFunction
// window.onscroll = function() {myFunction()};

// // Get the navbar
// var navbar = document.getElementById("navbar");

// // Get the offset position of the navbar
// var sticky = navbar.offsetTop;

// // Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function myFunction() {
//   if (window.pageYOffset >= sticky) {
//     navbar.classList.add("sticky")
//   } else {
//     navbar.classList.remove("sticky");
//   }
// }

// Function for sorting tables
// https://www.w3schools.com/howto/howto_js_sort_table.asp
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("myTable2");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

        function search_function_001() {

            const search_result = document.getElementById("laboratory_table").rows[0].cells.length;

            document.getElementById("search_output_001").innerHTML = "Found " + search_result + " cells in the table's first row"
        }

function search_function_002() {

    const search_result = document.getElementById("laboratory_table").rows[0].cells[0].innerHTML;

    document.getElementById("search_output_002").innerHTML = search_result
}

function search_function_003() {

    // Column header from table
    const column_header_text = document.getElementById("laboratory_table").rows[0].cells[4].innerHTML

    // Column that function should hide
    const target_column_text = "Release Price in";

    // Ascertain whether
    const comparison_output = column_header_text.includes(target_column_text)

    document.getElementById("search_output_003").innerHTML = comparison_output

}

function search_function_004() {

    // Put each element that has the "inflation_adjusted_price_cell" class in an array-like list of HTML elements
    const inflation_adjusted_prices = document.getElementsByClassName("inflation_adjusted_price_cell");

    // Get the number items in the array-like list of elements
    const item_count = inflation_adjusted_prices.length;

    // Output the number of items in the array-like list of elements
    document.getElementById("search_output_004").innerHTML = item_count
}

function search_function_005() {

    // Put each element that has the "inflation_adjusted_price_cell" class in an array-like list of HTML elements
    const inflation_adjusted_prices = document.getElementsByClassName("inflation_adjusted_price_cell");

    // Counting variable
    let i;

    // Iterate through each inflation-adjusted-price cell
    for (i = 0; i < inflation_adjusted_prices.length; i++) {

        // Set the background color of the ith inflation-adjusted-price cell
        inflation_adjusted_prices[i].style.backgroundColor = "red";
    }
}

function search_function_006() {

    // http://talkerscode.com/webtricks/show-hide-table-column-using-javascript.php

    // Put each element that has the "inflation_adjusted_price_cell" class in an array-like list of HTML elements
    const inflation_adjusted_prices = document.getElementsByClassName("inflation_adjusted_price_cell");

    // Counting variable
    let i;

    // Iterate through each inflation-adjusted-price cell
    for (i = 0; i < inflation_adjusted_prices.length; i++) {

        // Check whether the inflation-adjusted-price cell's diplay is "none"
        if (inflation_adjusted_prices[i].style.display === "none") {

            // Show the inflation-adjusted-price cell
            inflation_adjusted_prices[i].style.display = "table-cell";

        // In any other scenario . . .
        } else {

            // Hide the inflation-adjusted-price cell
            inflation_adjusted_prices[i].style.display = "none";
        }
    }
}

function spinner_function_001() {

    // // Put each element that has the "spinner" id in an array-like list of HTML elements
    const spinner = document.getElementById("spinner");

    // If the spinner is not showing
    if (spinner.style.display === "none") {

        // Show the spinner
        spinner.style.display = "block"

    // In any other scenario
    } else {

        // Hide the spinner
        spinner.style.display = "none"
    }
}

function spinner_function_002() {

    // // Put each element that has the "spinner" id in an array-like list of HTML elements
    const spinner = document.getElementById("spinner_wrapper");

    // If the spinner is not showing
    if (spinner.style.display === "none") {

        // Show the spinner
        spinner.style.display = "block"

    // In any other scenario
    } else {

        // Hide the spinner
        spinner.style.display = "none"
    }
}