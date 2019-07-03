$(document).ready(function () {
    $('#but1').click(function () {
        $('#todo1').append("<ul>" + $("input[name=task1]").val() + " <a href='#' class='close' aria-hidden='true'>&times;</a></ul>");
    });
    $("body").on('click', '#todo1 a', function () {
        $(this).closest("ul").remove();
    });
});


$(document).ready(function () {
    $('#but2').click(function () {
        $('#todo2').append("<ul>" + $("input[name=task2]").val() + " <a href='#' class='close' aria-hidden='true'>&times;</a></ul>");
    });
    $("body").on('click', '#todo2 a', function () {
        $(this).closest("ul").remove();
    });
});