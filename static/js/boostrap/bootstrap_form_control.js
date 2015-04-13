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

            $("#id_birth_date").datepicker({
                format: "yyyy-mm-dd",
                defaultViewDate: { year: thisYear - 18 }
            });
        }
        catch(err)
        {
            console.log(err);
        }
    });