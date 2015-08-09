

var moves = [];

//CadetMove is acting like a class here, and an array of these instances will be sent to the server for changes to be made
function CadetMove(cadet_id, grouping_type, grouping_id, staff, vacating_group_id, vacating_position, commissioned, inactive)
{
    this.cadet_id = cadet_id; //id of the cadet being moved
    this.grouping_type = grouping_type; //the type of grouping the cadet is being dropped in
    this.grouping_id = grouping_id; //the id of the group the cadet is being dropped in
    this.staff = staff; //if the cadet is getting put in a staff position
    this.vacating_group_id = vacating_group_id; //the id of the group to be used if a cadet is leaving a staff position
    this.vacating_position = vacating_position; //the staff position a cadet is leaving
    this.commissioned = commissioned;
    this.inactive = inactive;

}

//Droppable should be the container that a cadet is getting dropped in
//Unassigned is a bool to more quickly determine if a cadet has been dropped
// in the unassigned category
//This class serves as a constructor for CadetMove objects.
function CreateMove(draggable, droppable, unassigned, grouping_type, staff, vacating_group_id, vacating_position, commissioned, inactive)
{

    var cadet_id = draggable.data("id");
    var move_record;
    var grouping_id;
    //The cadet is not getting moved to unassigned
    if (!unassigned)
    {

        grouping_id = $(droppable).data("id");

        if (grouping_id == undefined)
        {
            grouping_id = $(droppable).parents(".grouping").data("id");
        }
        console.log(staff);
        move_record = new CadetMove(cadet_id, grouping_type, grouping_id, staff, vacating_group_id, vacating_position, commissioned, inactive);

    }
    //the cadet is getting moved to the unassigned category
    else
    {
        move_record = new CadetMove(cadet_id, null, null, null, vacating_group_id, vacating_position, commissioned, inactive);
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
           el.staff = staff;
           if (el.vacating_group_id == undefined)
           {
               el.vacating_group_id = vacating_group_id;
               el.vacating_position = vacating_position;
           }
           el.commissioned = commissioned;
           el.inactive = inactive;
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
        //If the draggable comes from this droppable, do not accept it
        //unless the draggable is a squad leader
        //contains need DOM nodes not Jquery objects, so .get() is used
        return !$.contains(this, $(draggable).get(0)) || $.contains($(this).find(".squad_leader_container").get(0), $(draggable).get(0));
    },
    drop: function(event, cadet)
    {
        var new_cadet_li = $( "<li></li>" ).appendTo( this );
        cadet.draggable.clone()
            .removeClass("unassigned_cadets")
            .addClass("assigned_cadet")
            .appendTo(new_cadet_li)
            .draggable({
                appendTo: "body",
                helper: "clone"
        });

        if (cadet.draggable.data("staff") != undefined)
        {
            var vacating_group_id = cadet.draggable.parents(".grouping").data("id");
            var vacating_position = cadet.draggable.data("staff");

            CreateMove(cadet.draggable, $(this), false, "Squad", null, vacating_group_id, vacating_position, false, false);

        }
        else
            CreateMove(cadet.draggable, $(this), false, "Squad", null, null, null, false, false);

        cadet.draggable.parent().remove();

    }
});

$(".squad_leader_container").droppable({
    activeClass: "droppable",
    hoverClass: "droppable_hover",
    greedy: true,
    accept: function(draggable)
    {
        //don't accept the draggable if the squad leader container has a cadet in it
        return $(this).find(".assigned_cadet").length < 1 || $.contains(this, $(draggable).get(0));
    },
    drop: function(event, cadet) {
        var new_cadet_li = $( "<span></span>" ).appendTo( this );
        cadet.draggable.clone()
            .removeClass("unassigned_cadets")
            .addClass("assigned_cadet")
            .appendTo(new_cadet_li)
            .draggable({
                appendTo: "body",
                helper: "clone"
        });

        if (cadet.draggable.data("staff") != undefined)
        {
            var vacating_group_id = cadet.draggable.parents(".grouping").data("id");
            var vacating_position = cadet.draggable.data("staff");

            CreateMove(cadet.draggable, $(this), false, "Squad", "SL", vacating_group_id, vacating_position, false, false);

        }
        else
            CreateMove(cadet.draggable, $(this), false, "Squad", "SL", null, null, false, false);

        cadet.draggable.parent().remove();
    }
});

$(".company_staff_position").droppable({
    activeClass: "droppable",
    hoverClass: "droppable_hover",
    accept: function(draggable)
    {
        //don't accept the draggable if the squad leader container has a cadet in it
        //return $(this).find(".assigned_cadet").length < 1 || !$.contains(this, $(draggable).get(0));
        var cadet = $(this).find(".assigned_cadet").get(0);
        return !$.contains(this, cadet);
    },
    drop: function(event, cadet) {
        var new_cadet_li = $( "<span></span>" ).appendTo( this );
        cadet.draggable.clone()
            .removeClass("unassigned_cadets")
            .addClass("assigned_cadet")
            .appendTo(new_cadet_li)
            .draggable({
                appendTo: "body",
                helper: "clone"
        });

        var new_position = $(this).data("staff");

        if (cadet.draggable.data("staff") != undefined)
        {
            var vacating_group_id = cadet.draggable.parents(".grouping").data("id");
            var vacating_position = cadet.draggable.data("staff");

            CreateMove(cadet.draggable, $(this), false, "Company", new_position, vacating_group_id, vacating_position, false, false);

        }
        else
            CreateMove(cadet.draggable, $(this), false, "Company", new_position, null, null, false, false);

        cadet.draggable.parent().remove();
    }


});


