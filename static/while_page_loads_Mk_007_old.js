// https://www.w3schools.com/js/js_htmldom_eventlistener.asp
// https://www.w3schools.com/js/tryit.asp?filename=tryjs_addeventlistener_displaydate

function submit_inflation_seeds() {



    // Put user's selection (or non-selection) for inflation year in a variable
    let year = document.getElementById("year_mk_008");

    // Display an alert popup window with an error message if user did not select an inflation year
    if (year.value == "") {

        // Show user an error message in a popup window
        alert("Please select an inflation year.");

        return false;
    }

    // Put user's selection (or non-selection) for inflation month in a variable
    let month = document.getElementById("month_mk_008");

    // Display an alert popup window with an error message if user did not select an inflation month
    if (month.value == "") {

        // Show user an error message in a popup window
        alert("Please select an inflation month.");

        return false;
    }

    // Put each element that has the "spinner" id in an array-like list of HTML elements
    const spinner = document.getElementById("spinner_wrapper");

    // Get the properties of the element after it has been styled by cascading style sheets
    const spinner_css_object = window.getComputedStyle(spinner, null)

    // If the spinner is not showing
    if (spinner_css_object.visibility === "hidden") {

        // Show the spinner
        spinner.style.visibility = "visible"

    // Put the inflation year and inflation month in JSON format
    let inflation_seeds = {
      year: year.value,
      month: month.value
    };

    // Send the inflation year and inflation month to the web server via a POST request
    fetch(`${window.origin}/console_release_prices_test`, {

        method: "POST",

        credentials: "include",

        body: JSON.stringify(inflation_seeds),

        cache: "no-cache",

        headers: new Headers({

            "content-type": "application/json"

        })
    })

    .then(function (response) {

        if (response.status !== 200) {

            console.log(`Looks like there was a problem. Status code: ${response.status}`);

            return;

        }

        response.json().then(function (data) {

        // Get a counting variable
        let i;

        // let destination;

        // Populate put inflation-adjusted prices in the table
        for (i = 0; i < data.length; i++) {

            // document.getElementById("Xbox").innerHTML = "data[" + i +"]: " + data[i].console_name_underscored;
            document.getElementById(data[i].console_name_underscored).innerHTML = data[i].inflation_answer;

        }

        // Put each element that has the "inflation_adjusted_price_cell" class in an array-like list of HTML elements
        let inflation_adjusted_prices = document.getElementsByClassName("inflation_adjusted_price_cell");

        // Get a counting variable for the upcoming for loop
        let j;

        // Reveal the column of cells that holds the inflation-adjusted prices
        for (j = 0; j < inflation_adjusted_prices.length; j++) {

            // Reveal the cell that holds an inflation-adjusted-price
            inflation_adjusted_prices[j].style.display = "table-cell";

        }

    });
    })

    .catch(function (error) {
    console.log("Fetch error: " + error);
    });

//     fetch(`${window.origin}/console_release_prices_test`, {
//       method: "POST",
//       credentials: "include",
//       body: JSON.stringify(inflation_seeds),
//       cache: "no-cache",
//       headers: new Headers({
//         "content-type": "application/json"
//       })
//     })
//       .then(function (response) {
//         if (response.status !== 200) {
//           console.log(`Looks like there was a problem. Status code: ${response.status}`);
//           return;
//         }
//         // response.json().then(function (data) {
//         //   console.log(data);
//         // });
//         response.json().then(function (data) {
//         //   document.getElementById("search_output_001").innerHTML = "Found " + data[0].company + " cells in the table's first row";

//           let i;

//             for (i = 0; i < data.length; i++) {

//                 document.getElementById("search_output_001").innerHTML = "data[" + i +"]: " + data[i].console_name;

//                 // setTimeout(function(), 1000);

//                 // (function(i) {

//                 //     setTimeout(function() {

//                 //          document.getElementById("search_output_001").innerHTML = "data[" + i +"]: " + data[i].console_name;

//                 //     }, 2000);

//                 // }(i));
//           }

// // var s = document.getElementById("div1");
// // for (i = 0; i < 10; i++) {

// //   // create a closure to preserve the value of "i"
// //   (function(i){

// //     window.setTimeout(function(){
// //       s.innerHTML = s.innerHTML + i.toString();
// //     }, i * 2000);

// //   }(i));

// // }

//         });
//       })
//       .catch(function (error) {
//         console.log("Fetch error: " + error);
//       });

    // Hide the spinner
    spinner.style.visibility = "hidden"

}

function show_hide_spinner() {

    // Put each element that has the "spinner" id in an array-like list of HTML elements
    const spinner = document.getElementById("spinner_wrapper");

    // Get the properties of the element after it has been styled by cascading style sheets
    const spinner_css_object = window.getComputedStyle(spinner, null)

    // If the spinner is not showing
    if (spinner_css_object.visibility === "hidden") {

        // Show the spinner
        spinner.style.visibility = "visible"

    // In any other scenario
    } else {

        // Hide the spinner
        spinner.style.visibility = "hidden"
    }

    // // If the spinner is not showing
    // if (spinner.style.visibility === "hidden") {

    //     // Show the spinner
    //     spinner.style.visibility = "visible"

    // // In any other scenario
    // } else {

    //     // Hide the spinner
    //     spinner.style.visibility = "hidden"
    // }

}

// function submit_inflation_seeds() {

//     var name = document.getElementById("name");
//     var message = document.getElementById("message");

//     var inflation_seeds = {
//       name: name.value,
//       message: message.value
//     };

//     fetch(`${window.origin}/console_release_prices_test`, {
//       method: "POST",
//       credentials: "include",
//       body: JSON.stringify(inflation_seeds),
//       cache: "no-cache",
//       headers: new Headers({
//         "content-type": "application/json"
//       })
//     })
//       .then(function (response) {
//         if (response.status !== 200) {
//           console.log(`Looks like there was a problem. Status code: ${response.status}`);
//           return;
//         }
//         // response.json().then(function (data) {
//         //   console.log(data);
//         // });
//         response.json().then(function (data) {
//           document.getElementById("search_output_001").innerHTML = "Found " + data.message + " cells in the table's first row";
//         });
//       })
//       .catch(function (error) {
//         console.log("Fetch error: " + error);
//       });
// }

function submit_message() {

    var name = document.getElementById("name");
    var message = document.getElementById("message");

    var entry = {
      name: name.value,
      message: message.value
    };

    fetch(`${window.origin}/console_release_prices_test`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(entry),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
      .then(function (response) {
        if (response.status !== 200) {
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(function (data) {
          console.log(data);
        });
      })
      .catch(function (error) {
        console.log("Fetch error: " + error);
      });
}


// function submit_inflation_seeds() {

//     let year = document.getElementById("year_mk_007").value;
//     let month = document.getElementById("month_mk_007").value;

//     var inflation_seeds = {

//         // Year for the inflation calculation
//         year: year.value,

//         // Month for the inflation calculation
//         month: month.value
//     };

//     fetch(`${window.origin}/console_release_prices_test`, {
//       method: "POST",
//       credentials: "include",
//       body: JSON.stringify(inflation_seeds),
//       cache: "no-cache",
//       headers: new Headers({
//         "content-type": "application/json"
//       })
//     })
//       .then(function (response) {
//         if (response.status !== 200) {
//           console.log(`Looks like there was a problem. Status code: ${response.status}`);
//           return;
//         }
//         response.json().then(function (data) {
//           console.log(data);
//         });
//       })
//       .catch(function (error) {
//         console.log("Fetch error: " + error);
//       });

//     // Start the loading spinner

//     // Send asynchronous request to server

//     // Get response from server

//     // Stop the loading spinner

//     // Update table on page

//     // Submbit the form
//     // document.getElementById("javascript_submission_test").submit();

// }


// function loading_mk_007() {

//     // Put user's selection (or non-selection) for inflation year in a variable
//     // let year = document.forms["form_loading_mk_007"]["year"].value;
//     let year = document.getElementById("year_mk_007").value;
//     // var year = document.getElementById("year_mk_007").value;

//     // Display an alert popup window with an error message if user did not select an inflation year
//     if (year == "") {

//         // Show user an error message in a popup window
//         alert("Please select an inflation year. [//loading_mk_007//]");

//         return false;
//     }

//     // Put user's selection (or non-selection) for inflation month in a variable
//     // let month = document.forms["form_loading_mk_007"]["month"].value;
//     let month = document.getElementById("month_mk_007").value;
//     // var month = document.getElementById("month_mk_007").value;

//     // Display an alert popup window with an error message if user did not select an inflation month
//     if (month == "") {

//         // Show user an error message in a popup window
//         alert("Please select an inflation month. [//loading_mk_007//]");

//         return false;
//     }

//     // https://pythonise.com/series/learning-flask/flask-and-fetch-api

//     function submit_inflation_seeds() {

//         let year = document.getElementById("year_mk_007").value;
//         let month = document.getElementById("month_mk_007").value;

//         var inflation_seeds = {

//             // Year for the inflation calculation
//             year: year.value,

//             // Month for the inflation calculation
//             month: month.value
//         };

//         fetch(`${window.origin}/console_release_prices_test`, {
//           method: "POST",
//           credentials: "include",
//           body: JSON.stringify(inflation_seeds),
//           cache: "no-cache",
//           headers: new Headers({
//             "content-type": "application/json"
//           })
//         })
//           .then(function (response) {
//             if (response.status !== 200) {
//               console.log(`Looks like there was a problem. Status code: ${response.status}`);
//               return;
//             }
//             response.json().then(function (data) {
//               console.log(data);
//             });
//           })
//           .catch(function (error) {
//             console.log("Fetch error: " + error);
//           });

//     // Start the loading spinner

//     // Send asynchronous request to server

//     // Get response from server

//     // Stop the loading spinner

//     // Update table on page

//     // Submbit the form
//     // document.getElementById("javascript_submission_test").submit();

// }

// }