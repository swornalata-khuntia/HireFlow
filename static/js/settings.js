document.addEventListener("DOMContentLoaded", function () {

    const passwordInputs =
        document.querySelectorAll(
            'input[type="password"]'
        );

    passwordInputs.forEach(function (input) {

        input.addEventListener(
            "input",
            function () {

                input.style.borderColor = "";

            }
        );

    });

});