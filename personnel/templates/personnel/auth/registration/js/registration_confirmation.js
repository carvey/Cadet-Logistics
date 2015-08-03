
function save()
{
    var approval_record = [];
    var approved_cadets = $(".cadet_checkbox:checked");
    $.each(approved_cadets, function() {
        var cadet_id = $(this).parent().data("id");
        approval_record.push(cadet_id);
    });

    var data = JSON.stringify(approval_record);
    $.post("/personnel/registered/save/", data, function() {
        location.reload();
    });

}