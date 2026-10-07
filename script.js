// -------------------------
// PARTICULES
// -------------------------

const section = document.getElementById("accueil");
const canvas = document.getElementById("particles-canvas");
const ctx = canvas.getContext("2d");

let particles = [];
let animationId = null;
let running = false;

function resizeCanvasToSection() {
    canvas.width = section.clientWidth;
    canvas.height = section.clientHeight;
}

window.addEventListener("resize", resizeCanvasToSection);
resizeCanvasToSection();

section.addEventListener("mousemove", (e) => {
    const rect = section.getBoundingClientRect();

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    for (let i = 0; i < 2; i++) {
        particles.push({
            x,
            y,
            radius: Math.random() * 4 + 0.5,
            alpha: 1,
            dx: (Math.random() - 0.5) * 1.5,
            dy: (Math.random() - 0.5) * 1.5,
        });
    }
});

function animate() {
    if (!running) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        p.x += p.dx;
        p.y += p.dy;
        p.alpha -= 0.005;

        if (p.alpha <= 0) {
            particles.splice(i, 1);
            i--;
            continue;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 132, 148, ${p.alpha})`;
        ctx.fill();

        let connectionCount = 0;

        for (let j = i + 1; j < particles.length; j++) {
            const p2 = particles[j];

            const dx = p.x - p2.x;
            const dy = p.y - p2.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 120 && connectionCount < 1) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);

                ctx.strokeStyle =
                    `rgba(0, 132, 148, ${
                        Math.min(p.alpha, p2.alpha) * 0.25
                    })`;

                ctx.lineWidth = 1;
                ctx.stroke();

                connectionCount++;
            }
        }
    }

    animationId = requestAnimationFrame(animate);
}

function startParticles() {
    if (running) return;

    running = true;
    animate();
}

function stopParticles() {
    running = false;

    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
}


// Pause les particules quand la section n'est plus visible
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting && !document.hidden) {
            startParticles();
        } else {
            stopParticles();
        }
    });
});

observer.observe(section);


// Pause si l'utilisateur change d'onglet
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        stopParticles();
    } else {
        const rect = section.getBoundingClientRect();

        if (rect.bottom > 0 && rect.top < window.innerHeight) {
            startParticles();
        }
    }
});


// -------------------------
// LOTTIE
// -------------------------

function loadLottieAnimation(containerId, animationPath, animationName) {
    const container = document.getElementById(containerId);

    if (!container) {
        console.error(`Conteneur #${containerId} introuvable.`);
        return null;
    }

    if (!window.lottie) {
        console.error("Lottie-web n'est pas chargé.");
        return null;
    }

    const animation = lottie.loadAnimation({
        container: container,
        renderer: "svg",
        loop: true,
        autoplay: true,
        path: animationPath,
        name: animationName
    });

    animation.addEventListener("DOMLoaded", () => {
        console.log(`Animation ${animationName} chargée.`);
    });

    animation.addEventListener("data_failed", () => {
        console.error(
            `Impossible de charger : ${animationPath}`
        );
    });

    return animation;
}


// Astronaute
const astronautAnim = loadLottieAnimation(
    "astronaut",
    "./ressources/animations/astronaut.json",
    "astronaut"
);


// Fusée
const rocketAnim = loadLottieAnimation(
    "rocket",
    "./ressources/animations/rocket.json",
    "rocket"
);


// -------------------------
// COMPÉTENCES : UNE SEULE LECTURE
// -------------------------

