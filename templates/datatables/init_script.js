{% load static %}

//initilize the datatable with no settings so that all dom elements can be assigned
var dt = $('.datatables-instance').dataTable({
    destroy: true
});

//actual datatable initilization that will be used
var final_dt = $('.datatables-instance').dataTable({
    "dom": 'TCR<"clear">lfrtip',
        "tableTools": {
            "sSwfPath": "{% static 'css/plugins/dataTables/plugins/TableTools/copy_csv_xls_pdf.swf' %}"
        },

        "fnInitComplete": function() {
            //$(".dataTables_filter").each(function() {
            //    var exporting_container = $(this).siblings(".DTTT_container").get(0);
            //    var vis_container = $(this).siblings(".ColVis").get(0);
            //
            //    $(this).insertBefore(exporting_container);
            //    $(vis_container).insertAfter(this);
            //});

            $(".ColVis").each(function() {
               var panel = $(this).parents('.panel').find('.right-panel-header').get(0);
                $(this).appendTo(panel);
            });

            $(".DTTT_container").each(function() {
               var panel = $(this).parents('.panel').find('.right-panel-header').get(0);
                $(this).appendTo(panel);
            });
        },
        "bDestroy": true,
        "aoColumnDefs": [
             <!--Column indices that should be hidden by default go in the block within the brackets-->
             {"bVisible": false, "aTargets": hide_list}

         ]
});