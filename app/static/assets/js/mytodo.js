function submitAddTask(){
	let nameTaskInput = document.getElementById('input-nametask')
	let descriptionTaskInput = document.getElementById('input-description')
	let datSuccessTaskInput = document.getElementById('input-dat')

	let modalWindow = document.getElementById('st1')

	const xhttp = new XMLHttpRequest();
	xhttp.onload = function() {
		if(this.status == 200){
			alert(xhttp.responseText)
		} else {
			alert("Problems sending to the server!")
		}
	}
	xhttp.open("POST", 'mytodo/add', true)
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(`name-task=${nameTaskInput.value}&desc-task=${descriptionTaskInput.value}&dat-succes=${datSuccessTaskInput.value}`)

	bootstrap.Modal.getInstance(modalWindow).hide()
}
