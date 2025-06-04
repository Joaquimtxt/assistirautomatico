import time
from playwright.sync_api import sync_playwright


# Initial configuration
# Change to your login details and video URLs

EMAIL = "email@example.com"
SENHA = "password123"

video_urls = [
    "https://www.example.com/video1",
    "https://www.example.com/video2",
    "https://www.example.com/video3"
]

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def wait_video_finish(frame):
    print("⏳ Waiting the video finishes or lock for 30 seconds...")
    paused_for = 0
    last_time = 0
    while True:
        try:
            current = frame.evaluate("document.querySelector('video')?.currentTime || 0")
            duration = frame.evaluate("document.querySelector('video')?.duration || 0")
        except Exception as e:
            print(f"⚠️ Error getting progress: {e}")
            break

        print(f"⏱️ Progress: {current:.2f} / {duration:.2f} | Stuck for: {paused_for}s")

        if abs(current - last_time) < 0.1:
            paused_for += 5
        else:
            paused_for = 0

        last_time = current

        if paused_for >= 30:
            print("⚠️ Video stuck for 30 seconds. Skipping to the next.")
            break

        if duration > 0 and (duration - current) < 1 and current > 0:
            print("✅ Video finished successfully.")
            break

        time.sleep(5)

with sync_playwright() as p:
    user_data_dir = "C:/temp/playwright-user-data"
    browser = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        executable_path=chrome_path,
        headless=False,
        args=[
            "--start-maximized",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--disable-features=PreloadMediaEngagementData,AutoplayIgnoreWebAudio,MediaSessionService",
            "--autoplay-policy=no-user-gesture-required"
        ]
    )

    page = browser.pages[0]
    page.set_viewport_size({"width": 1920, "height": 1080})

    for url in video_urls:
        print(f"Opening: {url}")
        page.goto(url)

        # Automatic login if needed
        if "login" in page.url or page.locator("input[name='email']").is_visible():
            print("🔐 Login screen detected. Logging in...")
            page.fill("input[name='email']", EMAIL)
            page.fill("input[name='password']", SENHA)
            page.keyboard.press("Enter")
            page.wait_for_timeout(3000)
            page.wait_for_selector("text=Meus Cursos", timeout=15000)
            print("✅ Login successful. Reloading video...")
            page.goto(url)
            page.wait_for_timeout(5000)

        # Close pop-up
        try:
            popup = page.locator("text=Entenda como funciona")
            popup.wait_for(timeout=5000)
            print("🟢 Pop-up detected.")
            checkbox = page.locator("input[type='checkbox']")
            if checkbox.is_visible():
                checkbox.check()
            close = page.locator("button:has-text('FECHAR')")
            if close.is_visible():
                close.click()
                print("🧼 Pop-up closed.")
        except Exception as e:
            print(f"ℹ️ No pop-up detected. ({e})")


        # Force autoplay attempt and remove overlays
        try:
            page.evaluate("""
                let v = document.querySelector('video');
                if (v) {
                    v.currentTime = 0;
                    v.muted = false;
                    v.volume = 1.0;
                    v.autoplay = true;
                    v.playsInline = true;
                    v.style.display = '';
                    v.play().catch(()=>{});
                }
                let overlays = document.querySelectorAll('[style*="z-index"]');
                overlays.forEach(o => { if(o !== v) o.style.display = "none"; });
            """)
            time.sleep(1)
            try:
                page.click("video", timeout=3000, force=True)
                print("🖱️ Forced click on video to attempt autoplay.")
            except Exception:
                pass
            for attempt in range(4):
                is_playing = page.evaluate("document.querySelector('video')?.paused === false")
                if not is_playing:
                    print(f"▶️ Trying to start video... (attempt {attempt+1})")
                    page.evaluate("document.querySelector('video')?.play().catch(()=>{})")
                    time.sleep(2)
                else:
                    print("🎬 VVideo is already playing.")
                    break
        except Exception as e:
            print(f"⚠️ Error forcing play: {e}")

        # Wait for the Panda Video iframe
        try:
            page.wait_for_selector("iframe[src*='pandavideo']", timeout=30000)
            iframe_element = page.query_selector("iframe[src*='pandavideo']")
            frame = iframe_element.content_frame()

            # Wait for the video to load inside the iframe
            frame.wait_for_selector("video", timeout=20000)
            print("🎥 VVideo found inside the iframe.")

            frame.evaluate("""
                let v = document.querySelector('video');
                if (v) {
                    v.currentTime = 0;
                    v.muted = false;
                    v.volume = 1.0;
                    v.autoplay = true;
                    v.playsInline = true;
                    v.play().catch(()=>{});
                }
            """)

            wait_video_finish(frame)

        except Exception as e:
            print(f"❌ Error processing video in iframe: {e}")

        print("➡️ Next video...\n")
        time.sleep(5)

    browser.close()

print("🏁 All videos have been successfully played.")
