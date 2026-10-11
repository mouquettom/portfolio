from urllib.parse import urljoin, urlparse

import pytest
from playwright.sync_api import Page, expect


# =====================================
# URLS
# =====================================

# Les tests Playwright tournent sur le serveur local du CI.
BASE_URL = "http://127.0.0.1:8000"

# En local, les deux versions restent accessibles depuis le même projet.
PAGES = {
    "en": f"{BASE_URL}/",
    "fr": f"{BASE_URL}/fr/",
}

# En production, chaque langue possède désormais son propre domaine.
PRODUCTION_URLS = {
    "en": "https://tommouquet.com/",
    "fr": "https://tommouquet.fr/",
}

LANGUAGE_SWITCH = {
    "en": {
        "target": PRODUCTION_URLS["fr"],
        "hreflang": "fr",
        "lang": "fr",
        "aria_label": "Version française",
    },
    "fr": {
        "target": PRODUCTION_URLS["en"],
        "hreflang": "en",
        "lang": "en",
        "aria_label": "English version",
    },
}

PROJECT_IDS = [
    "epic-events",
    "softdesk-api",
    "lit-revu",
    "algoinvest",
    "chess-tournament",
    "contact-api",
]

# Structure d'une page : balise, id, classe et projet de chaque élément.
# Les textes et certaines URL peuvent différer d'une langue à l'autre,
# mais la structure visuelle doit rester identique.
#
# Important : Lottie génère dynamiquement des éléments SVG avec des identifiants
# internes (__lottie_element_3, __lottie_element_72, etc.) qui peuvent changer
# d'un chargement à l'autre. On conserve donc les conteneurs Lottie dans la
# comparaison, mais on ignore leurs descendants générés dynamiquement.
STRUCTURE_JS = """
() => {
    const lottieContainerIds = new Set([
        'astronaut',
        'rocket',
        'skills-01',
        'skills-02',
    ]);

    return [...document.querySelectorAll('body *')]
        .filter(el => {
            const lottieContainer = el.closest(
                '#astronaut, #rocket, #skills-01, #skills-02'
            );

            return !lottieContainer || lottieContainerIds.has(el.id);
        })
        .map(el => [
            el.tagName,
            el.id,
            el.getAttribute('class') || '',
            el.getAttribute('data-project') || '',
        ].join('|'));
}
"""


# =====================================
# STRUCTURE (les deux langues)
# =====================================

@pytest.mark.parametrize("lang", PAGES)
def test_homepage_loads(page: Page, lang):
    response = page.goto(PAGES[lang])

    assert response is not None
    assert response.ok
    assert page.locator("html").get_attribute("lang") == lang


@pytest.mark.parametrize("lang", PAGES)
def test_main_sections_exist(page: Page, lang):
    page.goto(PAGES[lang])

    for section_id in ["#accueil", "#about", "#projects", "#exp", "#contact"]:
        assert page.locator(section_id).count() == 1


@pytest.mark.parametrize("lang", PAGES)
def test_navigation_links_exist(page: Page, lang):
    page.goto(PAGES[lang])

    menu = page.locator(".nav-menu")

    for anchor in ["#about", "#projects", "#exp", "#contact"]:
        assert menu.locator(f'a[href="{anchor}"]').count() == 1


@pytest.mark.parametrize("lang", PAGES)
def test_six_projects_are_displayed(page: Page, lang):
    page.goto(PAGES[lang])

    assert page.locator(".container-portfolio .item").count() == 6


@pytest.mark.parametrize("lang", PAGES)
def test_lottie_containers_exist(page: Page, lang):
    page.goto(PAGES[lang])

    for container in ["#astronaut", "#rocket", "#skills-01", "#skills-02"]:
        assert page.locator(container).count() == 1


@pytest.mark.parametrize("lang", PAGES)
def test_journey_contains_four_entries(page: Page, lang):
    page.goto(PAGES[lang])

    assert page.locator(".flex-cont-bloc-exp .bloc").count() == 4


@pytest.mark.parametrize("lang", PAGES)
def test_external_journey_links_open_new_tab(page: Page, lang):
    page.goto(PAGES[lang])

    links = page.locator(".boule-ico")

    assert links.count() == 4

    for i in range(links.count()):
        link = links.nth(i)
        assert link.get_attribute("target") == "_blank"

        rel = link.get_attribute("rel") or ""
        assert "noopener" in rel


def test_english_and_french_pages_have_the_same_structure(page: Page):
    """Une modification de mise en page doit être répercutée dans les deux langues."""
    page.goto(PAGES["en"])
    english = page.evaluate(STRUCTURE_JS)

    page.goto(PAGES["fr"])
    french = page.evaluate(STRUCTURE_JS)

    assert english == french


# =====================================
# LANGUES / SEO
# =====================================

@pytest.mark.parametrize("lang", PAGES)
def test_page_has_correct_canonical_url(page: Page, lang):
    page.goto(PAGES[lang])

    canonical = page.locator('link[rel="canonical"]')
    assert canonical.count() == 1
    assert canonical.get_attribute("href") == PRODUCTION_URLS[lang]


