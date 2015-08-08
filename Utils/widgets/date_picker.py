from django.forms import Widget
from django.utils.safestring import mark_safe

class DatePicker(Widget):

    def render(self, name, value, attrs=None):

        update_date = ""
        if value:
            update_date = """
            $('#date').datepicker('update', '%s');
            $("#id_date").val(
                        $("#date").datepicker('getFormattedDate')
                    );
            """ % value

        html = """

            <div id='date' 'data-date-format': 'YYYY-mm-dd'></div>
            <input id="id_date" type='hidden' name='date'>

            <script>
                var date = new Date();
                var thisYear = date.getFullYear();

                $("#date").datepicker({
                    format: "yyyy-mm-dd",

                });


                %s


                $("#date").on('changeDate', function(event) {
                    $("#id_date").val(
                        $("#date").datepicker('getFormattedDate')
                    );

                });
            </script>
        """ % update_date

        return mark_safe(html)


class BirthDatePicker(Widget):
    def render(self, name, value, attrs=None):

        html = """

            <div id='date' 'data-date-format': 'YYYY-mm-dd'></div>
            <input id="id_birth_date" type='hidden' name='birth_date'>

            <script>
                var date = new Date();
                var thisYear = date.getFullYear();

                $("#date").datepicker({
                    format: "yyyy-mm-dd",

                });


                $("#date").on('changeDate', function(event) {
                    $("#id_birth_date").val(
                        $("#date").datepicker('getFormattedDate')
                    );

                });
            </script>
        """

        return mark_safe(html)