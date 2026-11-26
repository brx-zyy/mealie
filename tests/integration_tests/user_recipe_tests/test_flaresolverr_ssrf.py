from mealie.core.config import get_app_settings
from tests.utils.fixture_schemas import TestUser


def test_authenticated_recipe_import_follows_flaresolverr_redirect_into_private_network(
    api_client, unique_user: TestUser
):
    """Exercise the real authenticated URL-import endpoint, not just resilient_fetch."""
    settings = get_app_settings()
    assert settings.SCRAPER_FLARESOLVERR_URL
    assert "attacker-proof" in settings.http_allow_list

    response = api_client.post(
        "/api/recipes/create/url",
        json={"url": "http://attacker-proof:8080/challenge", "includeTags": False},
        headers=unique_user.token,
    )
    assert response.status_code == 201, response.text
    slug = response.json()

    imported = api_client.get(f"/api/recipes/{slug}", headers=unique_user.token)
    assert imported.status_code == 200, imported.text
    recipe = imported.json()
    print("Authenticated import endpoint status:", response.status_code)
    print("Created recipe slug:", slug)
    print("Imported recipe name:", recipe["name"])
    assert recipe["name"] == "INTERNAL_ONLY_PROOF_MARKER_7f31c9"
