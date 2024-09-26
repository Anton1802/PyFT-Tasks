async function getTaskById(id){
	let response = await fetch('mytodo/get');
	let jsonText = await response.json();

	task = jsonText.filter((task) => task.id == id)[0];

	return task;
}

async function submitAddTask(){
	let nameTaskInput = $('#input-nametask')
	let descriptionTaskInput = $('#input-description')
	let datSuccessTaskInput = $('#input-dat')

	let requestOptions = {
		method: "POST",
		body: JSON.stringify({
			'name_task': nameTaskInput.val(),
			'desc_task': descriptionTaskInput.val(),
			'dat_success': datSuccessTaskInput.val(),
		}),
		headers: {
			'Content-Type': 'application/json'
		}
	}

	let response = await fetch('mytodo/add', requestOptions)
	let jsonResponse = await response.json()

	alert(jsonResponse.message)
}

async function updateListTask(){
	let status = await getNoticeStatus()
	if (status.length > 0) {
		$("#btn-modal-settings-notice").removeClass('btn-primary')
		$("#btn-modal-settings-notice").addClass('btn-success')
	} else {
		$("#btn-modal-settings-notice").removeClass('btn-success')
		$("#btn-modal-settings-notice").addClass('btn-primary')
	}

	let response = await fetch('mytodo/get')
	let responseJson = await response.json()

	let listGroup = $('#task-list')

	if(responseJson.length == 0)
	{
		listGroup.empty()

		let text_a = document.createTextNode("You don't have tasks!");
        let text_b = document.createTextNode("Please click button: Add Task!");

		listGroup.append(text_a);
		listGroup.append($("<br>"));
		listGroup.append(text_b);

		return
	} else {
		listGroup.empty()
	}

	listGroup.empty()

	for(let i = 0; i < responseJson.length; i++)
	{
		let newTask = $("<li>");

		newTask.addClass("list-group-item");
		newTask.addClass('list-group-item-action');
		newTask.addClass("d-flex");
		newTask.addClass("justify-content-between");

		$(newTask).attr('data-id', responseJson[i]['id']);	

		let date = new Date(responseJson[i]['dat_success'])
		let dateTimeString = date.toLocaleString('ru-RU', {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit'
		});

		let taskName = $("<span>").text(responseJson[i]['name'].substring(0,10) + "...");
		let taskDate = $("<span>").text(dateTimeString).addClass('me-2');

		let dateContainer = $("<div>").addClass("d-flex align-items-center");

		dateContainer.append(taskDate);

		newTask.append(taskName);
		newTask.append(dateContainer);

		listGroup.append(newTask);
		$('.list-group-item').off('click').click(async function() {
			await modalViewTask($(this).data('id'))
		})
	}
	await hoverListItem()
}

async function modalViewTask(id){
	let task = await getTaskById(id)
	let modal = new bootstrap.Modal($('#modal-view'))

	modal.show()

	$('#input-nametask2').val(task.name);
	$('#input-description2').val(task.description);
	$('#input-dat2').val(task.dat_success);

	$('#btn-delete-task').off("click").one("click", async function(){
		let requestOptions = {
			method: 'DELETE'
		};
		let response = await fetch(`mytodo/del/${id}`, requestOptions);
		let jsonResponse = await response.json();
		alert(jsonResponse.message);
		modal.hide();
		await stopNotice();
		await updateListTask();
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
		await stopNotice();
		await updateListTask();
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

async function getNoticeStatus(){
	let requestOptions = {
		method: "GET"
	}

	let response = await fetch('mytodo/notice/get_jobs', requestOptions)
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

async function hoverListItem(){
	$('.list-group-item').hover(async function(e) {
		$(this).addClass("active");
	}, async function() {
		$(this).removeClass('active');
	})
}

$(window).on('load', async function() {
	await updateListTask()

	$('#btn-modal-add-task').click(async function () {
		let modalAddTask = new bootstrap.Modal($('#modal-add-task'))
		modalAddTask.show()
		$("#modal-btn-add-task").off('click').one('click', async function(){
			await submitAddTask()
			modalAddTask.hide()
			await stopNotice();
			await updateListTask()
		})
	})

	$('#btn-modal-settings-notice').click(async function() {
		let jsonConfig = await getNotice()
		$('#input-chat-id').val(jsonConfig['chat_id']);
		$('#input-interval-time').val(jsonConfig['interval']);
		let modalNotice = new bootstrap.Modal($('#modal-settings-notice'));
		modalNotice.show()
		$('#apply-settings-notice').off('click').one("click", async function () {
			await startNotice();
			modalNotice.hide();
			await updateListTask()
		})
		$('#stop-settings-notice').off('click').one("click", async function () {
			await stopNotice();
			modalNotice.hide();
			await updateListTask()
		})
		$('#input-current-value').text($('#input-interval-time').val())
		$('#input-interval-time').on('input', async function() {
			$('#input-current-value').text($('#input-interval-time').val())
		})
	});
});
