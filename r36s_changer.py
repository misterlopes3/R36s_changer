import os
import sys
import shutil
import re
import zipfile
import urllib.parse
import requests
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import psutil
from PIL import Image, ImageTk, ImageDraw
from fuzzywuzzy import process
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURAÇÃO DO AUTO-UPDATE ---
VERSAO_ATUAL = "1.3"
# ⚠️ IMPORTANTE: Substitui 'MIGUEL_LOPES' e 'R36S_ASSISTANT_REPO' pelos teus dados reais do GitHub
GITHUB_USER = "MIGUEL_LOPES"
GITHUB_REPO = "R36S_ASSISTANT_REPO"

URL_VERSAO_REMOTA = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/versao.txt"
URL_CODIGO_REMOTOS = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/assistente.py"

# --- DICIONÁRIO DE IDIOMAS ---
IDIOMA_ATUAL = "PT"

TEXTOS = {
    "PT": {
        "title": "Assistente Ultimate G80CA-MB V1.3 + Fixed Scraper",
        "tab_logo": "  🖼️ Boot Logo  ",
        "tab_jogos": "  🎮 Jogos e Capas  ",
        "tab_temas": "  🎨 Temas ES  ",
        "tab_drivers": "  🖥️ Drivers Ecrã  ",
        
        "logo_tit": "Altere o seu logo do seu R36s e diversos",
        "logo_sub": "Altere o splash screen estático que aparece ao ligar a consola portátil.",
        "btn_proc": "🔍 Procurar Ficheiro",
        "chk_rot": "🛠️ Tens a certeza que desejas aplicar o logo?",
        "btn_gravar": "💾  GRAVAR NOVO LOGO NO CARTÃO SD",
        
        "lbl_sis": "🔍 Sistema:",
        "lbl_dir": "Diretório:",
        "btn_scrap": "🌐 Scraper Automatizado",
        "status_analise": "A analisar barramento de armazenamento local...",
        "col_nome": "Ficheiro / ROM",
        "col_arte": "Estado da Mídia",
        "lbl_inspetor": " 👁️ Inspetor Visual ",
        "vid_none": "🎦 Vídeo: --",
        "btn_add_jogo": "✨ Adicionar Jogo",
        "btn_add_arte": "🖼️ Capa Manual",
        "btn_del_jogo": "🗑️ Remover Jogo",
        "btn_atualizar": "🔄 Atualizar",
        
        "status_temas": "A aguardar conexão...",
        "col_tema": "Tema Instalado",
        "col_status_tema": "Integridade Estrutural",
        "btn_add_tema": "➕ Instalar Novo Tema (.zip)",
        "btn_del_tema": "🗑️ Desinstalar Selecionado",
        
        "drv_tit": "Patch de Drivers do Ecrã (R36S)",
        "drv_sub": "Selecione a sua pasta de drivers e escolha o ficheiro correto para o seu ecrã.",
        "lbl_pasta_drv": "Pasta de Drivers:",
        "btn_procurar_pasta": "📁 Selecionar Pasta",
        "col_patch": "Patches / Ficheiros DTB Disponíveis Encontrados",
        "btn_aplicar_patch": "🚀 APLICAR PATCH NO CARTÃO BOOT",
        "status_drivers": "Selecione a pasta onde tem os drivers (.dtb)",
        
        "msg_sucesso": "Sucesso",
        "msg_erro": "Erro",
        "msg_aviso": "Aviso",
        "msg_logo_ok": "O teu novo Logo foi gravado com sucesso!",
        "msg_sel_img": "Selecione a imagem e verifique o cartão SD!",
        "status_scraper_conn": "🌐 A ligar ao repositório oficial Libretro...",
        "status_nenhum_sis": "ℹ️ Nenhum sistema selecionado.",
        "status_sd_erro": "⚠️ Cartão EASYROMS/BOOT não detetado.",
        "capa_ativa": "✦ Ativa",
        "capa_nenhuma": "✧ Nenhum",
        "vid_ok": "🎦 Vídeo: Encontrado no SD",
        "vid_fail": "🎦 Vídeo: Não Encontrado",
        "sem_capa_img": "Sem Capa Disponível",
        "msg_drv_ok": "Patch de ecrã aplicado com sucesso! Insira o cartão no R36S e teste.",
        "msg_sel_drv": "Por favor, selecione um ficheiro de patch da lista!",
        "msg_tudo_atualizado": "Excelente! Todos os teus jogos já têm capas atualizadas.",
        "status_concluido": "✨ Scraper concluído com sucesso!",
        "btn_update": "🔄 Procurar Atualizações"
    },
    "EN": {
        "title": "Ultimate G80CA-MB V1.3 Assistant + Fixed Scraper",
        "tab_logo": "  🖼️ Boot Logo  ",
        "tab_jogos": "  🎮 Games & Covers  ",
        "tab_temas": "  🎨 ES Themes  ",
        "tab_drivers": "  🖥️ Screen Drivers  ",
        
        "logo_tit": "Boot Customizer (G80CA-MB V1.3)",
        "logo_sub": "Change the static splash screen that appears when turning on the handheld.",
        "btn_proc": "🔍 Browse File",
        "chk_rot": "🛠️ Apply Hardware Rotation (G80CA-MB V1.3 Board / V12 Screen)",
        "btn_gravar": "💾  WRITE NEW LOGO TO SD CARD",
        
        "lbl_sis": "🔍 System:",
        "lbl_dir": "Directory:",
        "btn_scrap": "🌐 Automated Scraper",
        "status_analise": "Analyzing local storage bus...",
        "col_nome": "File / ROM",
        "col_arte": "Media Status",
        "lbl_inspetor": " 👁️ Visual Inspector ",
        "vid_none": "🎦 Video: --",
        "btn_add_jogo": "✨ Add Game",
        "btn_add_arte": "🖼️ Manual Cover",
        "btn_del_jogo": "🗑️ Remove Game",
        "btn_atualizar": "🔄 Refresh",
        
        "status_temas": "Waiting for connection...",
        "col_tema": "Installed Theme",
        "col_status_tema": "Structural Integrity",
        "btn_add_tema": "➕ Install New Theme (.zip)",
        "btn_del_tema": "🗑️ Uninstall Selected",
        
        "drv_tit": "Screen Driver Patching (R36S)",
        "drv_sub": "Select your drivers folder and choose the correct file for your screen type.",
        "lbl_pasta_drv": "Drivers Folder:",
        "btn_procurar_pasta": "📁 Select Folder",
        "col_patch": "Available Patches / DTB Files Found",
        "btn_aplicar_patch": "🚀 APPLY PATCH TO BOOT CARD",
        "status_drivers": "Select the folder containing your (.dtb) drivers",
        
        "msg_sucesso": "Success",
        "msg_erro": "Error",
        "msg_aviso": "Warning",
        "msg_logo_ok": "Your new Logo was written successfully!",
        "msg_sel_img": "Select the image and check the SD card!",
        "status_scraper_conn": "🌐 Connecting to official Libretro repository...",
        "status_nenhum_sis": "ℹ️ No system selected.",
        "status_sd_erro": "⚠️ EASYROMS/BOOT card not detected.",
        "capa_ativa": "✦ Active",
        "capa_nenhuma": "✧ None",
        "vid_ok": "🎦 Video: Found on SD",
        "vid_fail": "🎦 Video: Not Found",
        "sem_capa_img": "No Cover Available",
        "msg_drv_ok": "Screen patch applied successfully! Insert the card into your R36S and boot.",
        "msg_sel_drv": "Please select a patch file from the list!",
        "msg_tudo_atualizado": "Excellent! All your games already have updated covers.",
        "status_concluido": "✨ Scraper completed successfully!",
        "btn_update": "🔄 Check for Updates"
    }
}

