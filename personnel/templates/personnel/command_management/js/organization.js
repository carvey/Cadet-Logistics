

var moves = [];

function CadetMove(cadet_id, grouping_type, grouping_id)
{
    this.cadet_id = cadet_id;
    this.grouping_type = grouping_type;
    this.grouping_id = grouping_id;

}

//Droppable should be the container that a cadet is getting dropped in
//Unassigned is a bool to more quickly determine if a cadet has been dropped
// in the unassigned category
function CreateMove(draggable, droppable, unassigned, grouping_type)
{

    var cadet_id = draggable.data("id");
    var move_record;
    if (!unassigned)
    {
        var grouping_id = droppable.data("id");
        move_record = new CadetMove(cadet_id, grouping_type, grouping_id);

    }
    else
    {
        move_record = new CadetMove(cadet_id, null, null);
    }

    /*
    Before adding the new move record to the global list, check to see if a move for this
    particular cadet already exists. If so, override the previous move record with the new location.
    This is for cases where the cadet gets moved twice. If the cadet is getting moved for the first time,
    then just add the record to the global array.
     */

    var found = moves.some(function(el) {
        var match = el.cadet_id === cadet_id;
       if (match)
       {
           el.grouping_id = grouping_id;
           el.grouping_type = grouping_type;
       }
        return match;
    });

    if (!found)
        moves.push(move_record);

    console.log(moves);

}

$(".unassigned_cadets").draggable({
        appendTo: "body",
        helper: "clone"
    }
);

$(".assigned_cadet").draggable({
   appendTo: "body",
    helper: "clone"
});

$(".squad_container").droppable({
    activeClass: "droppable",
    hoverClass: "droppable_hover",
    accept: function(draggable) {
        //contains need DOM nodes not Jquery objects, so .get() is used
        return !$.contains(this, $(draggable).get(0));
    },
    drop: function(event, cadet)
    {
        var new_cadet_li = $( "<li></li>" ).appendTo( this );
        cadet.draggable.clone()
            .removeClass("unassigned_cadets")
            .addClass("assigned_cadet")
            .appendTo(new_cadet_li);
        cadet.draggable.parent().remove();

        CreateMove(cadet.draggable, $(this), false, "Squad");

        $(".assigned_cadet").draggable({
           appendTo: "body",
            helper: "clone"
        });

    }
});

$("#cadet_container").droppable({
    activeClass: "droppable",
    hoverClass: "droppable_hover",
    accept: ".assigned_cadet",
    drop: function(event, cadet)
    {
        var new_cadet_li = $( "<li></li>" ).appendTo( "#quad" );
        cadet.draggable.clone()
            .removeClass("assigned_cadet")
            .addClass("unassigned_cadets")
            .appendTo(new_cadet_li);
        cadet.draggable.parent().remove();

        CreateMove(cadet.draggable, $(this), true, null);

        $(".unassigned_cadets").draggable({
           appendTo: "body",
            helper: "clone"
        });
    }
});

//Save should, after a confirmation, turn the moves array into data that can be sent to and used
//by the server to make the necessary changes to the chain of command
function save()
{

}