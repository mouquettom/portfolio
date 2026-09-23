from playwright.sync_api import Page


BASE_URL = "http://127.0.0.1:8000"


def test_homepage_loads(page: Page):
    response = page.goto(BASE_URL)

    assert response is not None
    assert response.ok


def test_main_sections_exist(page: Page):
    page.goto(BASE_URL)

    assert page.locator("#accueil").count() == 1
    assert page.locator("#about").count() == 1
    assert page.locator("#projects").count() == 1
    assert page.locator("#exp").count() == 1
    assert page.locator("#contact").count() == 1


def test_navigation_links_exist(page: Page):
    page.goto(BASE_URL)

    assert page.locator('a[href="#about"]').count() == 1
    assert page.locator('a[href="#projects"]').count() == 1
    assert page.locator('a[href="#exp"]').count() == 1
    assert page.locator('a[href="#contact"]').count() == 1


def test_six_projects_are_displayed(page: Page):
    page.goto(BASE_URL)

    projects = page.locator(".container-portfolio .item")

    assert projects.count() == 6


def test_lottie_containers_exist(page: Page):
    page.goto(BASE_URL)

    assert page.locator("#astronaut").count() == 1
    assert page.locator("#rocket").count() == 1
    assert page.locator("#skills-01").count() == 1
    assert page.locator("#skills-02").count() == 1


def test_journey_contains_four_entries(page: Page):
    page.goto(BASE_URL)

    entries = page.locator(".flex-cont-bloc-exp .bloc")

    assert entries.count() == 4


def test_external_journey_links_open_new_tab(page: Page):
    page.goto(BASE_URL)

    links = page.locator(".boule-ico")

    assert links.count() == 4

    for i in range(links.count()):
        assert links.nth(i).get_attribute("target") == "_blank"
        assert "noopener" in links.nth(i).get_attribute("rel")