def t(chave):
    return TEXTOS[IDIOMA_ATUAL].get(chave, chave)

# --- MAPAS E VARIÁVEIS ---
MAPA_CONSOLAS_LIBRETRO = {
    "gba": "Nintendo - Game Boy Advance", "gbc": "Nintendo - Game Boy Color", "gb": "Nintendo - Game Boy",
    "snes": "Super Nintendo Entertainment System", "nes": "Nintendo - Entertainment System",
    "megadrive": "Sega - Mega Drive - Genesis", "mastersystem": "Sega - Master System - Mark III",
    "gamegear": "Sega - Game Gear", "n64": "Nintendo - Nintendo 64", "psx": "Sony - PlayStation",
    "pce": "NEC - PC Engine - TurboGrafx-16"
}

EXTENSOES_JOGOS_VALIDAS = ['.zip', '.gba', '.gbc', '.gb', '.snes', '.smc', '.sfc', '.nes', '.md', '.bin', '.gen', '.sms', '.gg', '.n64', '.z64', '.v64', '.chd', '.cue', '.pbp', '.iso', '.img', '.pce']
consoles_totais = []

# --- FUNÇÕES CORE ---
def mudar_idioma(event=None):
    global IDIOMA_ATUAL
    IDIOMA_ATUAL = combo_lang.get()
    
    root.title(t("title"))
    abas.tab(aba_logo, text=t("tab_logo"))
    abas.tab(aba_jogos, text=t("tab_jogos"))
    abas.tab(aba_temas, text=t("tab_temas"))
    abas.tab(aba_drivers, text=t("tab_drivers"))
    
    lbl_tit_logo.config(text=t("logo_tit"))
    lbl_sub_logo.config(text=t("logo_sub"))
    btn_proc_logo.config(text=t("btn_proc"))
    chk_v12.config(text=t("chk_rot"))
    btn_grav_logo.config(text=t("btn_gravar"))
    
    lbl_busca_console.config(text=t("lbl_sis"))
    lbl_plataforma.config(text=t("lbl_dir"))
    btn_scraper_online.config(text=t("btn_scrap"))
    lbl_status_jogos.config(text=t("status_analise"))
    
    lista_jogos.heading("nome", text=t("col_nome"))
    lista_jogos.heading("arte", text=t("col_arte"))
    frame_preview.config(text=t("lbl_inspetor"))
    lbl_info_video.config(text=t("vid_none"))
    
    btn_add_jogo.config(text=t("btn_add_jogo"))
    btn_add_arte.config(text=t("btn_add_arte"))
    btn_del_jogo.config(text=t("btn_del_jogo"))
    btn_atualizar.config(text=t("btn_atualizar"))
    
    lbl_status_temas.config(text=t("status_temas"))
    lista_temas.heading("nome_tema", text=t("col_tema"))
    lista_temas.heading("status_tema", text=t("col_status_tema"))
    btn_add_tema.config(text=t("btn_add_tema"))
    btn_del_tema.config(text=t("btn_del_tema"))
    btn_refresh_temas.config(text=t("btn_atualizar"))
    
    lbl_tit_drv.config(text=t("drv_tit"))
    lbl_sub_drv.config(text=t("drv_sub"))
    lbl_pasta_drv.config(text=t("lbl_pasta_drv"))
    btn_proc_pasta_drv.config(text=t("btn_procurar_pasta"))
    lista_drivers.heading("nome_patch", text=t("col_patch"))
    btn_aplicar_patch.config(text=t("btn_aplicar_patch"))
    lbl_status_drivers.config(text=t("status_drivers"))
    btn_update_app.config(text=t("btn_update"))
    
    atualizar_tudo_ao_entrar()

