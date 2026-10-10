// -------------------------
// LANGUE ET RESSOURCES
// -------------------------

// "en" sur tommouquet.com/, "fr" sur tommouquet.com/fr/ (lu dans <html lang>)
const LANG = document.documentElement.lang.startsWith("fr") ? "fr" : "en";

// Dossier du script : les chemins des animations restent justes depuis /fr/
const ASSET_BASE = new URL(".", document.currentScript.src);

function assetUrl(path) {
    return new URL(path, ASSET_BASE).href;
}

const MESSAGES = {
    en: {
        send: "Send",
        sending: "Sending...",
        sent: "Message sent successfully.",
        error: "Unable to send message. Please try again.",
    },
    fr: {
        send: "Envoyer",
        sending: "Envoi...",
        sent: "Message envoyé, merci !",
        error: "Le message n'a pas pu être envoyé. Veuillez réessayer.",
    },
}[LANG];


// -------------------------
// SÉLECTEUR DE LANGUE
// -------------------------

// On arrive dans l'autre langue sur la section que l'on lisait
document.querySelectorAll(".lang-switch").forEach((link) => {
    link.addEventListener("click", () => {
        const sections = [...document.querySelectorAll("main section[id]")];
        const current = sections
            .filter((section) => section.getBoundingClientRect().top <= window.innerHeight * 0.35)
            .pop();

        const base = link.getAttribute("href").split("#")[0];

        link.setAttribute(
            "href",
            current && current.id !== "accueil" ? `${base}#${current.id}` : base
        );
    });
});


// -------------------------
// PRÉFÉRENCES
// -------------------------

// Respecte le réglage système « Réduire les animations »
const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
).matches;


// -------------------------
// MENU MOBILE
// -------------------------

const navBar = document.querySelector(".nav-bar");
const navToggle = document.querySelector(".nav-toggle");
const navPanel = document.querySelector("#nav-panel");

function setMenuOpen(open) {
    navBar.classList.toggle("is-open", open);
    navToggle.setAttribute("aria-expanded", String(open));
    const labels = LANG === "fr"
        ? ["Fermer le menu", "Ouvrir le menu"]
        : ["Close menu", "Open menu"];

    navToggle.setAttribute("aria-label", open ? labels[0] : labels[1]);
}

if (navBar && navToggle && navPanel) {

    navToggle.addEventListener("click", () => {
        setMenuOpen(!navBar.classList.contains("is-open"));
    });

    // Un lien choisi : le panneau se ferme
    navPanel.addEventListener("click", (event) => {
        if (event.target.closest("a")) {
            setMenuOpen(false);
        }
    });

    // Clic en dehors du header
    document.addEventListener("click", (event) => {
        if (!navBar.contains(event.target)) {
            setMenuOpen(false);
        }
    });

    // Échap : ferme et rend le focus au bouton
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && navBar.classList.contains("is-open")) {
            setMenuOpen(false);
            navToggle.focus();
        }
    });

    // Retour à une largeur où le menu complet s'affiche : on réinitialise
    window.matchMedia("(min-width: 901px)").addEventListener("change", (event) => {
        if (event.matches) {
            setMenuOpen(false);
        }
    });
}


// -------------------------
// PARTICULES
// -------------------------

const section = document.getElementById("accueil");
const canvas = document.getElementById("particles-canvas");
const ctx = canvas.getContext("2d");

let particles = [];
let animationId = null;
let running = false;

let canvasWidth = 0;
let canvasHeight = 0;

// Dessine en pixels physiques : particules nettes sur écran Retina
function resizeCanvasToSection() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);

    canvasWidth = section.clientWidth;
    canvasHeight = section.clientHeight;

    canvas.width = Math.round(canvasWidth * ratio);
    canvas.height = Math.round(canvasHeight * ratio);

    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
}

// Suit la taille réelle de la section (rotation, fenêtre redimensionnée…)
new ResizeObserver(resizeCanvasToSection).observe(section);