$(".platoon_staff_position").droppable({
    activeClass: "droppable",
    hoverClass: "droppable_hover",
    accept: function(draggable)
    {
        //don't accept the draggable if the squad leader container has a cadet in it
        //return $(this).find(".assigned_cadet").length < 1 || !$.contains(this, $(draggable).get(0));
        var cadet = $(this).find(".assigned_cadet").get(0);
        return !$.contains(this, cadet);
    },
    drop: function(event, cadet) {
        var new_cadet_li = $( "<span></span>" ).appendTo( this );
        cadet.draggable.clone()
            .removeClass("unassigned_cadets")
            .addClass("assigned_cadet")
            .appendTo(new_cadet_li)
            .draggable({
                appendTo: "body",
                helper: "clone"
        });

        var new_position = $(this).data("staff");
        console.log(new_position);

        if (cadet.draggable.data("staff") != undefined)
        {
            var vacating_group_id = cadet.draggable.parents(".grouping").data("id");
            var vacating_position = cadet.draggable.data("staff");

            CreateMove(cadet.draggable, $(this), false, "Platoon", new_position, vacating_group_id, vacating_position, false, false);

        }
        else
            CreateMove(cadet.draggable, $(this), false, "Platoon", new_position, null, null, false, false);

        cadet.draggable.parent().remove();
    }

});

$("#unassigned").droppable({
    activeClass: "droppable",
    hoverClass: "droppable_hover",
    accept: ".assigned_cadet",
    drop: function(event, cadet)
    {
        var new_cadet_li = $( "<li></li>" ).appendTo( $(this).find(".quad") );
        cadet.draggable.clone()
            .removeClass("assigned_cadet")
            .addClass("unassigned_cadets")
            .appendTo(new_cadet_li)
            .draggable({
                appendTo: "body",
                helper: "clone"
        });

        if (cadet.draggable.data("staff") != undefined)
        {
            var vacating_group_id = cadet.draggable.parents(".grouping").data("id");
            var vacating_position = cadet.draggable.data("staff");
            CreateMove(cadet.draggable, $(this), true, "Squad", null, vacating_group_id, vacating_position, false, false);

        }
        else
         CreateMove(cadet.draggable, $(this), true, null, null, null, null, false, false);

        cadet.draggable.parent().remove();

    }
});


$("#inactive").droppable({
    activeClass: "droppable",
    hoverClass: "droppable_hover",
    accept: ".assigned_cadet",
    drop: function(event, cadet)
    {
        var new_cadet_li = $( "<li></li>" ).appendTo( $(this).find(".quad") );
        cadet.draggable.clone()
            .removeClass("assigned_cadet")
            .addClass("unassigned_cadets")
            .appendTo(new_cadet_li)
            .draggable({
                appendTo: "body",
                helper: "clone"
        });

        if (cadet.draggable.data("staff") != undefined)
        {
            var vacating_group_id = cadet.draggable.parents(".grouping").data("id");
            var vacating_position = cadet.draggable.data("staff");
            CreateMove(cadet.draggable, $(this), true, "Squad", null, vacating_group_id, vacating_position, false, true);

        }
        else
         CreateMove(cadet.draggable, $(this), true, null, null, null, null, false, true);

        cadet.draggable.parent().remove();

    }
});

$("#commissioned").droppable({
    activeClass: "droppable",
    hoverClass: "droppable_hover",
    accept: ".assigned_cadet",
    drop: function(event, cadet)
    {
        var new_cadet_li = $( "<li></li>" ).appendTo( $(this).find(".quad") );
        cadet.draggable.clone()
            .removeClass("assigned_cadet")
            .addClass("unassigned_cadets")
            .appendTo(new_cadet_li)
            .draggable({
                appendTo: "body",
                helper: "clone"
        });

        if (cadet.draggable.data("staff") != undefined)
        {
            var vacating_group_id = cadet.draggable.parents(".grouping").data("id");
            var vacating_position = cadet.draggable.data("staff");
            CreateMove(cadet.draggable, $(this), true, "Squad", null, vacating_group_id, vacating_position, true, false);

        }
        else
         CreateMove(cadet.draggable, $(this), true, null, null, null, null, true, false);

        cadet.draggable.parent().remove();

    }
});


//Save should, after a confirmation, turn the moves array into data that can be sent to and used
//by the server to make the necessary changes to the chain of command
function save()
{
    var data = JSON.stringify(moves);
    $.post("/personnel/organize/save/", data);
}

$('#confirm-delete').on('show.bs.modal', function(e) {
    $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
});