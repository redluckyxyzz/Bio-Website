from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# HTML from user (with minor adjustments for Flask)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
<title>RED LUCKY XYZ LONG BIO</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #000; color: white; font-family: 'Segoe UI', monospace; overflow-x: hidden; }
canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
.container { position: relative; z-index: 1; max-width: 500px; margin: 0 auto; padding: 16px 16px 30px; }

/* ===== HEADER BANNER CARD STYLES ===== */
.header-card {
    background: rgba(20, 25, 40, 0.75);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 16px 18px;
    margin: 10px 0 20px;
    border: 2px solid rgba(0, 255, 195, 0.4);
    box-shadow: 0 0 20px rgba(0, 255, 195, 0.15);
    display: flex;
    align-items: center;
    gap: 16px;
}
.header-logo-container {
    width: 75px;
    height: 75px;
    flex-shrink: 0;
    border-radius: 16px;
    border: 2px solid #00ffc3;
    overflow: hidden;
    box-shadow: 0 0 12px rgba(0, 255, 195, 0.4);
}
.header-logo-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.header-content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.header-title {
    font-size: 1.3rem;
    font-weight: 900;
    color: #00ffc3;
    text-shadow: 0 0 10px rgba(0, 255, 195, 0.5);
    letter-spacing: 0.5px;
    line-height: 1.2;
    margin-bottom: 10px;
}
.header-socials {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 12px;
    font-size: 0.72rem;
    color: #bbb;
}
.header-socials a {
    color: #fff;
    text-decoration: none;
    transition: color 0.2s;
    white-space: nowrap;
}
.header-socials a:hover {
    color: #00ffc3;
}
.header-socials i {
    color: #00ffc3;
    margin-right: 3px;
}

