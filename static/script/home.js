function handleClick(sex) {
	if (sex.value == 'M') {
		document.getElementById('1').disabled = false;
		document.getElementById('2').disabled = true;
	} else if (sex.value == 'F') {
		document.getElementById('1').disabled = true;
		document.getElementById('2').disabled = false;
	}
	document.getElementById('major').disabled = false;
}