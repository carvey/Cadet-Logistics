$(document).ready(function() {

    //var gender_p = $("#id_gender").parent().parent();
    //var date_div = $("<div class='form-group'></div>").insertBefore(gender_p);
    //$("<label class='control-label col-sm-2 col-lg-2' " + "for='id_birth_date_picker'>Birth Date</label>").appendTo(date_div);
    //var input_div = $("<div class=' col-sm-10 col-lg-10 '></div>").appendTo(date_div);
    //$("<div id='birth_datepicker'></div>").appendTo(input_div);

    //$("#id_birth_date").appendTo(input_div);

    var date = new Date();
    var thisYear = date.getFullYear();

    $("#birth_datepicker").datepicker({
        format: "yyyy-mm-dd",
        defaultViewDate: { year: thisYear - 18 }
    });

    var date_entered = $("#id_birth_date").val();
    if (date_entered)
    {
        $("#birth_datepicker").datepicker('update', date_entered);
    }

    $("#birth_datepicker").on('changeDate', function(event) {
        $("#id_birth_date").val(
            $("#birth_datepicker").datepicker('getFormattedDate')
        );

    });

});