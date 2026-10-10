from urllib.parse import urljoin, urlparse

import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:8000"

PAGES = {
    "en": f"{BASE_URL}/",
    "fr": f"{BASE_URL}/fr/",
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
# Les textes peuvent différer d'une langue à l'autre, la structure jamais.
STRUCTURE_JS = """
() => [...document.querySelectorAll('body *')].map(el => [
    el.tagName,
    el.id,
    el.getAttribute('class') || '',
    el.getAttribute('data-project') || '',
].join('|'))
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
        assert links.nth(i).get_attribute("target") == "_blank"
        assert "noopener" in links.nth(i).get_attribute("rel")


def test_english_and_french_pages_have_the_same_structure(page: Page):
    """Une modification de mise en page doit être faite dans les deux langues."""
    page.goto(PAGES["en"])
    english = page.evaluate(STRUCTURE_JS)

    page.goto(PAGES["fr"])
    french = page.evaluate(STRUCTURE_JS)

    assert english == french


# =====================================
# LANGUES
# =====================================

@pytest.mark.parametrize("lang", PAGES)
def test_pages_declare_both_languages(page: Page, lang):
    page.goto(PAGES[lang])

    assert page.locator('link[rel="alternate"][hreflang="en"]').count() == 1
    assert page.locator('link[rel="alternate"][hreflang="fr"]').count() == 1


def test_language_switch_goes_both_ways(page: Page):
    page.goto(PAGES["en"])
    page.locator(".lang-switch").click()
    expect(page).to_have_url(PAGES["fr"])

    page.locator(".lang-switch").click()
    expect(page).to_have_url(PAGES["en"])


def test_language_switch_keeps_the_current_section(page: Page):
    page.goto(PAGES["en"])
    page.locator("#projects").scroll_into_view_if_needed()
    page.evaluate("document.querySelector('#projects').scrollIntoView({behavior: 'instant'})")

    page.locator(".lang-switch").click()

    expect(page).to_have_url(f"{PAGES['fr']}#projects")


# =====================================
# CASE STUDIES
# =====================================

@pytest.mark.parametrize("lang", PAGES)
def test_projects_are_in_illustration_order(page: Page, lang):
    """The contact API stays 6th, on the porftolio.jpg illustration."""
    page.goto(PAGES[lang])

    buttons = page.locator(".project-open")
    order = [buttons.nth(i).get_attribute("data-project") for i in range(buttons.count())]

    assert order == PROJECT_IDS
    assert page.locator(".item").nth(5).locator("img").get_attribute("src").endswith("ressources/porftolio.jpg")


@pytest.mark.parametrize("project_id", PROJECT_IDS)
@pytest.mark.parametrize("lang", PAGES)
def test_each_card_opens_its_case_study(page: Page, lang, project_id):
    page.goto(PAGES[lang])

    dialog = page.locator(f"#{project_id}")
    expect(dialog).to_be_hidden()

    page.locator(f'.project-open[data-project="{project_id}"]').click()

    expect(dialog).to_be_visible()
    expect(dialog.locator('a[href^="https://github.com/mouquettom/"]').first).to_be_visible()

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
    """Images, CSS, scripts, internal links and the CV answer HTTP 200."""
    page.goto(PAGES[lang])

    urls = page.eval_on_selector_all(
        "img[src], link[href], script[src], a[href]",
        "elements => elements.map(e => e.getAttribute('src') || e.getAttribute('href'))",
    )

    local_urls = set()

    for url in urls:
        absolute = urljoin(page.url, url)

        if urlparse(absolute).netloc != urlparse(BASE_URL).netloc:
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
    page.on("response", lambda r: failed.append(r.url) if "animations" in r.url and not r.ok else None)

    page.goto(PAGES[lang])
    page.locator(".skills-animations").scroll_into_view_if_needed()
    page.wait_for_timeout(1500)

    assert failed == []
    assert page.locator("#astronaut svg").count() == 1
    assert page.locator("#skills-01 svg").count() == 1
