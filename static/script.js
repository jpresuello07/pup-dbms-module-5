var thesislist=[];

function onFormSubmit(event){
	var data = $(event.target).serializeArray();

	var thesis={};

	for (var i=0;i<data.length;i++){
		thesis[data[i].name] = data[i].value;
	}

	var list_element=$('<li id="item"' +'class="' + thesis.year + thesis.title1 + '">');
	
	var item = list_element.html(thesis.year + ' ' + thesis.title1);

	//send data to server
	var thesis_entry_api = '/api/thesis';
	$.post(thesis_entry_api, thesis, function(response){
	//read response from server
	//if student save is successful
		if(response.status = 'OK') {
			//display student
			var full_info = response.data.year + ' ' + response.data.title1+ ' - Entered by:' + response.data.author;
			$('.thesis-list').append('<li>' + full_info + '<li>')
		}
		else {
			//if student is not successful
		}
	});


	return false;
}

function onRegFormSubmit(event){
	var data = $(event.target).serializeArray();

	var users={};

	for (var i=0;i<data.length;i++){
		users[data[i].name] = data[i].value;
	}

	//send data to server
	var user_entry_api = '/register';
	$.post(user_entry_api, users, function(response){
	//read response from server
	//if student save is successful
		if(response.status = 'OK') {
			//display student
			alert('Registration Successful!')
			window.location.replace('/home')
		}
		else {
			//if student is not successful
			alert('Registration not Successful!')
		}
	});


	return false;

}

function loadAllthesis(){
	var thesis_list_api = '/api/thesis';
	$.get(thesis_list_api, {}, function(response){
		response.data.forEach(function(thesis) {
			var full_info = thesis.year + ' - ' + thesis.title1;
			thesis.author.forEach(function(author_name){
				var thesis_auth = author_name.first_name + '  ' + author_name.last_name;
				$('.thesis-list').append('<li>' + full_info + ' Entered by: ' + thesis_auth +'</li>');
			})
		});
	});
}

$('.reg-form').submit(onRegFormSubmit);

$('.create-form').submit(onFormSubmit);

loadAllthesis();