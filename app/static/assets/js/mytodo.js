async function getTaskById(id){
	let response = await fetch('mytodo/get');
	let jsonText = await response.json()

	task = jsonText.filter((task) => task.id == id)[0];

	return task;
}

function submitAddTask(){
	let nameTaskInput = document.getElementById('input-nametask')
	let descriptionTaskInput = document.getElementById('input-description')
	let datSuccessTaskInput = document.getElementById('input-dat')

	let modalWindow = document.getElementById('st1')

	const xhttp = new XMLHttpRequest();
	xhttp.onload = function() {
		if(this.status == 200){
			alert(xhttp.responseText);
			updateListTask();
            setTimeout(hoverListItem, 400);
		} else {
			alert("Problems sending to the server!")
		}
	}
	xhttp.open("POST", 'mytodo/add', true)
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(
			   `name-task=${nameTaskInput.value}&` + 
			   `desc-task=${descriptionTaskInput.value}&` +
			   `dat-succes=${datSuccessTaskInput.value}`
	);

	bootstrap.Modal.getInstance(modalWindow).hide()
}

function updateListTask(){
	function truncate(str, maxlength) {
	  return (str.length > maxlength) ?
		str.slice(0, maxlength - 1) + '…' : str;
	}

	const xhttp = new XMLHttpRequest()
	xhttp.onload = function() {
		if(this.status == 200){
			let jsonText = JSON.parse(xhttp.responseText);
			let listGroup = document.getElementById("task-list");

			listGroup.innerHTML = ""

			for (let i = 0; i < jsonText.length; i++){
				let newTask = document.createElement("li");

				newTask.classList.add("list-group-item");
				newTask.classList.add('list-group-item-action');

				$(newTask).attr('data-id', jsonText[i]['id']);	

				let date = new Date(jsonText[i]['dat_success'])
				let dateTimeString = date.toLocaleString('ru-RU', {
				  year: 'numeric',
				  month: '2-digit',
				  day: '2-digit',
				  hour: '2-digit',
				  minute: '2-digit',
				  second: '2-digit'
				});

				newTask.textContent = `Name task: ${truncate(jsonText[i]['name'], 15)} ` +
									  `Dat Success: ${dateTimeString}`;

				listGroup.appendChild(newTask);
			}
		}
	}
	xhttp.open("GET", 'mytodo/get', true)
	xhttp.setRequestHeader("Content-type", "application/json")
	xhttp.send()
}

async function modalViewTask(){
	$('.list-group-item').click(async function(e) {
		e.preventDefault();
		let id = $(this).data('id')
		let task = await getTaskById(id);
		
		let modal = new bootstrap.Modal($('#modal-view'));
		modal.show()
		$('#input-nametask2').val(task.name);
		$('#input-description2').val(task.description);
		$('#input-dat2').val(task.dat_success)
	})
}

function hoverListItem(){
	$('.list-group-item').hover(function(e) {
		e.preventDefault();
		$(this).addClass("active");
	}, function(e) {
		e.preventDefault();
		$(this).removeClass('active')
	})
}

$(window).on('load', function() {
	updateListTask();
	setTimeout(hoverListItem, 400);
	setTimeout(modalViewTask, 400);
})
