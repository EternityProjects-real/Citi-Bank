var btnCreatCp = document.getElementById("btnCompte");
var btnConnex = document.getElementById("btnConnex");
var fieldInputs = document.getElementsByClassName('form-control');

btnCreatCp.addEventListener('click', function(evt) {
    evt.preventDefault()
    var wrap = document.getElementById('page_body').classList.add('logInActive');
});

btnConnex.addEventListener('click', function(evt) {
    evt.preventDefault()
    var wrap = document.getElementById('page_body').classList.remove('logInActive');
});


for (var i = 0; i < fieldInputs.length; i++) {
    var fieldInput = fieldInputs[i];
    fieldInput.addEventListener("focus", function(event) {
        this.parentElement.classList.add('focused', 'filled');
    }, true);

    fieldInput.addEventListener("blur", function(event) {

        if (this.value == "") {
            this.parentElement.classList.remove('filled');
        }
        this.parentElement.classList.remove('focused');
    }, true);

}