from django.forms import Widget
from django.utils.safestring import mark_safe

class DatePicker(Widget):

    def render(self, name, value, attrs=None):

        update_date = ""
        if value:
            update_date = """
            $('#birth_datepicker').datepicker('update', '%s');
            $("#id_birth_date").val(
                        $("#birth_datepicker").datepicker('getFormattedDate')
                    );
            """ % value

        html = """

            <div id='birth_datepicker' 'data-date-format': 'YYYY-mm-dd'></div>
            <input id="id_birth_date" type='hidden' name='birth_date'>

            <script>
                var date = new Date();
                var thisYear = date.getFullYear();

                $("#birth_datepicker").datepicker({
                    format: "yyyy-mm-dd",
                    defaultViewDate: { year: thisYear - 18 }
                });


                %s


                $("#birth_datepicker").on('changeDate', function(event) {
                    $("#id_birth_date").val(
                        $("#birth_datepicker").datepicker('getFormattedDate')
                    );

                });
            </script>
        """ % update_date

        return mark_safe(html)