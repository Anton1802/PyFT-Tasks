async function getTaskById(id){
	let response = await fetch('mytodo/get');
	let jsonText = await response.json();

	task = jsonText.filter((task) => task.id == id)[0];

	return task;
}

async function submitAddTask(){
	let nameTaskInput = document.getElementById('input-nametask');
	let descriptionTaskInput = document.getElementById('input-description');
	let datSuccessTaskInput = document.getElementById('input-dat');

	let modalWindow = document.getElementById('st1');

	const xhttp = new XMLHttpRequest();
	xhttp.onload = async function() {
		if(this.status == 200){
			alert(xhttp.responseText);
			updateListTask();
			stopNotice();
            setTimeout(hoverListItem, 400);
		} else {
			alert("Problems sending to the server!");
		}
	}
	xhttp.open("POST", 'mytodo/add', true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(
			   `name-task=${nameTaskInput.value}&` + 
			   `desc-task=${descriptionTaskInput.value}&` +
			   `dat-succes=${datSuccessTaskInput.value}`
	);
	bootstrap.Modal.getInstance(modalWindow).hide();
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

            if(jsonText.length == 0){
                listGroup.innerHTML = "";

                let text_a = document.createTextNode("You don't have tasks!");
                let text_b = document.createTextNode("Please click button: Add Task!");

                listGroup.appendChild(text_a);
                listGroup.appendChild(document.createElement("br"));
                listGroup.appendChild(text_b);

                return 
            } else {
                listGroup.innerHTML = '';
            }

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
                modalViewTask();
			}
		}
	}
	xhttp.open("GET", 'mytodo/get', true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send();
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
		$('#input-dat2').val(task.dat_success);

        $('#btn-delete-task').off("click").one("click", async function(e){
            let requestOptions = {
                method: 'DELETE'
            };
            let response = await fetch(`mytodo/del/${id}`, requestOptions);
            let jsonResponse = await response.json();
            alert(jsonResponse.message);
			modal.hide();
            updateListTask();
			await stopNotice();
        });

        $('#btn-edit-task').off("click").one("click", async function(e){
            let nameTask = $('#input-nametask2').val();
            let descriptionTask = $('#input-description2').val();
            let datTask = $('#input-dat2').val();
            let requestOptions = {
                method: 'PUT',
                body: JSON.stringify({
                    name_task: nameTask,
                    description_task: descriptionTask,
                    dat_task: datTask,
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            let response = await fetch(`mytodo/edit/${id}`, requestOptions);
            let jsonResponse = await response.json();
			modal.hide();
			alert(jsonResponse.message);
            updateListTask();
        });
	});
}

async function getNotice(){
	let requestOptions = {
		method: "GET"
	}

	let response = await fetch('mytodo/notice/get', requestOptions)
	let jsonResponse = await response.json()

	return jsonResponse
}

async function startNotice(){
	let chat_id = $('#input-chat-id').val();
	let interval = $('#input-interval-time').val();

	let requestOptions = {
		method: "POST",
		body: JSON.stringify({
			chat_id: chat_id,
			interval: interval,
		}),
		headers: {
			'Content-Type': 'application/json'
		}
	};

	let response = await fetch('mytodo/notice/start', requestOptions);
	let jsonResponse = await response.json();

	alert(jsonResponse.message);
}

async function stopNotice(){
	let requestOptions = {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json"
		}
	};

	let response = await fetch('mytodo/notice/stop', requestOptions)
	let jsonResponse = await response.json();

	alert(jsonResponse.message)
}


function hoverListItem(){
	$('.list-group-item').hover(function(e) {
		e.preventDefault();
		$(this).addClass("active");
	}, function(e) {
		e.preventDefault();
		$(this).removeClass('active');
	})
}

$(window).on('load', function() {
	updateListTask();
	setTimeout(hoverListItem, 400);

	$('#btn-modal-settings-notice').click(async function() {
		let jsonConfig = await getNotice()
		$('#input-chat-id').val(jsonConfig['chat_id']);
		$('#input-interval-time').val(jsonConfig['interval']);
		let modalNotice = new bootstrap.Modal($('#modal-settings-notice'));
		modalNotice.show()
		$('#apply-settings-notice').off('click').one("click", async function () {
			await startNotice();
			modalNotice.hide();
		})
		$('#stop-settings-notice').off('click').one("click", async function () {
			await stopNotice();
			modalNotice.hide();
		})
	});
});
