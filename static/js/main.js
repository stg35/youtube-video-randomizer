$(document).ready(function(){
    $("#yes_no").click(function f(e) {
    e.preventDefault();
    $('#y').remove();
    var parent = $('#main');
    bt = document.createElement('bt');
    bt.innerHTML = '<form action="/" method="post">' +
        '<button type="submit" class="btn btn-primary">next</button>' +
        '</form>';
    parent.append(bt);
})});
