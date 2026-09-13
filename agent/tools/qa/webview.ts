// Browser QA for titian-web on Bun's built-in headless browser
// (Bun.WebView, Bun >= 1.4) — no Playwright install to lose on a reboot.
//
// Linux has no WebKit backend, so this drives Chrome over CDP. It always
// SPAWNS a fresh headless Chrome (`url: false`): left to auto-detect, Bun
// attaches to any Chrome already running with remote debugging, which on
// a dev machine can be the developer's own browser and its logged-in
// sessions.
//
// Auth: titian-web has no dev login. A session is a raw refresh token in
// localStorage["titian-auth"] (see the QA-access recipe in memory); the
// app exchanges it on first load. `login()` plants it on the origin
// before the real navigation.

// Known quirk (Bun 1.4.0, Chrome backend): `view.title` returns non-ASCII
// characters still escaped ("Titian Asa \\u2014 ..."). Read
// `await view.evaluate("document.title")` when the title matters.

export const WEB = process.env.TITIAN_WEB ?? "http://localhost:3000";

export function openView(width = 1440, height = 1000): Bun.WebView {
  return new Bun.WebView({
    width,
    height,
    backend: { type: "chrome", url: false },
    console: (type, ...args) => {
      if (type === "error") console.error("[page]", ...args);
    },
  });
}

export async function login(view: Bun.WebView, rawRefreshToken: string): Promise<void> {
  // The auth store (zustand `persist`) hydrates from localStorage
  // SYNCHRONOUSLY the moment its module first runs on a page — by the
  // time a plain `view.navigate()` + `view.evaluate(...setItem...)`
  // gets to write the token, the store already hydrated empty and its
  // SessionBootstrap effect already fired `clear()`. Setting it
  // afterward is too late; it needs to be there BEFORE the page's own
  // scripts run, on every navigation — the same job Playwright's
  // `addInitScript` does. `view.cdp()` needs one navigate first to open
  // a CDP session (see WebView's own docs), so this makes exactly two:
  // the first (throwaway, unauthenticated) opens the session so the
  // init script can be registered; the second is the real navigation,
  // now with the init script in place ahead of the page's own JS.
  await view.navigate(`${WEB}/`);
  const payload = JSON.stringify(JSON.stringify({ state: { refreshToken: rawRefreshToken }, version: 0 }));
  await view.cdp("Page.addScriptToEvaluateOnNewDocument", {
    source: `localStorage.setItem("titian-auth", ${payload});`,
  });
  await view.navigate(`${WEB}/`);
}

/** Poll a page-side boolean expression until true (Next dev's first
 *  compile of a route can take ~35s, hence the generous default). */
export async function waitFor(view: Bun.WebView, expression: string, timeoutMs = 120_000): Promise<void> {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    if (await view.evaluate<boolean>(`!!(${expression})`).catch(() => false)) return;
    await Bun.sleep(500);
  }
  throw new Error(`timed out waiting for: ${expression}`);
}

/** Page-side expression finding the first element whose text contains
 *  `text` — for waiting on / scrolling to visible copy, the way a person
 *  finds things on the page. */
export function byText(text: string, tag = "*"): string {
  return `[...document.querySelectorAll(${JSON.stringify(tag)})].reverse().find(el => el.textContent?.includes(${JSON.stringify(text)}) && el.children.length < 50)`;
}

/** Screenshot the viewport, or just one element when `elementExpr` is a
 *  page-side expression returning it (scrolled into view first). */
export async function shot(view: Bun.WebView, path: string, elementExpr?: string, padding = 8): Promise<void> {
  if (!elementExpr) {
    await Bun.write(path, await view.screenshot());
    return;
  }
  const box = await view.evaluate<{ x: number; y: number; width: number; height: number } | null>(`(() => {
    const el = ${elementExpr};
    if (!el) return null;
    el.scrollIntoView({ block: "center", behavior: "instant" });
    const r = el.getBoundingClientRect();
    return { x: r.x + scrollX, y: r.y + scrollY, width: r.width, height: r.height };
  })()`);
  if (!box) throw new Error(`element not found for screenshot: ${elementExpr}`);
  await Bun.sleep(300);
  const { data } = await view.cdp<{ data: string }>("Page.captureScreenshot", {
    format: "png",
    captureBeyondViewport: true,
    clip: { x: Math.max(box.x - padding, 0), y: Math.max(box.y - padding, 0), width: box.width + padding * 2, height: box.height + padding * 2, scale: 1 },
  });
  await Bun.write(path, Buffer.from(data, "base64"));
}