def encontrar_particoes():
    boot = roms = None
    for disco in psutil.disk_partitions():
        if 'cdrom' in disco.opts or disco.mountpoint.startswith('C:'): continue
        caminho = disco.mountpoint
        if any(os.path.exists(os.path.join(caminho, f)) for f in ['boot.ini', 'uEnv.txt', 'logo.bmp']): boot = caminho
        if any(os.path.exists(os.path.join(caminho, f)) for f in ['bios', 'gba', 'cheats']): roms = caminho
    if not roms or not boot:
        for disco in psutil.disk_partitions():
            if 'removable' in disco.opts and not disco.mountpoint.startswith('C:'):
                if not boot: boot = disco.mountpoint
                elif not roms: roms = disco.mountpoint
    return boot, roms

def listar_consoles(drive_roms):
    if not drive_roms or not os.path.exists(drive_roms): return []
    pastas_sistema = ['bios', 'cheats', 'themes', 'gamelists', 'lost+found', 'images', 'launchimages', 'downloaded_images', 'downloaded_videos']
    return sorted([i.lower() for i in os.listdir(drive_roms) if os.path.isdir(os.path.join(drive_roms, i)) and i.lower() not in pastas_sistema and not i.startswith('.')])

def filtrar_consoles(event=None):
    texto_busca = entrada_busca_console.get().lower()
    consoles_filtrados = [c for c in consoles_totais if texto_busca in c]
    combo_consoles.config(values=consoles_filtrados)
    combo_consoles.set(consoles_filtrados[0] if consoles_filtrados else "")
    atualizar_lista_jogos()

