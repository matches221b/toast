// http://jsfiddle.net/7BUmG/2/
// var $rows = $('#table tr');
// $('#search').keyup(function() {
//     var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();

//     $rows.show().filter(function() {
//         var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
//         return !~text.indexOf(val);
//     }).hide();
// });

// http://jsfiddle.net/dfsq/7BUmG/1133/
// var $rows = $('#release_price_table tr');
// $('#search').keyup(function() {

//     var val = '^(?=.*\\b' + $.trim($(this).val()).split(/\s+/).join('\\b)(?=.*\\b') + ').*$',
//         reg = RegExp(val, 'i'),
//         text;

//     $rows.show().filter(function() {
//         text = $(this).text().replace(/\s+/g, ' ');
//         return !reg.test(text);
//     }).hide();
// });

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