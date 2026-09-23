/* =========================================================
   HireFlow - Main JavaScript
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       MOBILE MENU
    ====================================================== */

    const mobileMenuBtn = document.getElementById("mobileMenuBtn");
    const mobileMenu = document.getElementById("mobileMenu");

    if (mobileMenuBtn && mobileMenu) {

        mobileMenuBtn.addEventListener("click", function () {

            mobileMenu.classList.toggle("show");

            if (mobileMenu.classList.contains("show")) {
                mobileMenuBtn.innerHTML = "✕";
            } else {
                mobileMenuBtn.innerHTML = "☰";
            }

        });


        // Close mobile menu after clicking a link

        const mobileLinks =
            mobileMenu.querySelectorAll("a");

        mobileLinks.forEach(function (link) {

            link.addEventListener("click", function () {

                mobileMenu.classList.remove("show");

                mobileMenuBtn.innerHTML = "☰";

            });

        });

    }



    /* =====================================================
       SMOOTH SCROLLING
    ====================================================== */

    const allLinks =
        document.querySelectorAll('a[href^="#"]');

    allLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const targetId =
                this.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target =
                document.querySelector(targetId);

            if (target) {

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        });

    });



    /* =====================================================
       ACTIVE NAVIGATION
    ====================================================== */

    const sections =
        document.querySelectorAll("section[id]");

    const navLinks =
        document.querySelectorAll(".nav-link");

    function updateActiveNavigation() {

        let currentSection = "";

        sections.forEach(function (section) {

            const sectionTop =
                section.offsetTop - 150;

            const sectionHeight =
                section.offsetHeight;

            if (
                window.scrollY >= sectionTop &&
                window.scrollY < sectionTop + sectionHeight
            ) {

                currentSection =
                    section.getAttribute("id");

            }

        });


        navLinks.forEach(function (link) {

            link.classList.remove("active");

            const linkTarget =
                link.getAttribute("href");

            if (linkTarget === "#" + currentSection) {
                link.classList.add("active");
            }

        });

    }

    window.addEventListener(
        "scroll",
        updateActiveNavigation
    );

    updateActiveNavigation();



    /* =====================================================
       NAVBAR SCROLL EFFECT
    ====================================================== */

    const navbar =
        document.querySelector(".navbar");

    function navbarScrollEffect() {

        if (!navbar) {
            return;
        }

        if (window.scrollY > 30) {

            navbar.classList.add("scrolled");

        } else {

            navbar.classList.remove("scrolled");

        }

    }

    window.addEventListener(
        "scroll",
        navbarScrollEffect
    );

    navbarScrollEffect();



    /* =====================================================
       SCROLL REVEAL ANIMATION
    ====================================================== */

    const revealElements =
        document.querySelectorAll(
            ".feature-card, " +
            ".step-card, " +
            ".platform-stat, " +
            ".highlight-box, " +
            ".candidate-content, " +
            ".candidate-visual, " +
            ".recruiter-content, " +
            ".recruiter-visual"
        );


    revealElements.forEach(function (element) {

        element.classList.add("reveal");

    });


    const revealObserver =
        new IntersectionObserver(
            function (entries, observer) {

                entries.forEach(function (entry) {

                    if (entry.isIntersecting) {

                        entry.target.classList.add(
                            "reveal-visible"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    }

                });

            },
            {
                threshold: 0.12
            }
        );


    revealElements.forEach(function (element) {

        revealObserver.observe(element);

    });



    /* =====================================================
       BUTTON CLICK EFFECT
    ====================================================== */

    const buttons =
        document.querySelectorAll(".btn");

    buttons.forEach(function (button) {

        button.addEventListener("click", function () {

            button.classList.add("button-clicked");

            setTimeout(function () {

                button.classList.remove(
                    "button-clicked"
                );

            }, 180);

        });

    });



    /* =====================================================
       HERO DASHBOARD FLOATING ANIMATION
    ====================================================== */

    const dashboard =
        document.querySelector(".dashboard-window");

    if (dashboard) {

        dashboard.addEventListener(
            "mousemove",
            function (event) {

                const rect =
                    dashboard.getBoundingClientRect();

                const x =
                    event.clientX - rect.left;

                const y =
                    event.clientY - rect.top;

                const rotateY =
                    ((x / rect.width) - 0.5) * 3;

                const rotateX =
                    ((y / rect.height) - 0.5) * -3;

                dashboard.style.transform =
                    `perspective(1000px)
                     rotateX(${rotateX}deg)
                     rotateY(${rotateY}deg)`;

            }
        );


        dashboard.addEventListener(
            "mouseleave",
            function () {

                dashboard.style.transform =
                    "perspective(1000px) rotateX(0deg) rotateY(0deg)";

            }
        );

    }



    /* =====================================================
       AI MATCH SCORE ANIMATION
    ====================================================== */

    const progress =
        document.querySelector(".progress-value");

    if (progress) {

        const progressObserver =
            new IntersectionObserver(
                function (entries, observer) {

                    entries.forEach(function (entry) {

                        if (entry.isIntersecting) {

                            progress.classList.add(
                                "animate-progress"
                            );

                            observer.unobserve(
                                entry.target
                            );

                        }

                    });

                },
                {
                    threshold: 0.5
                }
            );


        progressObserver.observe(progress);

    }



    /* =====================================================
       NUMBER COUNTER ANIMATION
    ====================================================== */

    const counters =
        document.querySelectorAll(
            ".platform-stat strong"
        );


    counters.forEach(function (counter) {

        const originalText =
            counter.textContent.trim();

        const numberMatch =
            originalText.match(/[\d,.]+/);

        if (!numberMatch) {
            return;
        }

        const numberValue =
            parseFloat(
                numberMatch[0].replace(/,/g, "")
            );

        if (isNaN(numberValue)) {
            return;
        }


        let suffix = "";

        if (originalText.includes("K+")) {
            suffix = "K+";
        } else if (originalText.includes("%")) {
            suffix = "%";
        } else if (originalText.includes("+")) {
            suffix = "+";
        }


        counter.textContent = "0" + suffix;


        const counterObserver =
            new IntersectionObserver(
                function (entries, observer) {

                    entries.forEach(function (entry) {

                        if (!entry.isIntersecting) {
                            return;
                        }


                        let start = 0;

                        const duration = 1200;

                        const startTime =
                            performance.now();


                        function updateCounter(
                            currentTime
                        ) {

                            const elapsed =
                                currentTime - startTime;

                            const progressValue =
                                Math.min(
                                    elapsed / duration,
                                    1
                                );


                            const current =
                                Math.floor(
                                    start +
                                    (numberValue - start) *
                                    progressValue
                                );


                            counter.textContent =
                                current.toLocaleString() +
                                suffix;


                            if (
                                progressValue < 1
                            ) {

                                requestAnimationFrame(
                                    updateCounter
                                );

                            }

                        }


                        requestAnimationFrame(
                            updateCounter
                        );


                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.6
                }
            );


        counterObserver.observe(counter);

    });



    /* =====================================================
       FEATURE CARD HOVER
    ====================================================== */

    const featureCards =
        document.querySelectorAll(
            ".feature-card"
        );


    featureCards.forEach(function (card) {

        card.addEventListener(
            "mouseenter",
            function () {

                this.classList.add(
                    "feature-hover"
                );

            }
        );


        card.addEventListener(
            "mouseleave",
            function () {

                this.classList.remove(
                    "feature-hover"
                );

            }
        );

    });



    /* =====================================================
       CONTACT / FUTURE BUTTON HANDLER
    ====================================================== */

    const actionLinks =
        document.querySelectorAll(
            'a[href="#login"], ' +
            'a[href="#signup"]'
        );


    actionLinks.forEach(function (link) {

        link.addEventListener(
            "click",
            function (event) {

                const targetId =
                    this.getAttribute("href");

                const target =
                    document.querySelector(targetId);

                /*
                 * Login and Signup pages will be connected
                 * to Django authentication later.
                 */

                if (!target) {

                    event.preventDefault();

                    showHireFlowMessage(
                        "Authentication module coming soon."
                    );

                }

            }
        );

    });



    /* =====================================================
       TOAST MESSAGE
    ====================================================== */

    function showHireFlowMessage(message) {

        const oldToast =
            document.querySelector(
                ".hireflow-toast"
            );

        if (oldToast) {
            oldToast.remove();
        }


        const toast =
            document.createElement("div");

        toast.className =
            "hireflow-toast";

        toast.textContent =
            message;


        document.body.appendChild(toast);


        setTimeout(function () {

            toast.classList.add(
                "toast-show"
            );

        }, 50);


        setTimeout(function () {

            toast.classList.remove(
                "toast-show"
            );

            setTimeout(function () {

                toast.remove();

            }, 300);

        }, 2500);

    }



    /* =====================================================
       BACK TO TOP
    ====================================================== */

    const backToTop =
        document.createElement("button");

    backToTop.className =
        "back-to-top";

    backToTop.innerHTML =
        "↑";

    backToTop.setAttribute(
        "aria-label",
        "Back to top"
    );


    document.body.appendChild(
        backToTop
    );


    window.addEventListener(
        "scroll",
        function () {

            if (window.scrollY > 500) {

                backToTop.classList.add(
                    "show"
                );

            } else {

                backToTop.classList.remove(
                    "show"
                );

            }

        }
    );


    backToTop.addEventListener(
        "click",
        function () {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        }
    );



    /* =====================================================
       PAGE LOADED
    ====================================================== */

    console.log(
        "HireFlow JavaScript loaded successfully 🚀"
    );

});
