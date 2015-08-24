$(function() {
	function onFormSubmit(event){

		var data = $(event.target).serializeArray();
		var thesis = {};


		for(var i = 0; i<data.length ; i++){
			thesis[data[i].name] = data[i].value;
		}
		
		// send data to server
			var thesis_create_api = '/api/thesis';
			$.post(thesis_create_api, thesis, function(response){

			// read response from server
			if (response.status = 'OK') {
				$('input[type=text], [type=number], select, textarea').val('');
				$('table tr:first').after('<tr></tr>');
				$('tr:eq(1)').before('<td >'+ response.data.created_by + '</td>');
				$('tr:eq(1)').before('<td >'+ response.data.email + '</td>');
			    $('tr:eq(1)').before('<td >'+ response.data.year + '</td>');
			    $('tr:eq(1)').before('<td >'+ response.data.title + '</td>') ;
				$('tr:eq(1)').before('<td >'+ '&nbsp<a id="edit" href=\'edit_thesis/'+response.data.id+'\'><img src="/static/img/edit.png"/></a>'  + '&nbsp <a id="delete" href=\'delete_thesis/'+response.data.id+'\'><img src="/static/img/Delete.png"/></a>'+ '</td>') ;
				
				$('#thesis-list').append('<td>' + thesis_list + '</td>');
				
			} else {

			}

			});

		return false;
	}

	$('form#create-form').submit(onFormSubmit);

	$(document).on('click', '#delete', function(){
		$(this).closest('li').remove();
	});

	function loadThesis()
	{
		var thesis_list_api = '/api/thesis';
		$.get(thesis_list_api, {} , function(response) {
			console.log('#thesis-list', response)
			response.data.forEach(function(thesis){
				$('table tr:first').after('<tr></tr>');
				$('tr:eq(1)').before('<td >'+ thesis.created_by + '</td>');
				$('tr:eq(1)').before('<td >'+ thesis.email + '</td>');
			    $('tr:eq(1)').before('<td >'+ thesis.year + '</td>');
			    $('tr:eq(1)').before('<td >'+ thesis.title + '</td>') ;
				$('tr:eq(1)').before('<td >'+ '&nbsp<a id="edit" href=\'edit_thesis/'+thesis.id+'\'><img src="/static/img/edit.png"/></a>'  + '&nbsp <a id="delete" href=\'delete_thesis/'+thesis.id+'\'><img src="/static/img/Delete.png"/></a>'+ '</td>') ;
			});
		});
	}
	loadThesis();
/*
$("#slideshow > div:gt(0)").hide();

setInterval(function() { 
  $('#slideshow > div:first')
    .fadeOut(1000)
    .next()
    .fadeIn(500)
    .end()
    .appendTo('#slideshow');
},  5000);
*/

});