def selecionar_imagem_logo():
    caminho = filedialog.askopenfilename(title=t("btn_proc"), filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
    if caminho:
        entrada_logo.delete(0, tk.END)
        entrada_logo.insert(0, caminho)

def gravar_logo():
    caminho_img, (drive_boot, _) = entrada_logo.get(), encontrar_particoes()
    if not caminho_img or not drive_boot:
        messagebox.showerror(t("msg_erro"), t("msg_sel_img"))
        return
    try:
        img = Image.open(caminho_img).resize((640, 480), Image.Resampling.LANCZOS).convert("RGB")
        if var_v12.get(): img = img.transpose(Image.Transpose.ROTATE_270)
        img.save(os.path.join(drive_boot, "logo.bmp"), format="BMP")
        os.makedirs(os.path.join(drive_boot, "BMPs"), exist_ok=True)
        img.save(os.path.join(drive_boot, "BMPs", "logo.bmp"), format="BMP")
        messagebox.showinfo(t("msg_sucesso") + " 🎉", t("msg_logo_ok"))
    except Exception as e:
        messagebox.showerror(t("msg_erro"), str(e))

def verificar_se_tem_arte(pasta, nome):
    for sub in ['images', 'downloaded_images', 'downloaded_videos']:
        p = os.path.join(pasta, sub)
        if os.path.exists(p) and any(os.path.splitext(f)[0] in [nome, f"{nome}-image", f"{nome}-video"] for f in os.listdir(p)):
            return t("capa_ativa")
    return t("capa_nenhuma")

def carregar_imagem_padrao():
    img = Image.new('RGB', (220, 240), color='#1e1e2e')
    ImageDraw.Draw(img).text((55, 115), t("sem_capa_img"), fill="#6c7086")
    foto = ImageTk.PhotoImage(img)
    lbl_foto_preview.config(image=foto)
    lbl_foto_preview.image = foto

def ao_selecionar_jogo(event=None):
    selecionado = lista_jogos.selection()
    if not selecionado: return carregar_imagem_padrao()
    nome_sem_ext = os.path.splitext(lista_jogos.item(selecionado[0])['values'][0])[0]
    _, drive_roms = encontrar_particoes()
    pasta = os.path.join(drive_roms, combo_consoles.get())
    
    caminho_capa = next((os.path.join(pasta, s, f"{nome_sem_ext}{e}") for s in ['downloaded_images', 'images'] for e in ['.png', '.jpg', '.jpeg'] if os.path.exists(os.path.join(pasta, s, f"{nome_sem_ext}{e}"))), None)
    try:
        img = Image.open(caminho_capa)
        img.thumbnail((220, 240), Image.Resampling.LANCZOS)
        foto = ImageTk.PhotoImage(img)
        lbl_foto_preview.config(image=foto)
        lbl_foto_preview.image = foto
    except: carregar_imagem_padrao()
    
    tem_vid = any(os.path.exists(os.path.join(pasta, s, f"{nome_sem_ext}{e}")) for s in ['downloaded_videos', 'videos'] for e in ['.mp4', '.mkv'])
    lbl_info_video.config(text=t("vid_ok") if tem_vid else t("vid_fail"), fg="#a6e3a1" if tem_vid else "#f38ba8")

def atualizar_lista_jogos():
    global consoles_totais
    _, drive_roms = encontrar_particoes()
    lista_jogos.delete(*lista_jogos.get_children())
    if not drive_roms:
        lbl_status_jogos.config(text=t("status_sd_erro"), fg="#f38ba8")
        return combo_consoles.config(values=[])
    
    if not consoles_totais:
        consoles_totais = listar_consoles(drive_roms)
        combo_consoles.config(values=consoles_totais)
    
    c_atual = combo_consoles.get() or (consoles_totais[0] if consoles_totais and not entrada_busca_console.get() else "")
    if c_atual: combo_consoles.set(c_atual)
    else: return lbl_status_jogos.config(text=t("status_nenhum_sis"), fg="#f9e2af")
        
    pasta = os.path.join(drive_roms, c_atual)
    lbl_status_jogos.config(text=f"🟢 {drive_roms} | {c_atual.upper()}", fg="#a6e3a1")
    if os.path.exists(pasta):
        for arq in os.listdir(pasta):
            if os.path.isfile(os.path.join(pasta, arq)) and not arq.startswith('.') and os.path.splitext(arq)[1].lower() in EXTENSOES_JOGOS_VALIDAS:
                lista_jogos.insert("", tk.END, values=(arq, verificar_se_tem_arte(pasta, os.path.splitext(arq)[0])))
    carregar_imagem_padrao()
    lbl_info_video.config(text=t("vid_none"), fg="#6c7086")

def limpar_nome_jogo(nome): return re.sub(r'(\[.*?\]|\(.*?\))', '', nome).strip()

def buscar_capas_online():
    _, drive_roms = encontrar_particoes()
    c_atual = combo_consoles.get()
    if not drive_roms or not c_atual: return messagebox.showerror(t("msg_erro"), "Select system!")
    if c_atual not in MAPA_CONSOLAS_LIBRETRO: return messagebox.showwarning(t("msg_aviso"), "Unsupported.")
    
    sem_capa = [i for i in lista_jogos.get_children() if lista_jogos.item(i)['values'][1] == t("capa_nenhuma")]
    
    if not sem_capa:
        messagebox.showinfo(t("msg_sucesso"), t("msg_tudo_atualizado"))
        lbl_status_jogos.config(text=t("status_concluido"), fg="#a6e3a1")
        return

    pasta_artes = os.path.join(drive_roms, c_atual, "downloaded_images")
    os.makedirs(pasta_artes, exist_ok=True)
    url_base = f"https://thumbnails.libretro.com/{urllib.parse.quote(MAPA_CONSOLAS_LIBRETRO[c_atual])}/Named_Boxarts/"
    lbl_status_jogos.config(text=t("status_scraper_conn"), fg="#89b4fa"); root.update()
    
    try:
        r = requests.get(url_base, headers={"User-Agent": "Mozilla/5.0"}, timeout=25, verify=False)
        capas = [urllib.parse.unquote(c) for c in re.findall(r'href="([^"]+\.png)"', r.text)]
    except Exception as e: return messagebox.showerror(t("msg_erro"), str(e))
    
    barra_progresso["maximum"] = len(sem_capa)
    
    for idx, item in enumerate(sem_capa):
        nome_sem_ext = os.path.splitext(lista_jogos.item(item)['values'][0])[0]
        melhor = process.extractOne(limpar_nome_jogo(nome_sem_ext) + ".png", capas)
        if melhor and melhor[1] >= 75:
            try:
                with open(os.path.join(pasta_artes, "temp.png"), 'wb') as f:
                    f.write(requests.get(url_base + urllib.parse.quote(melhor[0]), verify=False, timeout=15).content)
                img = Image.open(os.path.join(pasta_artes, "temp.png"))
                img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                img.save(os.path.join(pasta_artes, f"{nome_sem_ext}.png"), "PNG")
                os.remove(os.path.join(pasta_artes, "temp.png"))
            except: pass
        barra_progresso["value"] = idx + 1; root.update()
    
    barra_progresso["value"] = 0
    lbl_status_jogos.config(text=t("status_concluido"), fg="#a6e3a1")
    atualizar_lista_jogos()

# --- FUNÇÃO DE AUTO-UPDATE BASEADA NO GITHUB ---
def verificar_e_atualizar_app(silencioso=True):
    try:
        resposta_v = requests.get(URL_VERSAO_REMOTA, timeout=10, verify=False)
        if resposta_v.status_code != 200:
            if not silencioso:
                messagebox.showerror(t("msg_erro"), "Não foi possível conectar ao repositório para validar versões.")
            return

        versao_remota = resposta_v.text.strip()

        # Compara as versões (ex: Remota "1.4" > Atual "1.3")
        if float(versao_remota) > float(VERSAO_ATUAL):
            if messagebox.askyesno("Atualização Disponível", f"Uma nova versão ({versao_remota}) foi detetada no GitHub!\nDesejas atualizar a aplicação automaticamente agora?"):
                resposta_codigo = requests.get(URL_CODIGO_REMOTOS, timeout=20, verify=False)
                if resposta_codigo.status_code == 200:
                    caminho_atual = os.path.realpath(sys.argv[0])
                    
                    # Backup local preventivo
                    shutil.copy(caminho_atual, caminho_atual + ".bak")
                    
                    # Sobrescreve com o novo código do GitHub
                    with open(caminho_atual, "wb") as f:
                        f.write(resposta_codigo.content)
                        
                    messagebox.showinfo(t("msg_sucesso"), "Aplicação atualizada com sucesso! A reiniciar...")
                    os.execv(sys.executable, ['python'] + sys.argv)
                else:
                    messagebox.showerror(t("msg_erro"), "Não foi possível descarregar o ficheiro de código remetido.")
        else:
            if not silencioso:
                messagebox.showinfo("Atualizado", f"A tua aplicação está na versão mais recente ({VERSAO_ATUAL}).")
    except Exception as e:
        if not silencioso:
            messagebox.showerror(t("msg_erro"), f"Erro na árvore de verificação: {str(e)}")

def adicionar_jogo():
    caminhos = filedialog.askopenfilenames(title=t("btn_add_jogo"))
    if caminhos:
        for c in caminhos: shutil.copy(c, os.path.join(encontrar_particoes()[1], combo_consoles.get()))
        atualizar_lista_jogos()

def remover_jogo():
    selecionado = lista_jogos.selection()
    if selecionado and messagebox.askyesno("Delete", "Are you sure?"):
        nome = lista_jogos.item(selecionado[0])['values'][0]
        pasta = os.path.join(encontrar_particoes()[1], combo_consoles.get())
        os.remove(os.path.join(pasta, nome))
        atualizar_lista_jogos()

def adicionar_arte_manual():
    selecionado = lista_jogos.selection()
    if not selecionado: return
    img_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg")])
    if img_path:
        pasta = os.path.join(encontrar_particoes()[1], combo_consoles.get(), "downloaded_images")
        os.makedirs(pasta, exist_ok=True)
        img = Image.open(img_path)
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        img.save(os.path.join(pasta, f"{os.path.splitext(lista_jogos.item(selecionado[0])['values'][0])[0]}.png"), "PNG")
        atualizar_lista_jogos()

def atualizar_lista_temas():
    _, drive_roms = encontrar_particoes()
    lista_temas.delete(*lista_temas.get_children())
    if not drive_roms: return lbl_status_temas.config(text=t("status_sd_erro"), fg="#f38ba8")
    pasta = os.path.join(drive_roms, "themes")
    os.makedirs(pasta, exist_ok=True)
    lbl_status_temas.config(text=f"📂 {pasta}", fg="#a6e3a1")
    for item in os.listdir(pasta):
        if os.path.isdir(os.path.join(pasta, item)) and not item.startswith('.'):
            lista_temas.insert("", tk.END, values=(item, f"📦 {len(os.listdir(os.path.join(pasta, item)))} items"))

def adicionar_tema_zip():
    caminho_zip = filedialog.askopenfilename(filetypes=[("Zip", "*.zip")])
    if caminho_zip:
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(encontrar_particoes()[1], "themes"))
        atualizar_lista_temas()

