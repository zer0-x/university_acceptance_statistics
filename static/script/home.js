function handleClick(sex) {
	if (sex.id == 'male') {
		document.querySelectorAll('[data-sex="1"]').forEach(option => option.disabled = false);
		document.querySelectorAll('[data-sex="2"]').forEach(option => option.disabled = true);
	} else if (sex.id == 'female') {
		document.querySelectorAll('[data-sex="1"]').forEach(option => option.disabled = true);
		document.querySelectorAll('[data-sex="2"]').forEach(option => option.disabled = false);
	}
	document.getElementById('major').disabled = false;
}
