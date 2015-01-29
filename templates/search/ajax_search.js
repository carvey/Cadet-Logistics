

$(document).ready(function ()
{
    $('#search-form').submit(function () {
        var query = $('#site-search').val();
        $.get('/search/' + query, {}, function (data) {
            $('#searchModal').modal('toggle');
            $('#search-modal-body').html(data);
            //this is done here instead of in a template to avoid strange modal problems
            $('#query-string').html(query);
        });
        return false;
    });
});