def remover_tema():
    selecionado = lista_temas.selection()
    if selecionado and messagebox.askyesno("Delete", "Are you sure?"):
        shutil.rmtree(os.path.join(encontrar_particoes()[1], "themes", lista_temas.item(selecionado[0])['values'][0]))
        atualizar_lista_temas()

def selecionar_pasta_drivers():
    pasta = filedialog.askdirectory(title=t("btn_procurar_pasta"))
    if pasta:
        entrada_pasta_drv.delete(0, tk.END)
        entrada_pasta_drv.insert(0, pasta)
        atualizar_lista_drivers()

def atualizar_lista_drivers():
    pasta_raiz = entrada_pasta_drv.get()
    lista_drivers.delete(*lista_drivers.get_children())
    if not pasta_raiz or not os.path.exists(pasta_raiz): return
    
    encontrados = 0
    padrao_filtro = re.compile(r'(rg351mp|dtb|panel|v1|v2|v3|v4|v5|clone|screen|display|patch)', re.IGNORECASE)

    for raiz, subpastas, ficheiros in os.walk(pasta_raiz):
        for ficheiro in ficheiros:
            caminho_completo = os.path.join(raiz, ficheiro)
            extensao = os.path.splitext(ficheiro)[1].lower()
            
            if extensao in ['.dtb', '.sh'] or '.dtb.' in ficheiro.lower() or padrao_filtro.search(ficheiro):
                caminho_relativo = os.path.relpath(caminho_completo, pasta_raiz)
                lista_drivers.insert("", tk.END, values=(caminho_relativo,))
                encontrados += 1
                
    lbl_status_drivers.config(text=f"🔍 {encontrados} patches identificados na árvore de diretórios.", fg="#89b4fa")

