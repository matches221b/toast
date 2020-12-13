// https://www.tutorialrepublic.com/codelab.php?topic=faq&file=make-bootstrap-dropdown-menu-on-hover
// https://www.tutorialrepublic.com/faq/how-to-open-bootstrap-dropdown-menu-on-hover-rather-than-click.php

$(document).ready(function(){
    $(".dropdown").hover(function(){
        var dropdownMenu = $(this).children(".dropdown-menu");
        if(dropdownMenu.is(":visible")){
            dropdownMenu.parent().toggleClass("open");
        }
    });
});