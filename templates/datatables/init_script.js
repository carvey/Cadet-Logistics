{% load static %}

//initilize the datatable with no settings so that all dom elements can be assigned
var dt = $('#datatables-instance').dataTable({});

//setup search bars under all columns (before any are hidden)
setup_column_search();

//the method to handle adding the per column filtering
function setup_column_search() {
    $('#datatables-instance tfoot td').each( function () {
        var title = $('#datatables-instance tfoot td').eq( $(this).index() ).text();
        $(this).html( '<input type="text" class="form-control" style="width:100%" placeholder="Search '+title+'" />' );
    });

    var table = dt.api();

    table.columns().eq( 0 ).each( function ( colIdx ) {
        $( 'input', table.column( colIdx ).footer() ).on( 'keyup change', function () {
            table
                .column( colIdx )
                .search( this.value )
                .draw();
        } );
    } );
}

//actual datatable initilization that will be used
var final_dt = $('#datatables-instance').dataTable({
    "dom": 'TCR<"clear">lfrtip',
        "tableTools": {
            "sSwfPath": "{% static 'css/plugins/dataTables/plugins/TableTools/copy_csv_xls_pdf.swf' %}"
        },

        "fnInitComplete": function() {
            $('.ColVis').appendTo(".right-panel-header");
            $('.DTTT_container').appendTo('.right-panel-header');
        },
        "bDestroy": true,
        "aoColumnDefs": [
             <!--Column indices that should be hidden by default go in the block within the brackets-->
             {"bVisible": false, "aTargets": hide_list}

         ]
});