function loadSkillsAnimation(containerId, animationPath) {
    const container = document.getElementById(containerId);

    if (!container) {
        console.error(`Conteneur #${containerId} introuvable.`);
        return;
    }

    if (!window.lottie) {
        console.error("Lottie-web n'est pas chargé.");
        return;
    }

    let animation = null;
    let ready = false;
    let visible = false;
    let completed = false;

    function updatePlayback() {
        if (!animation || !ready || completed) return;

        if (visible && !document.hidden) {
            animation.play();
        } else {
            animation.pause();
        }
    }

    function stopWatching() {
        visibilityObserver.disconnect();
        document.removeEventListener("visibilitychange", updatePlayback);
    }

    const visibilityObserver = new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting && entry.intersectionRatio >= 0.15;

        // Charge chaque JSON seulement à l'arrivée de l'animation à l'écran.
        if (visible && !animation) {
            animation = lottie.loadAnimation({
                container: container,
                renderer: "svg",
                loop: false,
                autoplay: false,
                path: animationPath,
                name: containerId,
                rendererSettings: {
                    preserveAspectRatio: "xMidYMid meet"
                }
            });

            animation.addEventListener("DOMLoaded", () => {
                ready = true;
                updatePlayback();
            });

            animation.addEventListener("complete", () => {
                completed = true;
                animation.pause();
                stopWatching();

                // La dernière image reste affichée, sans relancer la lecture.
            });

            animation.addEventListener("data_failed", () => {
                completed = true;
                stopWatching();
                console.error(`Impossible de charger : ${animationPath}`);
            });
        }

        // Reprend au même endroit si l'utilisateur revient avant la fin.
        updatePlayback();
    }, { threshold: 0.15 });

    document.addEventListener("visibilitychange", updatePlayback);
    visibilityObserver.observe(container);
}

loadSkillsAnimation(
    "skills-01",
    "./ressources/animations/skills-01.json"
);

loadSkillsAnimation(
    "skills-02",
    "./ressources/animations/skills-02.json"
);


// Pause quand l'onglet n'est plus visible : astronaute et fusée.
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        astronautAnim?.pause();
        rocketAnim?.pause();
    } else {
        astronautAnim?.play();
        rocketAnim?.play();
    }
});


/* =========================================
   DE-ZOOM — RESPONSIVE
   ========================================= */

function updateDesktopZoom() {
    const width = window.innerWidth;
    const scaledContent = document.querySelector(".desktop-scaled-content");

    if (!scaledContent) return;

    const mobileBreakpoint = 768;

    const minWidth = 1481;
    const maxWidth = 2580;

    const minZoom = 0.80;
    const maxZoom = 1;

    // MOBILE : on remonte volontairement l'échelle à 1
    if (width <= mobileBreakpoint) {
        scaledContent.style.zoom = "1";
        return;
    }

    // Entre le mobile et 1290px : zoom minimum desktop
    if (width <= minWidth) {
        scaledContent.style.zoom = String(minZoom);
        return;
    }

    // Très grand écran : taille normale
    if (width >= maxWidth) {
        scaledContent.style.zoom = String(maxZoom);
        return;
    }

    // Dézoom progressif entre 2580px et 1700px
    const progress = (width - minWidth) / (maxWidth - minWidth);

    const zoom =
        minZoom +
        progress * (maxZoom - minZoom);

    scaledContent.style.zoom = String(zoom);
}

updateDesktopZoom();
window.addEventListener("resize", updateDesktopZoom);


// -------------------------
// FORMULAIRE
// -------------------------

const inputFields = document.querySelectorAll("input");

inputFields.forEach((field) => {
    field.addEventListener("input", (event) => {
        event.target.parentNode.classList.toggle(
            "animation",
            event.target.value !== ""
        );
    });
});

const API_BASE_URL =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
        ? "http://localhost:8001"
        : "https://tom-mouquet-portfolio-api.onrender.com";


/* =========================================
   CONTACT FORM
   ========================================= */

const contactForm = document.querySelector("#contact-form");
const contactStatus = document.querySelector("#contact-status");
const contactSubmit = document.querySelector("#contact-submit");

if (contactForm && contactStatus && contactSubmit) {

    contactForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const data = {
            first_name: document.querySelector("#first-name").value.trim(),
            last_name: document.querySelector("#last-name").value.trim(),
            email: document.querySelector("#email").value.trim(),
            company: document.querySelector("#company").value.trim() || null,
            message: document.querySelector("#message").value.trim()
        };

        contactSubmit.disabled = true;
        contactSubmit.textContent = "Sending...";
        contactStatus.textContent = "";

        try {

            const response = await fetch(
                `${API_BASE_URL}/contact`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }
            );

            if (!response.ok) {
                throw new Error("Unable to send message");
            }

            contactStatus.textContent = "Message sent successfully.";
            contactForm.reset();

            contactForm
                .querySelectorAll(".form-groupe.animation")
                .forEach((group) => {
                    group.classList.remove("animation");
                });

        } catch (error) {

            console.error(error);

            contactStatus.textContent =
                "Unable to send message. Please try again.";

        } finally {

            contactSubmit.disabled = false;
            contactSubmit.textContent = "Send";
        }
    });
}