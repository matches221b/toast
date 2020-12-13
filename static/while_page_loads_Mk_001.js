// Javascript file to help with having a spinner after user clicks form submit button
// https://medium.com/@ludwig.stumpp/part-2-how-to-build-a-web-form-with-a-loading-animation-using-html5-css3-jquery-8328ff87e769

// $(document).ready(function() {
//   const lockModal = $("#lock-modal");
//   const loadingCircle = $("#loading-circle");
//   const form = $("#my-form");


//   form.on('submit', function(e) {
//     e.preventDefault(); //prevent form from submitting

//     const firstname = $("input[name=user_firstname]").val();
//     const lastname = $("input[name=user_lastname]").val();

//     // lock down the form
//     lockModal.css("display", "block");
//     loadingCircle.css("display", "block");

//     form.children("input").each(function() {
//       $(this).attr("readonly", true);
//     });


//     // setTimeout(function() {
//     //   // re-enable the form
//     //   lockModal.css("display", "none");
//     //   loadingCircle.css("display", "none");

//     //   form.children("input").each(function() {
//     //     $(this).attr("readonly", false);
//     //   });

//     //   // form.append(`<p>Thanks ${firstname} ${lastname}!</p>`);
//     // }, 100);


//   });

// });


$(document).ready(function() {
  const lockModal = $("#lock-modal");
  const loadingCircle = $("#loading-circle");
  const form = $("#my-form");


  form.on('submit', function(e) {
    e.preventDefault(); //prevent form from submitting

    const firstname = $("input[name=user_firstname]").val();
    const lastname = $("input[name=user_lastname]").val();

    // lock down the form
    lockModal.css("display", "block");
    loadingCircle.css("display", "block");

    form.children("input").each(function() {
      $(this).attr("readonly", true);
    });


  });

});