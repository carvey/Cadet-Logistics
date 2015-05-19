    $(document).ready(function() {
        $("select,:text,:input[type='number'],:input[type='email'],:input[type='password']").addClass("form-control");
        $(":checkbox").addClass("checkbox");

        $("#id_date").datepicker({
            format: 'yyyy-mm-dd'
        });

    });