def aplicar_patch_driver():
    selecionado = lista_drivers.selection()
    if not selecionado:
        messagebox.showerror(t("msg_erro"), t("msg_sel_drv"))
        return
    
    caminho_relativo = lista_drivers.item(selecionado[0])['values'][0]
    pasta_origem = entrada_pasta_drv.get()
    caminho_origem = os.path.join(pasta_origem, caminho_relativo)
    
    drive_boot, _ = encontrar_particoes()
    if not drive_boot:
        messagebox.showerror(t("msg_erro"), t("status_sd_erro"))
        return
        
    try:
        destino_final = os.path.join(drive_boot, "rg351mp-kernel.dtb")
        if os.path.exists(destino_final):
            shutil.copy(destino_final, destino_final + ".bak")
            
        shutil.copy(caminho_origem, destino_final)
        messagebox.showinfo(t("msg_sucesso") + " 🖥️", t("msg_drv_ok"))
        lbl_status_drivers.config(text=f"🟢 Patch Ativo: {os.path.basename(caminho_relativo)}", fg="#a6e3a1")
    except Exception as e:
        messagebox.showerror(t("msg_erro"), str(e))

def atualizar_tudo_ao_entrar(event=None):
    indice = abas.index(abas.select())
    if indice == 1: atualizar_lista_jogos()
    elif indice == 2: atualizar_lista_temas()
    elif indice == 3: atualizar_lista_drivers()

# --- INTERFACE GRÁFICA ---
root = tk.Tk()
root.geometry("1060x680")
root.config(bg="#11111b")

# TOP FRAME COM IDIOMA E NOVO BOTÃO DE UPDATE
frame_topo = tk.Frame(root, bg="#11111b")
frame_topo.pack(fill="x", padx=15, pady=(10, 0))

combo_lang = ttk.Combobox(frame_topo, values=["PT", "EN"], state="readonly", width=5, font=("Segoe UI", 9))
combo_lang.set(IDIOMA_ATUAL)
combo_lang.pack(side="right")
combo_lang.bind("<<ComboboxSelected>>", mudar_idioma)

tk.Label(frame_topo, text="Language:", bg="#11111b", fg="#a6adc8", font=("Segoe UI", 9)).pack(side="right", padx=(15, 5))

