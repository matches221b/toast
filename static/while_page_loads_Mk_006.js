// https://www.w3schools.com/js/js_htmldom_eventlistener.asp
// https://www.w3schools.com/js/tryit.asp?filename=tryjs_addeventlistener_displaydate

function loading_mk_006() {

    // Put user's selection (or non-selection) for inflation year in a variable
    const year = document.forms["form_loading_mk_006"]["year"].value;

    // Display an alert popup window with an error message if user did not select an inflation year
    if (year == "") {

        // Show user an error message in a popup window
        alert("Please select an inflation year.");

        return false;
    }

    // Put user's selection (or non-selection) for inflation month in a variable
    const month = document.forms["form_loading_mk_006"]["month"].value;

    // Display an alert popup window with an error message if user did not select an inflation month
    if (month == "") {

        // Show user an error message in a popup window
        alert("Please select an inflation month.");

        return false;
    }

    // Start the loading spinner

    // Send asynchronous request to server

    // Get response from server

    // Stop the loading spinner

    // Update table on page

    // Submbit the form
    // document.getElementById("javascript_submission_test").submit();

}