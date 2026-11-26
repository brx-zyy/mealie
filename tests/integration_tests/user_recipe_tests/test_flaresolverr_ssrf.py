import os
from urllib.parse import urlparse

from mealie.core.config import get_app_settings
from tests.utils import api_routes
from tests.utils.fixture_schemas import TestUser


def test_authenticated_recipe_import_follows_flaresolverr_redirect_into_private_network(
    api_client, unique_user: TestUser
):
    """Exercise authenticated URL import from a public, non-allowlisted challenge host."""
    settings = get_app_settings()
    public_url = os.environ["SSRF_PROOF_PUBLIC_URL"]
    public_host = urlparse(public_url).hostname
    assert settings.SCRAPER_FLARESOLVERR_URL
    assert public_host
    assert public_host not in settings.http_allow_list, (
        f"Challenge host unexpectedly allowlisted: {public_host}"
    )

    response = api_client.post(
        api_routes.recipes_create_url,
        json={"url": public_url, "includeTags": False},
        headers=unique_user.token,
    )
    assert response.status_code == 201, response.text
    slug = response.json()

    imported = api_client.get(api_routes.recipes_slug(slug), headers=unique_user.token)
    assert imported.status_code == 200, imported.text
    recipe = imported.json()
    print("Authenticated import endpoint status:", response.status_code)
    print("Public non-allowlisted challenge host:", public_host)
    print("Created recipe slug:", slug)
    print("Imported recipe name:", recipe["name"])
    assert recipe["name"] == "INTERNAL_ONLY_PROOF_MARKER_7f31c9"
