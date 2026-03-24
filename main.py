from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SYSTEM // ADBYPASS_V5</title>
    <style>
        :root {
            --bg: #05070a;
            --surface: #0d1117;
            --accent: #00f2ff;
            --green: #00ff41;
            --border: #30363d;
            --text: #c9d1d9;
        }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body {
            background: var(--bg); color: var(--text);
            font-family: 'Consolas', 'Monaco', monospace;
            margin: 0; padding: 15px;
            display: flex; flex-direction: column; align-items: center;
            min-height: 100vh; overflow-x: hidden;
        }
        body::before {
            content: " "; display: block; position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
            z-index: -1; background-size: 100% 4px, 3px 100%; pointer-events: none;
        }
        
        /* Margem superior para descer a caixa para o alcance do polegar */
        .main-frame {
            width: 100%; max-width: 500px;
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 8px; padding: 20px; box-shadow: 0 0 20px rgba(0,0,0,0.5);
            margin-top: 10vh; z-index: 1;
        }
        
        h1 { font-size: 1.2rem; color: var(--accent); text-align: center; margin: 0 0 20px 0; letter-spacing: 2px; text-transform: uppercase; }
        
        .input-group { display: flex; gap: 8px; margin-bottom: 15px; }
        .input-box {
            flex-grow: 1; background: #000; border: 1px solid var(--border);
            padding: 12px; color: var(--accent); font-family: inherit;
            outline: none; font-size: 14px; border-radius: 4px;
        }
        .btn-paste {
            background: #161b22; border: 1px solid var(--border); color: var(--text);
            padding: 0 15px; font-weight: bold; font-size: 12px; cursor: pointer;
            border-radius: 4px; transition: 0.2s;
        }
        .btn-paste:hover, .btn-paste:active { color: var(--accent); border-color: var(--accent); }

        .btn-exe {
            width: 100%; background: #161b22; border: 1px solid var(--accent);
            color: var(--accent); padding: 15px; font-weight: bold; font-size: 14px;
            cursor: pointer; text-transform: uppercase; transition: 0.2s; border-radius: 4px;
        }
        .btn-exe:active { transform: scale(0.98); background: var(--accent); color: #000; }
        
        /* Checkbox Auto-Redirect */
        .options-group {
            margin-top: 15px; display: flex; align-items: center; justify-content: center; gap: 8px;
            font-size: 12px; color: #8b949e;
        }
        .options-group input[type="checkbox"] { accent-color: var(--accent); cursor: pointer; }

        #console {
            background: #010409; border: 1px solid #21262d; border-radius: 4px;
            height: 120px; margin-top: 15px; padding: 10px;
            font-size: 11px; color: #8b949e; overflow-y: auto; text-align: left;
        }
        .line::before { content: ">> "; color: var(--green); }
        
        .result-panel {
            margin-top: 15px; padding: 15px; border: 1px solid var(--green); border-radius: 4px;
            background: rgba(0, 255, 65, 0.05); display: none;
        }
        #final-link { color: #fff; word-break: break-all; font-size: 12px; display: block; margin: 10px 0; }
        .copy-btn { background: var(--green); color: #000; border: none; padding: 8px 15px; font-size: 11px; font-weight: bold; width: 100%; cursor: pointer; border-radius: 2px;}
        
        .catalog {
            width: 100%; max-width: 500px; margin-top: 30px; margin-bottom: 30px;
            display: grid; grid-template-columns: 1fr 1fr; gap: 15px; opacity: 0.6;
        }
        .cat-item h3 { font-size: 0.75rem; color: var(--accent); margin: 0 0 5px 0; text-transform: uppercase; border-bottom: 1px solid var(--border); padding-bottom: 3px;}
        .cat-item ul { list-style: none; padding: 0; margin: 0; font-size: 0.65rem; color: #8b949e; line-height: 1.6;}
    </style>
</head>
<body>
<div class="main-frame">
    <h1>BYPASS_V5.SYS</h1>
    
    <div class="input-group">
        <input type="url" id="target-url" class="input-box" placeholder="URL_ALVO..." minlength="12">
        <button class="btn-paste" onclick="pasteText()">COLAR</button>
    </div>
    
    <button class="btn-exe" onclick="runBypass()" id="btn-run">INIT_DECODE()</button>

    <div class="options-group">
        <input type="checkbox" id="auto-redirect">
        <label for="auto-redirect">REDIRECIONAMENTO_AUTOMÁTICO</label>
    </div>

    <div id="console"><div class="line">Kernel carregado. Aguardando input...</div></div>
    
    <div class="result-panel" id="result-box">
        <span style="font-size: 10px; color: var(--green);">[SUCCESS] LINK EXTRAÍDO:</span>
        <div id="final-link"></div>
        <button class="copy-btn" onclick="copyLink()">COPY_TO_BUFFER</button>
    </div>
</div>

<div class="catalog">
    <div class="cat-item">
        <h3>Ad-links</h3>
        <ul>
            <li>Linkvertise.com</li><li>Admaven (Lootlabs/Lootlinks)</li>
            <li>Paster.so / Paster.gg</li><li>Work.ink</li>
            <li>Cuty.io / Cety.io</li><li>Boost.ink</li>
            <li>Adfoc.us</li><li>Mendationforc.info</li>
        </ul>
    </div>
    <div class="cat-item">
        <h3>Social Unlock</h3>
        <ul>
            <li>Rekonise.com</li><li>Mboost.me / Bst.gg</li>
            <li>Social-unlock.com</li><li>Socialwolvez.com</li>
            <li>Sub2get / Sub2unlock</li><li>Sub4unlock.io</li>
            <li>Subfinal.com</li><li>Unlocknow.net / Ytsubme</li>
        </ul>
    </div>
    <div class="cat-item">
        <h3>Paster Sites</h3>
        <ul>
            <li>Justpaste.it</li><li>Paste-drop.com</li>
            <li>Pastebin.com</li><li>Pastecanyon.com</li>
            <li>Pastehill.com</li><li>Pastemode.com</li><li>Rentry.org</li>
        </ul>
    </div>
    <div class="cat-item">
        <h3>Shorteners</h3>
        <ul>
            <li>Bit.ly</li><li>Cl.gy</li><li>Goo.gl</li><li>Is.Gd</li>
            <li>Rebrand.ly</li><li>Rkns.link</li><li>Shorter.me</li>
            <li>T.co / T.ly</li><li>Tiny.cc / Tinyurl</li><li>V.gd</li>
        </ul>
    </div>
</div>

<script>
    function log(m, c) {
        const con = document.getElementById('console');
        const d = document.createElement('div');
        d.className = 'line';
        if(c) d.style.color = c;
        d.innerText = m;
        con.appendChild(d);
        con.scrollTop = con.scrollHeight;
    }

    async function pasteText() {
        try {
            const text = await navigator.clipboard.readText();
            document.getElementById('target-url').value = text;
            log("Clipboard inserido no campo alvo.", "#00f2ff");
        } catch (err) {
            log("ERRO: O navegador bloqueou o acesso à área de transferência.", "#ff5f56");
        }
    }

    async function runBypass() {
        const url = document.getElementById('target-url').value;
        const autoOpen = document.getElementById('auto-redirect').checked;
        
        if(url.length < 12) return log("ERRO: URL muito curta ou inválida.", "#ff5f56");
        
        document.getElementById('btn-run').disabled = true;
        document.getElementById('result-box').style.display = "none";
        log("Sincronizando com engine...");
        
        try {
            const r = await fetch('/api/bypass', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            });
            const d = await r.json();
            
            if(d.success) {
                log("Decriptado com sucesso!", "#00ff41");
                document.getElementById('final-link').innerText = d.link;
                document.getElementById('result-box').style.display = "block";
                
                if (autoOpen) {
                    log("Iniciando redirecionamento automático...", "#ffbd2e");
                    setTimeout(() => { window.open(d.link, '_blank'); }, 800);
                }
            } else { log("FALHA: " + d.error, "#ff5f56"); }
        } catch(e) { log("ERRO_CONEXAO", "#ff5f56"); }
        finally { document.getElementById('btn-run').disabled = false; }
    }

    function copyLink() {
        navigator.clipboard.writeText(document.getElementById('final-link').innerText);
        log("Link salvo na área de transferência.", "#ffbd2e");
    }
</script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_PAGE)

@app.route('/api/bypass', methods=['POST'])
def api_bypass():
    data = request.json
    url_target = data.get('url')
    sessao = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}
    try:
        cap_resp = sessao.get('https://leak.sx/bypass_captcha.php', headers=headers, timeout=10)
        captcha = cap_resp.text.strip()
        res_resp = sessao.post('https://leak.sx/bypass_resolver.php', headers=headers, data={'url': url_target, 'captcha': captcha}, timeout=15)
        res_json = res_resp.json()
        if res_json.get('status') == 'success': return jsonify({'success': True, 'link': res_json.get('result')})
        return jsonify({'success': False, 'error': 'Link não suportado ou expirado.'})
    except: return jsonify({'success': False, 'error': 'Servidor offline.'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
