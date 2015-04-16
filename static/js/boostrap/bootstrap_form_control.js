    $(document).ready(function() {
        $("select,:text,:input[type='number'],:input[type='email'],:input[type='password']").addClass("form-control");
        $(":checkbox").addClass("checkbox");

        try
        {
            $("#id_date").datepicker({
                format: 'yyyy-mm-dd'
            });


            var date = new Date();
            var thisYear = date.getFullYear();

            var gender_p = $("#id_gender").parents('p');
            var date_p = $("<p id='date_p'></p>").insertBefore(gender_p);
            $("<div id='birth_datepicker'></div>").appendTo(date_p);

            $("<label>Birth date:</label>").insertBefore("#birth_datepicker");

            $("#birth_datepicker").datepicker({
                format: "yyyy-mm-dd",
                defaultViewDate: { year: thisYear - 18 }
            });

            $("#birth_datepicker").on('changeDate', function(event) {
                $("#id_birth_date").val(
                    $("#birth_datepicker").datepicker('getFormattedDate')
                );

            });

        }
        catch(err)
        {
            console.log(err);
        }
    });