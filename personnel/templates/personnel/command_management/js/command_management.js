/**
 * Created by charles on 4/4/15.
 */


$( document ).ready(function() {
jQuery(document).ready(function() {
    $("#org").jOrgChart({
        chartElement : '#organization_content_area',
        dragAndDrop  : false
    });

    (function() {
          var $section = $('#focal');
          var $panzoom = $section.find('.jOrgChart').panzoom();
          $panzoom.parent().on('mousewheel.focal', function( e ) {
            e.preventDefault();
            var delta = e.delta || e.originalEvent.wheelDelta;
            var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
            $panzoom.panzoom('zoom', zoomOut, {
              increment: 0.1,
              animate: false,
              focal: e
            });
          });
        })();

    });
});