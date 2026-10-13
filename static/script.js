
document.addEventListener("DOMContentLoaded", function () {

    // ================= MOBILE MENU =================
    const menuButton = document.getElementById("mobile-menu");
    const navLinks = document.querySelector(".nav-links");

    if (menuButton && navLinks) {
        menuButton.addEventListener("click", function () {
            navLinks.classList.toggle("active");

            const isOpen = navLinks.classList.contains("active");
            menuButton.setAttribute("aria-expanded", String(isOpen));
        });

        navLinks.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("active");
                menuButton.setAttribute("aria-expanded", "false");
            });
        });
    }

    // ================= GALLERY LIGHTBOX =================
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    const closeBtn = document.querySelector(".close");
    const galleryImages = document.querySelectorAll(".gallery-item img");

    if (lightbox && lightboxImg) {
        galleryImages.forEach(function (img) {
            img.addEventListener("click", function () {
                lightbox.style.display = "block";
                lightboxImg.src = img.src;
            });
        });

        if (closeBtn) {
            closeBtn.addEventListener("click", function () {
                lightbox.style.display = "none";
            });
        }

        lightbox.addEventListener("click", function (event) {
            if (event.target !== lightboxImg) {
                lightbox.style.display = "none";
            }
        });
    }

    // ================= EVENTS =================
    const eventForm = document.getElementById("eventForm");

    if (eventForm) {
        eventForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const title = document.getElementById("eventTitle")?.value.trim();
            const date = document.getElementById("eventDate")?.value;
            const description =
                document.getElementById("eventDescription")?.value.trim();
            const imageInput = document.getElementById("eventImage");
            const imageFile = imageInput?.files[0];

            if (!title || !date || !description) {
                alert("Please fill in all event details.");
                return;
            }

            if (!imageFile) {
                alert("Please select an event image.");
                return;
            }

            const reader = new FileReader();

            reader.onload = function () {
                try {
                    const events = JSON.parse(
                        localStorage.getItem("events") || "[]"
                    );

                    events.push({
                        id: Date.now(),
                        title: title,
                        date: date,
                        description: description,
                        Image: reader.result
                    });

                    localStorage.setItem("events", JSON.stringify(events));
                    eventForm.reset();

                    if (typeof window.loadEvents === "function") {
                        window.loadEvents();
                    }

                    alert("Event added successfully!");
                } catch (error) {
                    console.error("Could not save event:", error);
                    alert("Could not save the event. Please try again.");
                }
            };

            reader.onerror = function () {
                alert("Could not read the selected image.");
            };

            reader.readAsDataURL(imageFile);
        });
    }

    // ================= JOIN / MEMBER FORM =================
    const joinForm = document.getElementById("joinForm");
    const joinSuccess = document.getElementById("joinSuccess");

    if (joinForm) {
        joinForm.addEventListener("submit", function (event) {
            const passwordInput = document.getElementById("joinPassword");
            const confirmPasswordInput =
                document.getElementById("confirmPassword");

            if (passwordInput && confirmPasswordInput) {
                if (passwordInput.value !== confirmPasswordInput.value) {
                    event.preventDefault();

                    if (joinSuccess) {
                        joinSuccess.textContent = "Passwords do not match.";
                        joinSuccess.style.color = "#dc3545";
                    }
                    return;
                }
            }

            // Keep the existing Flask submission behavior.
            // Do not prevent the form from submitting when valid.
        });
    }

    // ================= LOGIN =================
    const loginButton = document.getElementById("loginButton");
    const loginMessage = document.getElementById("loginMessage");

    if (loginButton && loginMessage) {
        loginButton.addEventListener("click", function () {
            const emailInput = document.getElementById("loginEmail");
            const passwordInput = document.getElementById("loginPassword");

            const email = emailInput ? emailInput.value.trim() : "";
            const password = passwordInput ? passwordInput.value : "";

            if (!email || !password) {
                loginMessage.textContent =
                    "Please enter your email and password.";
                loginMessage.style.color = "#dc3545";
                return;
            }

            loginMessage.textContent =
                "Login interface is working. Real authentication must be handled by Flask.";
            loginMessage.style.color = "#00a6c7";
        });
    }

    // ================= BACK TO TOP =================
    const backToTop = document.getElementById("backToTop");

    if (backToTop) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 400) {
                backToTop.classList.add("show");
            } else {
                backToTop.classList.remove("show");
            }
        });

        backToTop.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }

});