section.addEventListener("mousemove", (e) => {
    if (reduceMotion) return;

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

    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

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
    if (running || reduceMotion) return;

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

// Joue une animation seulement quand elle est à l'écran
// et que l'onglet est actif (batterie et CPU épargnés sur mobile).
function playWhenVisible(animation, element) {
    let ready = false;
    let visible = false;

    function update() {
        if (!ready) return;

        if (visible && !document.hidden) {
            animation.play();
        } else {
            animation.pause();
        }
    }

    animation.addEventListener("DOMLoaded", () => {
        ready = true;
        update();
    });

    new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        update();
    }).observe(element);

    document.addEventListener("visibilitychange", update);
}


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
        autoplay: false,
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

    if (reduceMotion) {
        // Image fixe à la place de la boucle
        animation.addEventListener("DOMLoaded", () => {
            animation.goToAndStop(0, true);
        });
    } else {
        playWhenVisible(animation, container);
    }

    return animation;
}


// Astronaute
loadLottieAnimation(
    "astronaut",
    assetUrl("ressources/animations/astronaut.json"),
    "astronaut"
);


// Fusée
loadLottieAnimation(
    "rocket",
    assetUrl("ressources/animations/rocket.json"),
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

                if (reduceMotion) {
                    // Affiche directement le schéma complet
                    animation.goToAndStop(animation.totalFrames - 1, true);
                    completed = true;
                    stopWatching();
                    return;
                }

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
    assetUrl("ressources/animations/skills-01.json")
);

loadSkillsAnimation(
    "skills-02",
    assetUrl("ressources/animations/skills-02.json")
);


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

const CONTACT_API_URL =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
        ? "http://localhost:8001/contact"
        : "https://api.tommouquet.com/contact";


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
        contactSubmit.textContent = MESSAGES.sending;
        contactStatus.textContent = "";

        try {

            const response = await fetch(CONTACT_API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error("Unable to send message");
            }

            contactStatus.textContent = MESSAGES.sent;
            contactForm.reset();

            contactForm
                .querySelectorAll(".form-groupe.animation")
                .forEach((group) => {
                    group.classList.remove("animation");
                });

        } catch (error) {

            console.error(error);

            contactStatus.textContent = MESSAGES.error;

        } finally {

            contactSubmit.disabled = false;
            contactSubmit.textContent = MESSAGES.send;
        }
    });
}


/* =========================================
   CASE STUDIES (fiches projet)
   Une carte ouvre sa fiche (<dialog>).
   Lien direct partageable : tommouquet.com/#epic-events
   ========================================= */

let lastProjectOpener = null;

function openProject(projectId, opener) {
    const dialog = document.getElementById(projectId);

    if (!dialog || !dialog.classList.contains("project-dialog")) return;

    // Navigateur trop ancien : on envoie vers le code sur GitHub
    if (typeof dialog.showModal !== "function") {
        const codeLink = dialog.querySelector(".dialog-actions a");
        if (codeLink) window.open(codeLink.href, "_blank", "noopener");
        return;
    }

    lastProjectOpener = opener || null;

    dialog.showModal();
    dialog.scrollTop = 0;

    history.replaceState(null, "", `#${projectId}`);
}

document.querySelectorAll(".project-open").forEach((button) => {
    button.addEventListener("click", () => {
        openProject(button.dataset.project, button);
    });
});

document.querySelectorAll(".project-dialog").forEach((dialog) => {

    dialog.addEventListener("click", (event) => {

        // Clic sur le fond assombri ou sur la croix
        if (event.target === dialog || event.target.closest(".dialog-close")) {
            dialog.close();
            return;
        }

        // Lien interne (« Try the form ») : on ferme puis on suit le lien
        if (event.target.closest("[data-close-dialog]")) {
            lastProjectOpener = null;
            dialog.close();
        }
    });

    dialog.addEventListener("close", () => {

        if (location.hash === `#${dialog.id}`) {
            history.replaceState(null, "", location.pathname + location.search);
        }

        // Le focus revient sur la carte qui a ouvert la fiche
        if (lastProjectOpener) {
            lastProjectOpener.focus({ preventScroll: true });
            lastProjectOpener = null;
        }
    });
});

// Ouverture directe depuis l'URL
const initialProject = location.hash.slice(1);

if (initialProject) {
    openProject(
        initialProject,
        document.querySelector(`.project-open[data-project="${CSS.escape(initialProject)}"]`)
    );
}
