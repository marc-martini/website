$(function() {
		$('#rng1').bind('change', function() {
		    $.getJSON('/_histo_graph', {
			  rng : $('#rng1').val(), sym : $("#stock").data('stock'), stock_name : $("#stock").data('name')
			}, function(data) {
			  $(".histo").remove();
			  $("#graph").append('<embed class="histo" type="image/svg+xml" src=' + data.graph + ' style="max-width:1000px"/>');
              });
			return false;
		  });
		});




$(function() {
	$('#rng').bind('change', function() {
		$.getJSON('/_stock_comp_graph', {
    		  rng : $('#rng').val(),
    		  sym1 : $("#stock1").data('stock'), stock_name1 : $("#stock1").data('name'),
    		  sym2 : $("#stock2").data('stock'), stock_name2 : $("#stock2").data('name'),
    		  sym3 : $("#stock3").data('stock'), stock_name3 : $("#stock3").data('name'),
	    }, function(data) {
			  $(".histo").remove();
			  $("#graph").append('<embed class="histo" type="image/svg+xml" src=' + data.graph + ' style="max-width:1000px"/>');
        });
		return false;
	});
});





function add_stock_db(id) {
    $.getJSON("/_stock_add_stock_db", {
        sym : $(id).data('stock'),
        name : $(id).data('name')
    }, function(data) {
        $("#mess").append('<div id=fl_al class="alert alert-'+data.cat+' border text-center" role="alert">'+data.message+'</div>');
        setTimeout(function () {$('#fl_al').remove();}, 5000);
    });
    return false;
}

function remove_stock_db(sym,name) {
    $.getJSON("/_stock_remove_stock_db", {
        sym : sym,
        name : name
    });
}
