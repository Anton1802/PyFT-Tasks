function submitAddTask(){
	let nameTaskInput = document.getElementById('input-nametask')
	let descriptionTaskInput = document.getElementById('input-description')
	let datSuccessTaskInput = document.getElementById('input-dat')

	let modalWindow = document.getElementById('st1')

	const xhttp = new XMLHttpRequest();
	xhttp.onload = function() {
		if(this.status == 200){
			alert(xhttp.responseText)
			updateListTask()
		} else {
			alert("Problems sending to the server!")
		}
	}
	xhttp.open("POST", 'mytodo/add', true)
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(`name-task=${nameTaskInput.value}&desc-task=${descriptionTaskInput.value}&dat-succes=${datSuccessTaskInput.value}`)

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
				newTask.classList.add("list-group-item", "list-group-item-primary", "d-flex");
				let date = new Date(jsonText[i]['dat_success'])
				let dateTimeString = date.toLocaleString('ru-RU', {
				  year: 'numeric',
				  month: '2-digit',
				  day: '2-digit',
				  hour: '2-digit',
				  minute: '2-digit',
				  second: '2-digit'
				});
				newTask.textContent = `Name task: ${truncate(jsonText[i]['name'], 15)} Dat Success: ${dateTimeString}`;
				listGroup.appendChild(newTask);

				let buttonView = document.createElement('button');
				buttonView.setAttribute("type", "button");
				buttonView.classList.add('btn', 'btn-primary', 'button-view', "ms-auto");
				buttonView.textContent = "View";
				newTask.appendChild(buttonView);
			}
		}
	}
	xhttp.open("GET", 'mytodo/get', true)
	xhttp.setRequestHeader("Content-type", "application/json")
	xhttp.send()
}

document.addEventListener("DOMContentLoaded", updateListTask);
