// Javascript file to help with having a spinner after user clicks form submit button

function submit_function() {

    // Put user's selection (or non-selection) for inflation year in a variable
    var year = document.forms["javascript_submission_test"]["year"].value;

    // Display an alert popup window with an error message if user did not select an inflation year
    if (year == "") {

        // Show user an error message in a popup window
        alert("Please select an inflation year.");

        return false;
    }

    // Put user's selection (or non-selection) for inflation month in a variable
    var month = document.forms["javascript_submission_test"]["month"].value;

    // Display an alert popup window with an error message if user did not select an inflation month
    if (month == "") {

        // Show user an error message in a popup window
        alert("Please select an inflation month.");

        return false;
    }

    // Submbit the form
    document.getElementById("javascript_submission_test").submit();

    // Start the spinner

    

    // Stop the spinner


}