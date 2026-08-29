const form = document.getElementById("checkoutForm");

form.addEventListener("submit", function(event) {

    event.preventDefault();

    let valid = true;

    // Get values
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const address = document.getElementById("address").value.trim();

    // Error elements
    const nameError = document.getElementById("nameError");
    const emailError = document.getElementById("emailError");
    const phoneError = document.getElementById("phoneError");
    const addressError = document.getElementById("addressError");


    // Clear previous errors
    nameError.textContent = "";
    emailError.textContent = "";
    phoneError.textContent = "";
    addressError.textContent = "";


    // Name validation
    if (name === "") {

        nameError.textContent = "Name is required";
        valid = false;

    } else if (name.length < 3) {

        nameError.textContent =
            "Name must contain at least 3 characters";

        valid = false;
    }


    // Email validation
    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (email === "") {

        emailError.textContent =
            "Email is required";

        valid = false;

    } else if (!emailPattern.test(email)) {

        emailError.textContent =
            "Enter a valid email address";

        valid = false;
    }


    // Phone validation
    const phonePattern = /^[0-9]{10}$/;

    if (phone === "") {

        phoneError.textContent =
            "Phone number is required";

        valid = false;

    } else if (!phonePattern.test(phone)) {

        phoneError.textContent =
            "Phone number must contain 10 digits";

        valid = false;
    }


    // Address validation
    if (address === "") {

        addressError.textContent =
            "Address is required";

        valid = false;

    } else if (address.length < 10) {

        addressError.textContent =
            "Please enter a complete address";

        valid = false;
    }


    // Submit form
    if (valid) {

        form.submit();

    }

});