.card { background: rgba(20, 25, 40, 0.65); backdrop-filter: blur(12px); border-radius: 28px; padding: 18px; margin: 16px 0; border: 1px solid rgba(0,255,195,0.25); }
textarea { width: 100%; height: 130px; border-radius: 20px; background: #0a0a0e; border: 1px solid #00ffc3; color: white; padding: 14px; font-size: 15px; resize: vertical; font-family: monospace; }
.preview { margin-top: 12px; padding: 12px; background: #0a0a0e; border-radius: 20px; border: 1px solid #00ffc3; min-height: 65px; font-size: 15px; word-wrap: break-word; }

/* COMBINED CARD FORMATTING BUTTONS SECTION */
.formatting-section {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px dashed rgba(0, 255, 195, 0.25);
}
.formatting-title {
    font-size: 0.95rem;
    margin-bottom: 8px;
    color: #00ffc3;
}

button, .format-btn { background: linear-gradient(90deg, #00ffc3, #0099ff); border: none; border-radius: 40px; padding: 8px 14px; margin: 5px 4px 5px 0; font-weight: bold; color: black; cursor: pointer; font-size: 14px; }

/* COLORS SECTION STYLES WITH ICON BUTTON */
.colors-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.toggle-colors-btn {
    background: rgba(0, 255, 195, 0.15);
    border: 1px solid #00ffc3;
    color: #00ffc3;
    border-radius: 50%;
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 0;
    margin: 0;
}
.toggle-colors-btn:hover {
    background: #00ffc3;
    color: #000;
}
.colors-ribbon { 
    display: grid; 
    grid-template-columns: repeat(7, 1fr); 
    gap: 8px; 
    margin-top: 12px; 
    transition: max-height 0.4s ease, opacity 0.3s ease;
}
.colors-ribbon.hidden-colors {
    display: none;
}

.c-dot { height: 36px; border-radius: 12px; cursor: pointer; border: 1px solid rgba(255,255,255,0.3); }
input, select { width: 100%; padding: 12px; margin-top: 8px; border-radius: 60px; background: #0a0a0e; border: 1px solid #333; color: white; font-size: 14px; }
#overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); backdrop-filter: blur(20px); z-index: 1000; display: flex; flex-direction: column; justify-content: center; align-items: center; opacity: 0; visibility: hidden; transition: 0.2s; }
#overlay.active { opacity: 1; visibility: visible; }
.res-icon { font-size: 70px; margin-bottom: 16px; }
.res-title { font-size: 28px; font-weight: bold; }
.res-body { text-align: center; padding: 20px; max-width: 85%; word-break: break-word; }
.success .res-icon { color: #00ffc3; }
.error .res-icon { color: #ff5555; }

/* ===== GET EAT TOKEN BIG CARD ===== */
.eat-token-card {
    display: block;
    text-decoration: none;
    background: linear-gradient(135deg, rgba(20, 25, 40, 0.85), rgba(0, 153, 255, 0.15));
    backdrop-filter: blur(12px);
    border-radius: 28px;
    padding: 22px;
    margin: 16px 0;
    border: 2px solid #00ffc3;
    box-shadow: 0 0 20px rgba(0, 255, 195, 0.2);
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}
.eat-token-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 30px rgba(0, 255, 195, 0.4);
    border-color: #0099ff;
    background: linear-gradient(135deg, rgba(20, 25, 40, 0.95), rgba(0, 255, 195, 0.2));
}
.eat-token-text {
    font-size: 1.4rem;
    font-weight: 900;
    color: #00ffc3;
    text-shadow: 0 0 12px rgba(0, 255, 195, 0.6);
    letter-spacing: 1.5px;
}

/* ===== CAPTCHA STYLES ===== */
#captchaOverlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.95);
    backdrop-filter: blur(30px);
    z-index: 2000;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding: 20px;
}
#captchaOverlay.hidden {
    display: none;
}
.captcha-box {
    background: rgba(20, 25, 40, 0.95);
    border-radius: 32px;
    padding: 40px 30px 50px;
    max-width: 440px;
    width: 100%;
    border: 2px solid rgba(0,255,195,0.3);
    box-shadow: 0 0 80px rgba(0,255,195,0.1), inset 0 0 60px rgba(0,255,195,0.05);
    text-align: center;
    animation: captchaPulse 2s infinite;
}
@keyframes captchaPulse {
    0% { border-color: rgba(0,255,195,0.3); box-shadow: 0 0 80px rgba(0,255,195,0.1); }
    50% { border-color: rgba(0,255,195,0.6); box-shadow: 0 0 100px rgba(0,255,195,0.2); }
    100% { border-color: rgba(0,255,195,0.3); box-shadow: 0 0 80px rgba(0,255,195,0.1); }
}

.captcha-box img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    margin: -10px auto 15px;
    object-fit: cover;
    border: 2px solid #00ffc3;
    box-shadow: 0 0 15px #00ffc3, 0 0 30px rgba(0, 255, 195, 0.6);
    display: block;
}

.captcha-box h2 {
    color: #00ffc3;
    font-size: 1.5rem;
    margin-bottom: 6px;
    text-shadow: 0 0 20px rgba(0,255,195,0.3);
}
.captcha-box .sub-text {
    color: #aaa;
    font-size: 0.85rem;
    margin-bottom: 20px;
    line-height: 1.5;
}
.captcha-slider-container {
    background: #0a0a0e;
    border-radius: 60px;
    padding: 4px;
    border: 2px solid #333;
    position: relative;
    margin: 15px 0;
    display: flex;
    align-items: center;
    user-select: none;
    -webkit-user-select: none;
    touch-action: none;
    height: 60px;
    transition: border-color 0.3s;
}
.captcha-slider-container:hover,
.captcha-slider-container.active {
    border-color: #00ffc3;
}
.captcha-slider-track {
    flex: 1;
    height: 100%;
    border-radius: 60px;
    background: #1a1a2e;
    position: relative;
    overflow: hidden;
}
.captcha-slider-fill {
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #00ffc3, #0099ff);
    border-radius: 60px;
    transition: width 0.05s linear;
    position: absolute;
    left: 0;
    top: 0;
}
.captcha-slider-thumb {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00ffc3, #0099ff);
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: 2px;
    box-shadow: 0 0 30px rgba(0,255,195,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    color: #000;
    transition: left 0.05s linear, background 0.3s;
    z-index: 2;
    cursor: grab;
    touch-action: none;
}
.captcha-slider-thumb:active {
    cursor: grabbing;
}
.captcha-slider-thumb i {
    pointer-events: none;
}
.captcha-status {
    margin: 14px 0 8px;
    font-size: 0.95rem;
    min-height: 30px;
    font-weight: 500;
}
.captcha-status.verified {
    color: #00ffc3;
}
.captcha-status.failed {
    color: #ff5555;
}
.captcha-refresh {
    background: transparent;
    border: 1px solid #444;
    color: #aaa;
    padding: 8px 20px;
    border-radius: 25px;
    font-size: 0.8rem;
    cursor: pointer;
    margin-top: 5px;
    transition: all 0.3s;
}
.captcha-refresh:hover {
    border-color: #00ffc3;
    color: #00ffc3;
    background: rgba(0,255,195,0.05);
}
.captcha-progress-text {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.8rem;
    color: rgba(255,255,255,0.5);
    z-index: 1;
    font-weight: bold;
    letter-spacing: 0.5px;
    pointer-events: none;
    transition: color 0.3s;
}
.captcha-footer {
    margin-top: 15px;
    font-size: 0.7rem;
    color: #444;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}
.captcha-footer i {
    color: #00ffc3;
}
.captcha-lock {
    margin-bottom: 10px;
    color: #00ffc3;
    font-size: 14px;
}
.captcha-lock i {
    margin-right: 6px;
}

/* Mobile touch optimization */
@media (max-width: 480px) {
    .header-card {
        padding: 12px;
        gap: 12px;
    }
    .header-logo-container {
        width: 60px;
        height: 60px;
    }
    .header-title {
        font-size: 1.05rem;
        margin-bottom: 6px;
    }
    .header-socials {
        font-size: 0.65rem;
        gap: 4px 8px;
    }
    .captcha-slider-container {
        height: 56px;
    }
    .captcha-slider-thumb {
        width: 48px;
        height: 48px;
        font-size: 18px;
    }
    .captcha-box {
        padding: 30px 20px;
    }
}
</style>
</head>
<body>

<!-- ===== CAPTCHA OVERLAY - ALWAYS SHOWN ON PAGE LOAD ===== -->
<div id="captchaOverlay">
    <div class="captcha-box">
        <img src="https://i.ibb.co/mFXZW6pB/file-000000003c5c82118bd70d4024da7486.png" alt="Logo">
        <h2>🔒 Human Verification</h2>
        <p class="sub-text">Please verify you're human to access the tool</p>
        <div class="captcha-lock"><i class="fas fa-shield-alt"></i> Protected by advanced security</div>
        
        <div class="captcha-slider-container" id="sliderContainer">
            <div class="captcha-slider-track">
                <div class="captcha-slider-fill" id="sliderFill"></div>
                <span class="captcha-progress-text" id="progressText">Slide to verify</span>
            </div>
            <div class="captcha-slider-thumb" id="sliderThumb">
                <i class="fas fa-chevron-right"></i>
            </div>
        </div>
        <div class="captcha-status" id="captchaStatus">👉 Drag the slider to the right</div>
        <button class="captcha-refresh" onclick="resetCaptcha()">⟳ Refresh</button>
        <div class="captcha-footer">
            <i class="fas fa-check-circle"></i> Secure Connection
            <i class="fas fa-circle" style="font-size:4px; color:#333;"></i>
            <i class="fas fa-clock"></i> Session Active
        </div>
    </div>
</div>

<!-- ===== RESULT OVERLAY ===== -->
<div id="overlay">
    <i id="res-icon" class="fas fa-check-circle res-icon"></i>
    <div id="res-title" class="res-title"></div>
    <div id="res-body" class="res-body"></div>
</div>

<canvas id="matrix"></canvas>
<div class="container">
    
    <!-- ===== HEADER BOARD CARD ===== -->
    <div class="header-card">
        <div class="header-logo-container">
            <img src="https://i.ibb.co/0RZh07Ck/file-0000000016bc8211927fbaca183db97c.png" alt="Logo">
        </div>
        <div class="header-content">
            <div class="header-title">RED LUCKY XYZ BIO TOOL</div>
            <div class="header-socials">
                <a href="https://instagram.com/ly.luc4y" target="_blank"><i class="fab fa-instagram"></i>Instagram: ly.luc4y</a>
                <a href="https://t.me/Redluckyxyz" target="_blank"><i class="fab fa-telegram"></i>Telegram: Redluckyxyz</a>
                <a href="https://tiktok.com/@ly.luc4y" target="_blank"><i class="fab fa-tiktok"></i>Tiktok: ly.luc4y</a>
            </div>
        </div>
    </div>
    
    <!-- ===== COMBINED BIO EDITOR & FORMATTING CARD ===== -->
    <div class="card">
        <h3>✏️ Bio Editor</h3>
        <textarea id="bio" placeholder="Write your bio here..."></textarea>
        <div id="charCount" style="text-align:right; font-size:12px; margin-top:5px;">0 / 350</div>
        <div class="preview" id="preview">Live Preview</div>
        
        <!-- Formatting Options Inside the Same Card -->
        <div class="formatting-section">
            <div class="formatting-title">🎨 Formatting</div>
            <button class="format-btn" onclick="insertSimple('[b]')">Bold</button>
            <button class="format-btn" onclick="insertSimple('[i]')">Italic</button>
            <button class="format-btn" onclick="insertSimple('[c]')">Curve</button>
            <button class="format-btn" onclick="insertSimple('[u]')">Underline</button>
            <button class="format-btn" onclick="insertSimple('[s]')">Strike</button>
        </div>
    </div>

    <!-- ===== COLORS CARD WITH V-ICON TOGGLE BUTTON ===== -->
    <div class="card">
        <div class="colors-header">
            <h3>🌈 Colors</h3>
            <button class="toggle-colors-btn" id="toggleColorsBtn" onclick="toggleColors()"><i class="fas fa-chevron-up"></i></button>
        </div>
        <div class="colors-ribbon" id="colorRibbon"></div>
    </div>

    <div class="card">
        <h3>🔐 Auth Method</h3>
        <select id="method" onchange="togglePassword()">
            <option value="jwt">JWT Token (Direct)</option>
            <option value="uid">UID & Password</option>
            <option value="access">Access Token</option>
            <option value="eat">EAT Token</option>
        </select>
        <select id="serverSelect" style="margin-top: 10px;">
            <option value="IND">🇮🇳 IND - India</option>
            <option value="BD">🇧🇩 BD - Bangladesh</option>
            <option value="SG">🇸🇬 SG - Singapore</option>
            <option value="BR">🇧🇷 BR - Brazil</option>
            <option value="US">🇺🇸 US - USA</option>
            <option value="EU">🇪🇺 EU - Europe</option>
        </select>
        <input id="token" placeholder="Enter Token / UID" autocomplete="off">
        <input id="password" placeholder="Password" type="password" style="display:none;">
        <button id="submitBtn" onclick="handleSubmit()" style="width:100%; margin-top:15px;" disabled>🔒 Verify First</button>
    </div>

    <!-- ===== GET EAT TOKEN BIG CARD AT THE VERY BOTTOM ===== -->
    <a href="https://lucky-eat-token-website.lovable.app/" target="_blank" class="eat-token-card">
        <div class="eat-token-text">GET EAT TOKEN</div>
    </a>

</div>

<script>
// ========== MATRIX BACKGROUND ==========
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const letters = "VKBOY01";
const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = [];
for (let i = 0; i < columns; i++) drops[i] = 1;
function drawMatrix() {
    ctx.fillStyle = "rgba(0,0,0,0.05)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#00ffc3";
    ctx.font = fontSize + "px monospace";
    for (let i = 0; i < drops.length; i++) {
        let text = letters[Math.floor(Math.random() * letters.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
    }
    requestAnimationFrame(drawMatrix);
}
drawMatrix();

// ========== UTILITY FUNCTIONS ==========
function showResult(type, title, html) {
    const ov = document.getElementById('overlay');
    ov.className = type + " active";
    document.getElementById('res-icon').className = type === 'success' ? "fas fa-check-circle res-icon" : "fas fa-times-circle res-icon";
    document.getElementById('res-title').innerText = title;
    document.getElementById('res-body').innerHTML = html;
    setTimeout(() => { ov.className = ""; }, 5000);
}

function insertSimple(tag) {
    let bio = document.getElementById("bio");
    let start = bio.selectionStart;
    let end = bio.selectionEnd;
    let text = bio.value;
    let newText = text.substring(0, start) + tag + text.substring(end);
    bio.value = newText;
    bio.focus();
    bio.setSelectionRange(start + tag.length, start + tag.length);
    updatePreview();
}

function insertColor(color) {
    insertSimple('[' + color + ']');
}

function togglePassword() {
    let m = document.getElementById("method").value;
    let pwdField = document.getElementById("password");
    pwdField.style.display = (m === "uid") ? "block" : "none";
}

let lastValidBio = "";
function updatePreview() {
    let bio = document.getElementById("bio");
    if (bio.value.length > 350) {
        bio.value = lastValidBio;
        return;
    }
    lastValidBio = bio.value;
    document.getElementById("charCount").innerText = bio.value.length + " / 350";
    let raw = bio.value;
    let text = raw.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
    let result = '';
    let i = 0;
    let currentColor = null;
    let currentBold = false, currentItalic = false, currentCurve = false, currentUnderline = false, currentStrike = false;
    
    function applyCurrent() {
        let style = '';
        if (currentColor) style += `color:#${currentColor};`;
        if (currentBold) style += `font-weight:bold;`;
        if (currentItalic) style += `font-style:italic;`;
        if (currentCurve) style += `font-style:italic;`;
        if (currentUnderline) style += `text-decoration:underline;`;
        if (currentStrike) style += `text-decoration:line-through;`;
        if (style) return `<span style="${style}">`;
        return '';
    }
    
    let buffer = '';
    while (i < text.length) {
        if (text[i] === '[') {
            if (buffer) {
                let open = applyCurrent();
                result += open + buffer + (open ? '</span>' : '');
                buffer = '';
            }
            let endIdx = text.indexOf(']', i);
            if (endIdx === -1) {
                buffer += text[i];
                i++;
                continue;
            }
            let tag = text.substring(i+1, endIdx);
            i = endIdx + 1;
            if (/^[0-9A-Fa-f]{6}$/.test(tag)) {
                currentColor = tag;
            } else if (tag === 'b') {
                currentBold = !currentBold;
            } else if (tag === 'i') {
                currentItalic = !currentItalic;
            } else if (tag === 'c') {
                currentCurve = !currentCurve;
            } else if (tag === 'u') {
                currentUnderline = !currentUnderline;
            } else if (tag === 's') {
                currentStrike = !currentStrike;
            } else {
                buffer += '[' + tag + ']';
            }
        } else {
            buffer += text[i];
            i++;
        }
    }
    if (buffer) {
        let open = applyCurrent();
        result += open + buffer + (open ? '</span>' : '');
    }
    document.getElementById("preview").innerHTML = result || "Live Preview";
}

// ========== COLOR RIBBON ==========
const colors = ["#FF0000","#DC143C","#B22222","#8B0000","#FA8072","#FF7F50","#FF8C00","#FFA500","#FFD700","#FFFF00","#F0E68C","#98FB98","#00FF00","#32CD32","#00FF7F","#008000","#2E8B57","#556B2F","#808000","#40E0D0","#00FFFF","#00BFFF","#1E90FF","#4682B4","#0000FF","#0000CD","#00008B","#191970","#8A2BE2","#9370DB","#800080","#4B0082","#FF00FF","#EE82EE","#DA70D6","#FF1493","#FF69B4","#FFC0CB","#D2B48C","#D2691E","#A0522D","#8B4513","#FFFFFF","#C0C0C0","#A9A9A9","#808080","#696969","#2F4F4F","#000000"];
const ribbon = document.getElementById("colorRibbon");
colors.forEach(col => {
    let dot = document.createElement("div");
    dot.className = "c-dot";
    dot.style.backgroundColor = col;
    dot.onclick = () => insertColor(col.substring(1));
    ribbon.appendChild(dot);
});

// ========== TOGGLE COLORS WITH V-ICON FUNCTION ==========
function toggleColors() {
    const ribbon = document.getElementById("colorRibbon");
    const btn = document.getElementById("toggleColorsBtn");
    
    if (ribbon.classList.contains("hidden-colors")) {
        ribbon.classList.remove("hidden-colors");
        btn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    } else {
        ribbon.classList.add("hidden-colors");
        btn.innerHTML = '<i class="fas fa-chevron-down"></i>';
    }
}

document.getElementById("bio").addEventListener("input", updatePreview);
updatePreview();

// ========== SMART CAPTCHA (Touch Optimized) ==========
let captchaVerified = false;
let isDragging = false;
let startX = 0;
let currentX = 0;
let thumbLeft = 2;

const sliderContainer = document.getElementById('sliderContainer');
const sliderThumb = document.getElementById('sliderThumb');
const sliderFill = document.getElementById('sliderFill');
const progressText = document.getElementById('progressText');
const captchaStatus = document.getElementById('captchaStatus');
const captchaOverlay = document.getElementById('captchaOverlay');
const submitBtn = document.getElementById('submitBtn');

function getMaxLeft() {
    return sliderContainer.offsetWidth - sliderThumb.offsetWidth - 4;
}

function updateSlider(x) {
    const maxLeft = getMaxLeft();
    let left = Math.max(0, Math.min(x, maxLeft));
    const percent = (left / maxLeft) * 100;
    
    sliderThumb.style.left = (left + 2) + 'px';
    sliderFill.style.width = percent + '%';
    progressText.textContent = Math.round(percent) + '%';
    
    return left;
}

function handleStart(clientX) {
    const rect = sliderContainer.getBoundingClientRect();
    isDragging = true;
    startX = clientX - rect.left - sliderThumb.offsetWidth / 2;
    const currentLeft = parseFloat(sliderThumb.style.left) || 2;
    thumbLeft = currentLeft - 2;
    
    sliderThumb.style.transition = 'none';
    sliderFill.style.transition = 'none';
    sliderContainer.classList.add('active');
    
    captchaStatus.textContent = '🔓 Keep sliding...';
    captchaStatus.className = 'captcha-status';
    
    updateSlider(thumbLeft + (clientX - rect.left - sliderThumb.offsetWidth / 2 - startX));
}

function handleMove(clientX) {
    if (!isDragging) return;
    
    const rect = sliderContainer.getBoundingClientRect();
    const maxLeft = getMaxLeft();
    let newLeft = thumbLeft + (clientX - rect.left - sliderThumb.offsetWidth / 2 - startX);
    newLeft = Math.max(0, Math.min(newLeft, maxLeft));
    
    updateSlider(newLeft);
    
    if (newLeft >= maxLeft - 2) {
        isDragging = false;
        captchaVerified = true;
        captchaStatus.textContent = '✅ Verified Successfully!';
        captchaStatus.className = 'captcha-status verified';
        progressText.textContent = '✅ Verified';
        sliderThumb.style.background = 'linear-gradient(135deg, #00ffc3, #00cc88)';
        sliderThumb.innerHTML = '<i class="fas fa-check"></i>';
        sliderContainer.classList.remove('active');
        
        submitBtn.disabled = false;
        submitBtn.textContent = '🚀 UPDATE BIO';
        submitBtn.style.opacity = '1';
        
        setTimeout(() => {
            captchaOverlay.classList.add('hidden');
        }, 500);
    }
}

function handleEnd() {
    if (isDragging) {
        isDragging = false;
        sliderContainer.classList.remove('active');
        
        const maxLeft = getMaxLeft();
        const currentLeft = parseFloat(sliderThumb.style.left) || 2;
        
        if (currentLeft - 2 < maxLeft - 20) {
            sliderThumb.style.transition = 'left 0.4s ease';
            sliderFill.style.transition = 'width 0.4s ease';
            sliderThumb.style.left = '2px';
            sliderFill.style.width = '0%';
            progressText.textContent = 'Slide to verify';
            captchaStatus.textContent = '👉 Drag to the end to verify';
            captchaStatus.className = 'captcha-status';
            thumbLeft = 0;
        }
    }
}

sliderContainer.addEventListener('mousedown', function(e) {
    e.preventDefault();
    handleStart(e.clientX);
});

document.addEventListener('mousemove', function(e) {
    if (isDragging) {
        e.preventDefault();
        handleMove(e.clientX);
    }
});

document.addEventListener('mouseup', function(e) {
    if (isDragging) {
        handleEnd();
    }
});

sliderContainer.addEventListener('touchstart', function(e) {
    e.preventDefault();
    const touch = e.touches[0];
    handleStart(touch.clientX);
}, { passive: false });

document.addEventListener('touchmove', function(e) {
    if (isDragging) {
        e.preventDefault();
        const touch = e.touches[0];
        handleMove(touch.clientX);
    }
}, { passive: false });

document.addEventListener('touchend', function(e) {
    if (isDragging) {
        handleEnd();
    }
}, { passive: false });

function resetCaptcha() {
    captchaVerified = false;
    isDragging = false;
    thumbLeft = 0;
    
    sliderThumb.style.transition = 'left 0.4s ease';
    sliderFill.style.transition = 'width 0.4s ease';
    sliderThumb.style.left = '2px';
    sliderFill.style.width = '0%';
    progressText.textContent = 'Slide to verify';
    captchaStatus.textContent = '🔄 Verification reset';
    captchaStatus.className = 'captcha-status';
    sliderThumb.style.background = 'linear-gradient(135deg, #00ffc3, #0099ff)';
    sliderThumb.innerHTML = '<i class="fas fa-chevron-right"></i>';
    sliderContainer.classList.remove('active');
    
    captchaOverlay.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = '🔒 Verify First';
}

// ========== MAIN SUBMIT HANDLER ==========
async function handleSubmit() {
    if (!captchaVerified) {
        captchaOverlay.classList.remove('hidden');
        resetCaptcha();
        return;
    }
    
    await updateBio();
}

async function updateBio() {
    let method = document.getElementById("method").value;
    let token = document.getElementById("token").value.trim();
    let bio = document.getElementById("bio").value;
    let password = document.getElementById("password").value.trim();
    let server = document.getElementById("serverSelect").value;
    let btn = document.getElementById("submitBtn");
    
    if (!token) { alert("Token required!"); return; }
    if (!bio) { alert("Bio is required!"); return; }
    if (bio.length < 3) { alert("Bio too short! Minimum 3 characters."); return; }
    
    let body = { token, bio, server, method };
    if (method === "uid") {
        if (!password) { alert("Password required!"); return; }
        body.password = password;
    }
    
    let original = btn.innerText;
    btn.innerText = "⏳ Processing...";
    btn.disabled = true;
    
    try {
        let res = await fetch("/api/update", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(body)
        });
        let data = await res.json();
        
        if (data.status === "success") {
            showResult('success', '✅ SUCCESS!', `
                <div style="text-align:center; padding:10px;">
                    <div style="margin:5px 0;"><strong>🆔 UID:</strong> ${data.uid || data.user_id || 'N/A'}</div>
                    <div style="margin:5px 0;"><strong>👤 Nickname:</strong> ${data.name || 'N/A'}</div>
                    <div style="margin:5px 0;"><strong>🌍 Region:</strong> ${data.region_used || 'N/A'}</div>
                    <div style="margin:5px 0;"><strong>🔑 Method:</strong> ${data.login_method || 'N/A'}</div>
                    <div style="margin-top:10px; color:#00ffc3;">✅ ${data.message || 'Bio updated successfully'}</div>
                </div>
            `);
            
            document.getElementById("token").value = "";
            document.getElementById("password").value = "";
            document.getElementById("bio").value = "";
            lastValidBio = "";
            updatePreview();
        } else {
            showResult('error', '❌ FAILED', data.message || data.error || 'Unknown error');
        }
    } catch(e) {
        showResult('error', '⚠️ ERROR', e.message);
    } finally {
        btn.innerText = original;
        btn.disabled = false;
    }
}

window.addEventListener('load', () => {
    submitBtn.disabled = true;
    submitBtn.textContent = '🔒 Verify First';
});

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
</script>
</body>
</html>
"""

API_BASE_URL = "https://drogon-bio-api.vercel.app/bio"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/update', methods=['POST'])
def update_bio():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Missing JSON body"}), 400

        method = data.get('method', 'jwt')
        bio = data.get('bio', '').strip()
        server = data.get('server', 'IND')
        token = data.get('token', '').strip()
        password = data.get('password', '').strip()

        if not bio:
            return jsonify({"status": "error", "message": "Bio is required"}), 400
        if not token:
            return jsonify({"status": "error", "message": "Token/UID is required"}), 400

        params = {"bio": bio}

        if method == 'uid':
            if not password:
                return jsonify({"status": "error", "message": "Password required for UID method"}), 400
            params['uid'] = token
            params['pass'] = password
        elif method == 'jwt':
            params['jwt'] = token
        elif method == 'eat':
            params['eat'] = token
        elif method == 'access':
            params['access'] = token
        else:
            return jsonify({"status": "error", "message": f"Unsupported method: {method}"}), 400

        # Server selection via region param (optional, but we include it)
        # The API doesn't explicitly document server param, but we pass it as region if needed
        params['region'] = server  # Some APIs use 'region'

        # Make the request to the external API
        response = requests.get(API_BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        api_data = response.json()

        # Extract relevant fields for frontend
        result = {
            "status": "success" if api_data.get('success') else "error",
            "message": api_data.get('status', 'Bio updated'),
            "uid": api_data.get('uid'),
            "name": api_data.get('name'),
            "region_used": api_data.get('region_used'),
            "login_method": api_data.get('login_method'),
            "server_response": api_data.get('server_response'),
            "generated_jwt": api_data.get('generated_jwt'),  # if returned
            "http_code": api_data.get('http_code'),
        }

        # If API returned success=false, treat as error
        if not api_data.get('success', False):
            result["status"] = "error"
            result["message"] = api_data.get('status', 'API returned failure')

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"API request failed: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