@pytest.mark.parametrize("lang", PAGES)
def test_pages_declare_both_languages(page: Page, lang):
    page.goto(PAGES[lang])

    alternates = {
        "en": PRODUCTION_URLS["en"],
        "fr": PRODUCTION_URLS["fr"],
        "x-default": PRODUCTION_URLS["en"],
    }

    for hreflang, expected_url in alternates.items():
        link = page.locator(
            f'link[rel="alternate"][hreflang="{hreflang}"]'
        )
        assert link.count() == 1
        assert link.get_attribute("href") == expected_url


@pytest.mark.parametrize("lang", PAGES)
def test_automatic_translation_is_disabled(page: Page, lang):
    page.goto(PAGES[lang])

    assert page.locator("html").get_attribute("translate") == "no"

    notranslate = page.locator('meta[name="google"][content="notranslate"]')
    assert notranslate.count() == 1


@pytest.mark.parametrize("lang", PAGES)
def test_language_switch_targets_other_production_domain(page: Page, lang):
    """
    Le CI ne clique pas sur le sélecteur de langue : cela ferait sortir Playwright
    du serveur local pour aller sur le site de production. On vérifie directement
    que le lien cible le bon domaine et possède les bons attributs d'accessibilité.
    """
    page.goto(PAGES[lang])

    switch = page.locator(".lang-switch")
    expected = LANGUAGE_SWITCH[lang]

    assert switch.count() == 1
    assert switch.get_attribute("href") == expected["target"]
    assert switch.get_attribute("hreflang") == expected["hreflang"]
    assert switch.get_attribute("lang") == expected["lang"]
    assert switch.get_attribute("aria-label") == expected["aria_label"]


# =====================================
# CASE STUDIES
# =====================================

@pytest.mark.parametrize("lang", PAGES)
def test_projects_are_in_illustration_order(page: Page, lang):
    """The contact API stays 6th, on the porftolio.jpg illustration."""
    page.goto(PAGES[lang])

    buttons = page.locator(".project-open")
    order = [
        buttons.nth(i).get_attribute("data-project")
        for i in range(buttons.count())
    ]

    assert order == PROJECT_IDS
    assert (
        page.locator(".item")
        .nth(5)
        .locator("img")
        .get_attribute("src")
        .endswith("ressources/porftolio.jpg")
    )


@pytest.mark.parametrize("project_id", PROJECT_IDS)
@pytest.mark.parametrize("lang", PAGES)
def test_each_card_opens_its_case_study(page: Page, lang, project_id):
    page.goto(PAGES[lang])

    dialog = page.locator(f"#{project_id}")
    expect(dialog).to_be_hidden()

    page.locator(f'.project-open[data-project="{project_id}"]').click()

    expect(dialog).to_be_visible()
    expect(
        dialog.locator('a[href^="https://github.com/mouquettom/"]').first
    ).to_be_visible()

    page.keyboard.press("Escape")
    expect(dialog).to_be_hidden()


@pytest.mark.parametrize("lang", PAGES)
def test_case_study_opens_from_direct_link(page: Page, lang):
    page.goto(f"{PAGES[lang]}#epic-events")

    expect(page.locator("#epic-events")).to_be_visible()


# =====================================
# LIENS ET RESSOURCES
# =====================================

@pytest.mark.parametrize("lang", PAGES)
def test_local_links_and_assets_are_not_broken(page: Page, lang):
    """
    Images, CSS, scripts, liens internes et CV doivent répondre HTTP 200.

    Les URL absolues vers tommouquet.com / tommouquet.fr et les autres sites
    externes sont volontairement ignorées : ce test concerne uniquement les
    ressources servies par le serveur local du CI.
    """
    page.goto(PAGES[lang])

    urls = page.eval_on_selector_all(
        "img[src], link[href], script[src], a[href]",
        "elements => elements.map(e => e.getAttribute('src') || e.getAttribute('href'))",
    )

    local_urls = set()
    local_netloc = urlparse(BASE_URL).netloc

    for url in urls:
        if not url:
            continue

        absolute = urljoin(page.url, url)

        if urlparse(absolute).netloc != local_netloc:
            continue

        local_urls.add(absolute.split("#")[0])

    assert local_urls

    for url in sorted(local_urls):
        response = page.request.get(url)
        assert response.ok, f"{url} -> HTTP {response.status}"


@pytest.mark.parametrize("lang", PAGES)
def test_animations_load_from_both_pages(page: Page, lang):
    """The Lottie files resolve from / and from /fr/."""
    failed = []

    page.on(
        "response",
        lambda response: (
            failed.append(response.url)
            if "animations" in response.url and not response.ok
            else None
        ),
    )

    page.goto(PAGES[lang])
    page.locator(".skills-animations").scroll_into_view_if_needed()
    page.wait_for_timeout(1500)

    assert failed == []
    assert page.locator("#astronaut svg").count() == 1
    assert page.locator("#skills-01 svg").count() == 1