# Botão Injetado para Tratar Atualizações
btn_update_app = tk.Button(frame_topo, command=lambda: verificar_e_atualizar_app(silencioso=False), bg="#313244", fg="#89b4fa", activebackground="#45475a", activeforeground="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, padx=12, pady=2)
btn_update_app.pack(side="right", padx=10)

estilo = ttk.Style()
estilo.theme_use('default')
estilo.configure('TNotebook', background='#11111b', borderwidth=0)
estilo.configure('TNotebook.Tab', background='#1e1e2e', foreground='#cdd6f4', padding=[16, 8], font=("Segoe UI", 10, "bold"))
estilo.map('TNotebook.Tab', background=[('selected', '#181825')], foreground=[('selected', '#89b4fa')])
estilo.configure('TCombobox', fieldbackground='#313244', background='#45475a', foreground='white', borderwidth=0)
estilo.configure("Horizontal.TProgressbar", troughcolor='#1e1e2e', background='#89b4fa', bordercolor='#11111b')
estilo.configure("Treeview", background="#1e1e2e", foreground="#cdd6f4", fieldbackground="#1e1e2e", rowheight=26, font=("Segoe UI", 10), borderwidth=0)
estilo.configure("Treeview.Heading", background="#313244", foreground="white", font=("Segoe UI", 10, "bold"), borderwidth=0)
estilo.map("Treeview", background=[("selected", "#89b4fa")], foreground=[("selected", "#11111b")])

abas = ttk.Notebook(root)
abas.pack(fill="both", expand=True, padx=15, pady=(5, 15))
abas.bind("<<NotebookTabChanged>>", atualizar_tudo_ao_entrar)

# ABA 1 - BOOT LOGO
aba_logo = tk.Frame(abas, bg="#1e1e2e"); abas.add(aba_logo, text="")
lbl_tit_logo = tk.Label(aba_logo, font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#cdd6f4"); lbl_tit_logo.pack(pady=(40, 10))
lbl_sub_logo = tk.Label(aba_logo, font=("Segoe UI", 10), bg="#1e1e2e", fg="#a6adc8"); lbl_sub_logo.pack(pady=(0, 30))

frame_lbl = tk.Frame(aba_logo, bg="#1e1e2e"); frame_lbl.pack(pady=10, fill="x", padx=100)
entrada_logo = tk.Entry(frame_lbl, font=("Segoe UI", 11), width=45, bg="#313244", fg="white", relief="flat", bd=0)
entrada_logo.pack(side="left", padx=5, ipady=6, fill="x", expand=True)
btn_proc_logo = tk.Button(frame_lbl, command=selecionar_imagem_logo, bg="#45475a", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, bd=0)
btn_proc_logo.pack(side="left", padx=5, ipady=4)

var_v12 = tk.BooleanVar(value=True)
chk_v12 = tk.Checkbutton(aba_logo, variable=var_v12, bg="#1e1e2e", fg="#a6e3a1", selectcolor="#313244", activebackground="#1e1e2e", activeforeground="#a6e3a1", font=("Segoe UI", 10, "bold"), bd=0)
chk_v12.pack(pady=15)
btn_grav_logo = tk.Button(aba_logo, font=("Segoe UI", 11, "bold"), bg="#89b4fa", fg="#11111b", relief="flat", command=gravar_logo, height=2, bd=0)
btn_grav_logo.pack(pady=30, fill="x", padx=105)

# ABA 2 - JOGOS E CAPAS
aba_jogos = tk.Frame(abas, bg="#1e1e2e"); abas.add(aba_jogos, text="")
frame_seletor = tk.Frame(aba_jogos, bg="#252538"); frame_seletor.pack(fill="x", padx=15, pady=15, ipady=6)
lbl_busca_console = tk.Label(frame_seletor, font=("Segoe UI", 10, "bold"), bg="#252538", fg="#cdd6f4"); lbl_busca_console.pack(side="left", padx=(15, 5))
entrada_busca_console = tk.Entry(frame_seletor, font=("Segoe UI", 10), width=12, bg="#313244", fg="white", relief="flat", bd=0); entrada_busca_console.pack(side="left", padx=(0, 15), ipady=4)
entrada_busca_console.bind("<KeyRelease>", filtrar_consoles)
lbl_plataforma = tk.Label(frame_seletor, font=("Segoe UI", 10, "bold"), bg="#252538", fg="#cdd6f4"); lbl_plataforma.pack(side="left", padx=5)
combo_consoles = ttk.Combobox(frame_seletor, font=("Segoe UI", 10), state="readonly", width=22); combo_consoles.pack(side="left", padx=5)
combo_consoles.bind("<<ComboboxSelected>>", lambda e: atualizar_lista_jogos())
btn_scraper_online = tk.Button(frame_seletor, bg="#89b4fa", fg="#11111b", relief="flat", font=("Segoe UI", 10, "bold"), command=buscar_capas_online, bd=0, padx=15); btn_scraper_online.pack(side="right", padx=15)

lbl_status_jogos = tk.Label(aba_jogos, font=("Segoe UI", 10, "italic"), bg="#1e1e2e", fg="#a6adc8"); lbl_status_jogos.pack(pady=(0, 5))
frame_progresso = tk.Frame(aba_jogos, bg="#1e1e2e"); frame_progresso.pack(fill="x", padx=15, pady=(0, 10))
barra_progresso = ttk.Progressbar(frame_progresso, orient="horizontal", style="Horizontal.TProgressbar", mode="determinate"); barra_progresso.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=2)

frame_conteudo_jogos = tk.Frame(aba_jogos, bg="#1e1e2e"); frame_conteudo_jogos.pack(pady=5, fill="both", expand=True, padx=15)
frame_tabela = tk.Frame(frame_conteudo_jogos, bg="#1e1e2e"); frame_tabela.pack(side="left", fill="both", expand=True)
lista_jogos = ttk.Treeview(frame_tabela, columns=("nome", "arte"), show="headings")
lista_jogos.column("nome", width=420, anchor="w"); lista_jogos.column("arte", width=140, anchor="center")
lista_jogos.pack(side="left", fill="both", expand=True)
scroll = ttk.Scrollbar(frame_tabela, orient="vertical", command=lista_jogos.yview); lista_jogos.configure(yscrollcommand=scroll.set); scroll.pack(side="right", fill="y")
lista_jogos.bind("<<TreeviewSelect>>", ao_selecionar_jogo)

frame_preview = tk.LabelFrame(frame_conteudo_jogos, bg="#1e1e2e", fg="#89b4fa", font=("Segoe UI", 10, "bold"), labelanchor="n", padx=15, pady=15, bd=1, relief="solid")
frame_preview.pack(side="right", fill="y", padx=(20, 0))
lbl_foto_preview = tk.Label(frame_preview, bg="#11111b", bd=0); lbl_foto_preview.pack(pady=5, anchor="center")
lbl_info_video = tk.Label(frame_preview, font=("Segoe UI", 10, "bold"), bg="#1e1e2e", fg="#6c7086"); lbl_info_video.pack(pady=(15, 0), anchor="center")

frame_botoes = tk.Frame(aba_jogos, bg="#1e1e2e"); frame_botoes.pack(pady=15, fill="x", padx=15)
btn_add_jogo = tk.Button(frame_botoes, bg="#a6e3a1", fg="#11111b", relief="flat", font=("Segoe UI", 10, "bold"), command=adicionar_jogo, width=16, bd=0); btn_add_jogo.pack(side="left", padx=5)
btn_add_arte = tk.Button(frame_botoes, bg="#74c7ec", fg="#11111b", relief="flat", font=("Segoe UI", 10, "bold"), command=adicionar_arte_manual, width=16, bd=0); btn_add_arte.pack(side="left", padx=5)
btn_del_jogo = tk.Button(frame_botoes, bg="#f38ba8", fg="#11111b", relief="flat", font=("Segoe UI", 10, "bold"), command=remover_jogo, width=16, bd=0); btn_del_jogo.pack(side="left", padx=5)
btn_atualizar = tk.Button(frame_botoes, bg="#45475a", fg="white", relief="flat", font=("Segoe UI", 10, "bold"), command=atualizar_lista_jogos, width=12, bd=0); btn_atualizar.pack(side="right", padx=5)

# ABA 3 - TEMAS
aba_temas = tk.Frame(abas, bg="#1e1e2e"); abas.add(aba_temas, text="")
lbl_status_temas = tk.Label(aba_temas, font=("Segoe UI", 10, "italic"), bg="#1e1e2e", fg="#a6adc8"); lbl_status_temas.pack(pady=15)
frame_tabela_temas = tk.Frame(aba_temas, bg="#1e1e2e"); frame_tabela_temas.pack(pady=5, fill="both", expand=True, padx=15)
lista_temas = ttk.Treeview(frame_tabela_temas, columns=("nome_tema", "status_tema"), show="headings")
lista_temas.column("nome_tema", width=420, anchor="w"); lista_temas.column("status_tema", width=160, anchor="center")
lista_temas.pack(side="left", fill="both", expand=True)
scroll_temas = ttk.Scrollbar(frame_tabela_temas, orient="vertical", command=lista_temas.yview); lista_temas.configure(yscrollcommand=scroll_temas.set); scroll_temas.pack(side="right", fill="y")

frame_botoes_temas = tk.Frame(aba_temas, bg="#1e1e2e"); frame_botoes_temas.pack(pady=20, fill="x", padx=15)
btn_add_tema = tk.Button(frame_botoes_temas, bg="#a6e3a1", fg="#11111b", relief="flat", font=("Segoe UI", 10, "bold"), command=adicionar_tema_zip, width=25, bd=0); btn_add_tema.pack(side="left", padx=5)
btn_del_tema = tk.Button(frame_botoes_temas, bg="#f38ba8", fg="#11111b", relief="flat", font=("Segoe UI", 10, "bold"), command=remover_tema, width=25, bd=0); btn_del_tema.pack(side="left", padx=5)
btn_refresh_temas = tk.Button(frame_botoes_temas, bg="#45475a", fg="white", relief="flat", font=("Segoe UI", 10, "bold"), command=atualizar_lista_temas, width=12, bd=0); btn_refresh_temas.pack(side="right", padx=5)

# ABA 4 - DRIVERS DO ECRÃ
aba_drivers = tk.Frame(abas, bg="#1e1e2e"); abas.add(aba_drivers, text="")
lbl_tit_drv = tk.Label(aba_drivers, font=("Segoe UI", 16, "bold"), bg="#1e1e2e", fg="#cdd6f4"); lbl_tit_drv.pack(pady=(20, 5))
lbl_sub_drv = tk.Label(aba_drivers, font=("Segoe UI", 10), bg="#1e1e2e", fg="#a6adc8"); lbl_sub_drv.pack(pady=(0, 15))

frame_pasta_drv = tk.Frame(aba_drivers, bg="#252538"); frame_pasta_drv.pack(fill="x", padx=15, pady=10, ipady=6)
lbl_pasta_drv = tk.Label(frame_pasta_drv, font=("Segoe UI", 10, "bold"), bg="#252538", fg="#cdd6f4"); lbl_pasta_drv.pack(side="left", padx=(15, 5))
entrada_pasta_drv = tk.Entry(frame_pasta_drv, font=("Segoe UI", 10), width=45, bg="#313244", fg="white", relief="flat", bd=0)
entrada_pasta_drv.pack(side="left", padx=5, ipady=4, fill="x", expand=True)
btn_proc_pasta_drv = tk.Button(frame_pasta_drv, command=selecionar_pasta_drivers, bg="#45475a", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, bd=0)
btn_proc_pasta_drv.pack(side="right", padx=15)

lbl_status_drivers = tk.Label(aba_drivers, font=("Segoe UI", 10, "italic"), bg="#1e1e2e", fg="#a6adc8"); lbl_status_drivers.pack(pady=(5, 5))

frame_tabela_drivers = tk.Frame(aba_drivers, bg="#1e1e2e"); frame_tabela_drivers.pack(pady=5, fill="both", expand=True, padx=15)
lista_drivers = ttk.Treeview(frame_tabela_drivers, columns=("nome_patch",), show="headings")
lista_drivers.column("nome_patch", width=800, anchor="w")
lista_drivers.pack(side="left", fill="both", expand=True)
scroll_drivers = ttk.Scrollbar(frame_tabela_drivers, orient="vertical", command=lista_drivers.yview); lista_drivers.configure(yscrollcommand=scroll_drivers.set); scroll_drivers.pack(side="right", fill="y")

frame_botoes_drivers = tk.Frame(aba_drivers, bg="#1e1e2e"); frame_botoes_drivers.pack(pady=15, fill="x", padx=15)
btn_aplicar_patch = tk.Button(frame_botoes_drivers, bg="#89b4fa", fg="#11111b", relief="flat", font=("Segoe UI", 11, "bold"), command=aplicar_patch_driver, height=2, bd=0)
btn_aplicar_patch.pack(fill="x", padx=5)

# Inicializar interface
mudar_idioma()
root.after(1000, lambda: verificar_e_atualizar_app(silencioso=True)) # Tenta update silencioso ao iniciar
root.mainloop()