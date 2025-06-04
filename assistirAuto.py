import time
from playwright.sync_api import sync_playwright

EMAIL = "email@example.com"
SENHA = "password123"

video_urls = [
    "https://www.example.com/video1",
    "https://www.example.com/video2",
    "https://www.example.com/video3"
]

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def aguardar_video_terminar(frame):
    print("⏳ Aguardando o vídeo terminar ou travar por 30 segundos...")
    pausado_ha = 0
    ultimo_tempo = 0
    while True:
        try:
            current = frame.evaluate("document.querySelector('video')?.currentTime || 0")
            duration = frame.evaluate("document.querySelector('video')?.duration || 0")
        except Exception as e:
            print(f"⚠️ Erro ao obter progresso: {e}")
            break

        print(f"⏱️ Progresso: {current:.2f} / {duration:.2f} | Parado há: {pausado_ha}s")

        if abs(current - ultimo_tempo) < 0.1:
            pausado_ha += 5
        else:
            pausado_ha = 0

        ultimo_tempo = current

        if pausado_ha >= 30:
            print("⚠️ Vídeo travado por 30 segundos. Pulando para o próximo.")
            break

        if duration > 0 and (duration - current) < 1 and current > 0:
            print("✅ Vídeo finalizado com sucesso.")
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
        print(f"Abrindo: {url}")
        page.goto(url)

        # Login automático
        if "login" in page.url or page.locator("input[name='email']").is_visible():
            print("🔐 Tela de login detectada. Fazendo login...")
            page.fill("input[name='email']", EMAIL)
            page.fill("input[name='password']", SENHA)
            page.keyboard.press("Enter")
            page.wait_for_timeout(3000)
            page.wait_for_selector("text=Meus Cursos", timeout=15000)
            print("✅ Login realizado. Recarregando vídeo...")
            page.goto(url)
            page.wait_for_timeout(5000)

        # Fechar pop-up
        try:
            popup = page.locator("text=Entenda como funciona")
            popup.wait_for(timeout=5000)
            print("🟢 Pop-up detectado.")
            checkbox = page.locator("input[type='checkbox']")
            if checkbox.is_visible():
                checkbox.check()
            fechar = page.locator("button:has-text('FECHAR')")
            if fechar.is_visible():
                fechar.click()
                print("🧼 Pop-up fechado.")
        except Exception as e:
            print(f"ℹ️ Nenhum pop-up detectado. ({e})")


        # Força tentativa de autoplay e remove overlays
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
                print("🖱️ Clique forçado no vídeo para tentar autoplay.")
            except Exception:
                pass
            for tentativa in range(4):
                is_playing = page.evaluate("document.querySelector('video')?.paused === false")
                if not is_playing:
                    print(f"▶️ Tentando iniciar o vídeo... (tentativa {tentativa+1})")
                    page.evaluate("document.querySelector('video')?.play().catch(()=>{})")
                    time.sleep(2)
                else:
                    print("🎬 Vídeo já está tocando.")
                    break
        except Exception as e:
            print(f"⚠️ Erro ao forçar play: {e}")

        # Esperar o iframe do Panda Vídeo
        try:
            page.wait_for_selector("iframe[src*='pandavideo']", timeout=30000)
            iframe_element = page.query_selector("iframe[src*='pandavideo']")
            frame = iframe_element.content_frame()

            # Espera o vídeo carregar dentro do iframe
            frame.wait_for_selector("video", timeout=20000)
            print("🎥 Vídeo encontrado dentro do iframe.")

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

            aguardar_video_terminar(frame)

        except Exception as e:
            print(f"❌ Erro ao processar vídeo no iframe: {e}")

        print("➡️ Próximo vídeo...\n")
        time.sleep(5)

    browser.close()

print("🏁 Todos os vídeos foram executados com sucesso.")
