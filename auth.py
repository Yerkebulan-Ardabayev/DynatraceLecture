"""
Interactive login to Dynatrace SaaS tenant.
Saves storage_state.json so subsequent crawler runs don't need to re-login.

Usage:
    python auth.py            # headed browser, авто-ввод DT_LOGIN/DT_PASSWORD из .env, ждёт MFA
    python auth.py --manual   # headed, БЕЗ .env-креденшелов: логинишься руками, сессия сохраняется
    python auth.py --headless # try without showing browser (no MFA support)
"""
import os
import sys
import asyncio
import argparse
from pathlib import Path
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent
TENANT_URL = os.getenv("DT_TENANT", "https://guu84124.live.dynatrace.com").rstrip("/")
LOGIN = os.getenv("DT_LOGIN")
PASSWORD = os.getenv("DT_PASSWORD")
STATE_FILE = ROOT / "state" / "storage_state.json"


async def login(headless: bool = False, mfa_wait_seconds: int = 180, manual: bool = False):
    # --manual: креденшелы не нужны, весь вход (email/пароль/MFA) делает человек
    # руками в открытом окне. Иначе email/пароль подставляются из .env.
    if not manual and (not LOGIN or not PASSWORD):
        print("ERROR: DT_LOGIN / DT_PASSWORD not set in .env "
              "(или запусти `python auth.py --manual` и залогинься руками)", file=sys.stderr)
        sys.exit(1)
    if manual and headless:
        print("ERROR: --manual несовместим с --headless (нужно окно для ручного входа).", file=sys.stderr)
        sys.exit(1)

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        print(f"[auth] -> {TENANT_URL}")
        await page.goto(TENANT_URL, wait_until="domcontentloaded", timeout=60000)
        try:
            await page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass
        print(f"[auth] landed at {page.url}")

        if manual:
            print("[auth] MANUAL: залогинься в открывшемся окне (email + пароль + MFA). "
                  f"Жду до {mfa_wait_seconds}s появления тенанта.")

        # ---- Auto-fill (пропускается целиком в manual: email/пароль вводит человек) ----
        if not manual:
            # ---- Email step ----
            try:
                email = page.locator(
                    'input[type="email"], input[name="username"], input[name="email"], input#email'
                ).first
                await email.wait_for(timeout=15000)
                await email.fill(LOGIN)
                print("[auth] email filled")

                nxt = page.locator(
                    'button:has-text("Next"), button:has-text("Continue"), button:has-text("Далее"), button[type="submit"]'
                ).first
                if await nxt.count():
                    await nxt.click()
                else:
                    await email.press("Enter")
            except Exception as e:
                print(f"[auth] email step skipped: {e}")

            # ---- Password step ----
            try:
                pwd = page.locator('input[type="password"]').first
                await pwd.wait_for(timeout=20000)
                await pwd.fill(PASSWORD)
                print("[auth] password filled")
                sub = page.locator(
                    'button:has-text("Sign in"), button:has-text("Log in"), button:has-text("Войти"), button[type="submit"]'
                ).first
                if await sub.count():
                    await sub.click()
                else:
                    await pwd.press("Enter")
            except Exception as e:
                print(f"[auth] password step issue: {e}")

        # ---- Wait for tenant page (handles MFA: user enters code in browser) ----
        print(f"[auth] waiting up to {mfa_wait_seconds}s for tenant. If MFA appears — enter code in the browser.")
        try:
            await page.wait_for_url(
                lambda url: "live.dynatrace.com" in url and "sso" not in url and "login" not in url.lower(),
                timeout=mfa_wait_seconds * 1000,
            )
        except Exception:
            print(f"[auth] timeout waiting. current url: {page.url}")
            print("[auth] If you see the tenant in the browser anyway — press ENTER here to save session.")
            try:
                input()
            except EOFError:
                pass

        try:
            await page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass

        await context.storage_state(path=str(STATE_FILE))
        print(f"[auth] OK. session saved -> {STATE_FILE}")
        await browser.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--manual", action="store_true",
                    help="ручной вход в окне (без DT_LOGIN/DT_PASSWORD в .env), поддерживает MFA")
    ap.add_argument("--mfa-wait", type=int, default=180, help="seconds to wait after submit for MFA / nav")
    args = ap.parse_args()
    asyncio.run(login(headless=args.headless, mfa_wait_seconds=args.mfa_wait, manual=args.manual))


if __name__ == "__main__":
    main()
