var captchaText = '';
var captchaContainer = document.getElementById('centralNoiseContainer');
captchaContainer.querySelectorAll('.noiseLine').forEach(function(line) {
	captchaText += line.innerText;
});
var input = document.getElementById('noiseInput');
for (var i = 0; i < captchaText.length; i++) {
	input.value += captchaText[i];
}
