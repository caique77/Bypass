from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TERMINAL // ADBYPASS_V3</title>
    <style>
        :root { --bg: #050505; --surface: #0d0d0d; --accent: #ff1493; --green: #00ff41; --text: #cccccc; --border: #222; }
        body { background: var(--bg); color: var(--text); font-family: 'Courier New', Courier, monospace; margin: 0; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .terminal-window { width: 100%; max-width: 800px; background: var(--surface); border: 1px solid var(--border); border-radius: 6px; box-shadow: 0 15px 50px rgba(0,0,0,0.8); overflow: hidden; }
        .terminal-header { background: #1a1a1a; padding: 10px 15px; display: flex; gap: 8px; border-bottom: 1px solid var(--border); }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .red { background: #ff5f56; } .yellow { background: #ffbd2e; } .green { background: #27c93f; }
        .content { padding: 30px; }
        h1 { font-size: 1.2rem; color: var(--accent); margin: 0 0 20px 0; text-transform: uppercase; letter-spacing: 2px; }
        input { width: 100%; background: #000; border: 1px solid var(--border); padding: 15px; color: var(--green); font-family: inherit; border-radius: 4px; outline: none; box-sizing: border-box; font-size: 14px; margin-bottom: 20px; }
        input:focus { border-color: var(--accent); }
        button { width: 100%; background: transparent; border: 1px solid var(--accent); color: var(--accent); padding: 12px; font-family: inherit; cursor: pointer; text-transform: uppercase; font-weight: bold; transition: 0.3s; }
        button:hover { background: var(--accent); color: #fff; box-shadow: 0 0 15px var(--accent); }
        #log-container { background: #000; border: 1px solid #1a1a1a; padding: 15px; height: 150px; overflow-y: auto; margin-top: 20px; font-size: 13px; line-height: 1.5; color: var(--green); text-align: left;}
        .log-entry::before { content: "> "; }
        .result-area { margin-top: 20px; padding: 15px; border: 1px solid var(--green); background: rgba(0, 255, 65, 0.05); display: none; text-align: center;}
        .copy-btn { margin-top: 10px; padding: 5px 15px; font-size: 11px; border-color: var(--green); color: var(--green); width: auto; }
        .catalog { margin-top: 40px; width: 100%; max-width: 800px; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; font-size: 0.75rem; opacity: 0.6; }
        .cat-box h3 { color: var(--accent); font-size: 0.8rem; border-bottom: 1px solid #222; padding-bottom: 5px; }
        .cat-box ul { list-style: none; padding: 0; }
    </style>
</head>
<body>
<div class="terminal-window">
    <div class="terminal-header"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div class="content">
        <h1>Bypass_System // v3.0</h1>
        <input type="url" id="url-input" placeholder="COLE A URL ALVO AQUI..." minlength="12" maxlength="500">
        <button onclick="startBypass()" id="main-btn">Execute_Bypass()</button>
        <div id="log-container"><div class="log-entry">Aguardando entrada de dados...</div></div>
        <div class="result-area" id="result-box">
            <div style="font-size: 11px; margin-bottom: 5px;">[+][DECRYPT_SUCCESS] DESTINO ENCONTRADO:</div>
            <div id="final-link" style="color: #fff; word-break: break-all; margin-bottom:10px;"></div>
            <button class="copy-btn" onclick="copyToClipboard()">Copiar_Link</button>
        </div>
    </div>
</div>
<div class="catalog">
    <div class="cat-box"><h3>Popular Ad-links</h3><ul><li>Linkvertise.com</li><li>Admaven / Lootlabs</li><li>Work.ink / Cuty.io</li></ul></div>
    <div class="cat-box"><h3>Social Unlock</h3><ul><li>Rekonise.com</li><li>Mboost.me / Bst.gg</li><li>Sub2get / Sub4unlock</li></ul></div>
    <div class="cat-box"><h3>Shorteners</h3><ul><li>Bit.ly / TinyURL</li><li>Pastebin / Rentry</li></ul></div>
</div>
<script>
    function addLog(msg, color) {
        const log = document.getElementById('log-container');
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        if(color) entry.style.color = color;
        entry.innerText = msg;
        log.appendChild(entry);
        log.scrollTop = log.scrollHeight;
    }
    async function startBypass() {
        const url = document.getElementById('url-input').value.trim();
        const resultBox = document.getElementById('result-box');
        if(url.length < 12) { addLog("ERRO: URL muito curta.", "#ff5f56"); return; }
        document.getElementById('main-btn').disabled = true;
        resultBox.style.display = "none";
        addLog("Protocolo iniciado...");
        addLog("Estabelecendo conexão...");
        try {
            const response = await fetch('/api/bypass', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            });
            const data = await response.json();
            if(data.success) {
                addLog("Link decriptado com sucesso!", "#00ff41");
                document.getElementById('final-link').innerText = data.link;
                resultBox.style.display = "block";
            } else { addLog("FALHA: " + data.error, "#ff5f56"); }
        } catch(e) { addLog("ERRO CRÍTICO na API.", "#ff5f56"); }
        finally { document.getElementById('main-btn').disabled = false; }
    }
    function copyToClipboard() {
        const link = document.getElementById('final-link').innerText;
        navigator.clipboard.writeText(link);
        addLog("Copiado para a área de transferência.", "#ffbd2e");
    }
</script>
</body></html>
"""

@app.route('/')
def index(): return render_template_string(HTML_PAGE)

@app.route('/api/bypass', methods=['POST'])
def api_bypass():
    data = request.json
    url_target = data.get('url')
    if not url_target or len(url_target) < 12: return jsonify({'success': False, 'error': 'Entrada inválida.'})
    sessao = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}
    try:
        cap_resp = sessao.get('https://leak.sx/bypass_captcha.php', headers=headers, timeout=10)
        captcha = cap_resp.text.strip()
        res_resp = sessao.post('https://leak.sx/bypass_resolver.php', headers=headers, data={'url': url_target, 'captcha': captcha}, timeout=15)
        res_json = res_resp.json()
        if res_json.get('status') == 'success': return jsonify({'success': True, 'link': res_json.get('result')})
        return jsonify({'success': False, 'error': 'Link não suportado.'})
    except: return jsonify({'success': False, 'error': 'Timeout na rede.'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
