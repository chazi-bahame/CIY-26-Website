

// Kusimamia menyu ya simu (Mobile Menu Toggle)
const mobileMenu = document.getElementById('mobile-menu');
const navLinks = document.querySelector('.nav-links');

mobileMenu.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Kuficha menyu kiotomatiki mtumiaji anapobofya link yoyote kwenye simu
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
    });
});


// Kuchukua vipengele muhimu
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const closeBtn = document.querySelector('.close');
const galleryImages = document.querySelectorAll('.gallery-item img');

// Mtumiaji akibonyeza picha yoyote
galleryImages.forEach(img => {
    img.addEventListener('click', () => {
        lightbox.style.display = 'block';
        lightboxImg.src = img.src;
    });
});

// Kufunga picha kubwa ukibonyeza kitufe cha 'X'
closeBtn.addEventListener('click', () => {
    lightbox.style.display = 'none';
});

// Kufunga ukibonyeza nje kidogo ya picha
lightbox.addEventListener('click', (e) => {
    if (e.target !== lightboxImg) {
        lightbox.style.display = 'none';
    }
});


eventForm.addEventListener("submit", function(e) {
    e.preventDefault();
    const title = 
    document.getElementById("eventTitle").value;
    const date = 
    document.getElementById(eventDate).value;
    const description = 
    document.getElementById(eventDescription).value;
    const imageFile = 
    document.getElementById(eventImage).files[0];
    if (!imageFile) {
        alert("please select an event image.");
        return;
    }
    const [events, setEvents] = 
    useState([]);
    const handleAddEvent = (e) =>{
        e.preventDefault();
        //kutengeneza object ya tukio jipya
        const newEvent = {
            title,
            date,
            description,
            file
        };
        //kuongeza tukio kwenye orodha
        setEvents([...events, newEvent]);
        //kusafisha form baada ya kusubmit
        SVGTextPositioningElement('');
        SVGMetadataElement('');
    };
    
    //convert image to data
    const reader = 
    new FileReader();
    reader.onload = function() {
        const newEvent = {
            id:Date.now(),
            title:title,
            date:date,
            description:description,
            //picha ya event hii
            Image:reader.result
        };
        const events = 
        JSON.parse(localStorage.getItem("events")) || [];
        //andika event mpya
        events.push(newEvent);
        //save events
        localStorage.setItem(
            "events", JSON.stringify(events)
        );
        //clear form
        eventForm.reset();
        //display events
        loadEvents();
        alert("Event added successifully!");
    };
    reader.readAsDataURL(imageFile);
});
function deleteEvent(index) {
    const events = 
    JSON.parse(localStorage.getItem("events")) || [];
    events.splice(index, 1);
    localStorage.setItem("event", JSON.stringify(events));
    loadEvents();
}
// ============================
// START
// ============================
loadEvents();

const mobileMenu = document.getElementById("mobile-menu");
const navigation = document.querySelector(".main-navigation nav");

if (mobileMenu) {
mobileMenu.addEventListener("click", function () {
navigation.classList.toggle("active");
});
}

// ================= JOIN FORM =================

const joinForm = document.getElementById("joinForm");
const joinSuccess = document.getElementById("joinSuccess");

if (joinForm) {

    joinForm.addEventListener("submit", function(event) {

        event.preventDefault();

        joinSuccess.textContent =
            "Your application has been received successfully. The CIY-26 team will contact you through your email.";

        joinForm.reset();

    });

}
// ================= CONTACT FORM =================

document.addEventListener("DOMContentLoaded", function () {

    const contactForm = document.getElementById("contactForm");

    if (contactForm) {

        contactForm.addEventListener("submit", function (event) {

            // Allow the form to be submitted to Flask
            // Do not use event.preventDefault() here

        });

    }

});
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
// ================= LOGIN =================

document.addEventListener("DOMContentLoaded", function () {

    const loginButton = document.getElementById("loginButton");
    const loginMessage = document.getElementById("loginMessage");

    if (loginButton) {

        loginButton.addEventListener("click", function () {

            const email = document.getElementById("loginEmail").value;
            const password = document.getElementById("loginPassword").value;

            if (email === "" || password === "") {

                loginMessage.textContent =
                    "Please enter your email and password.";

                loginMessage.style.color = "#dc3545";

                return;
            }

            loginMessage.textContent =
                "Login interface is working. Real authentication will be added with Flask.";

            loginMessage.style.color = "#00a6c7";

        });

    }

});
// ================= MEMBER REGISTRATION =================

document.addEventListener("DOMContentLoaded", function () {

    const joinForm = document.getElementById("joinForm");
    const joinSuccess = document.getElementById("joinSuccess");

    if (joinForm) {

        joinForm.addEventListener("submit", function (event) {

            event.preventDefault();

            const password =
                document.getElementById("joinPassword").value;

            const confirmPassword =
                document.getElementById("confirmPassword").value;


            if (password !== confirmPassword) {

                joinSuccess.textContent =
                    "Passwords do not match.";

                joinSuccess.style.color = "#dc3545";

                return;
            }


            joinSuccess.textContent =
                "Your CIY-26 account information has been received successfully.";

            joinSuccess.style.color = "#00875a";

            joinForm.reset();

        });

    }

});


document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("mobile-menu");
    const navLinks = document.querySelector(".nav-links");

    if (!menuButton || !navLinks) {
        console.log("Mobile menu elements not found");
        return;
    }

    menuButton.addEventListener("click", function () {
        navLinks.classList.toggle("active");

        console.log(
            "Menu active:",
            navLinks.classList.contains("active")
        );
    });

    navLinks.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            navLinks.classList.remove("active");
        });
    });
});
