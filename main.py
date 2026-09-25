from flask import Flask, request, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

# HTML from user (with minor adjustments for Flask)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
<title>LUCKY X LONG BIO</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
/* ===== GLOBAL STYLES ===== */
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
body {
    background:
        radial-gradient(circle at 82% 8%, rgba(255, 0, 153, 0.13), transparent 24%),
        radial-gradient(circle at 18% 28%, rgba(0, 153, 255, 0.10), transparent 26%),
        linear-gradient(180deg, #050910 0%, #070b12 55%, #04070d 100%);
    color: #dce7f7;
    overflow-x: hidden;
    min-height: 100vh;
    position: relative;
}

/* ===== SAKURA (FLOWER) ANIMATION ===== */
.sakura {
    position: fixed;
    top: -10%;
    z-index: 0;
    user-select: none;
    pointer-events: none;
    animation: fall linear infinite;
    filter: drop-shadow(0 0 5px rgba(255, 105, 180, 0.5));
}
@keyframes fall {
    0% { transform: translateY(-10vh) rotate(0deg) scale(0.8); opacity: 1; }
    100% { transform: translateY(110vh) rotate(360deg) scale(1.2); opacity: 0; }
}

.container { position: relative; z-index: 1; max-width: 720px; margin: 0 auto; padding: 24px 16px 50px; }

/* ===== MULTI-COLOR GLASSMORPHISM CARDS (40% OPACITY) ===== */
.card, .header-card {
    background: rgba(7, 12, 19, 0.78);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 24px;
    border: 1px solid rgba(70, 108, 150, 0.34);
    box-shadow: 0 12px 45px rgba(0, 0, 0, 0.38), inset 0 1px 0 rgba(255,255,255,0.025);
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.card:hover {
    border-color: rgba(0, 179, 255, 0.42);
    box-shadow: 0 12px 42px rgba(0, 130, 255, 0.12);
}

/* ===== HEADER BANNER ===== */
.header-card {
    padding: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
    border-top: 2px solid #00b7d8; 
}
.header-logo-container {
    width: 80px; height: 80px; flex-shrink: 0;
    border-radius: 12px;
    padding: 4px;
    background: linear-gradient(135deg, #0055ff, #8a2be2, #ff1493);
    box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
}
.header-logo-container img {
    width: 100%; height: 100%; object-fit: cover; 
    border-radius: 10px; 
    border: 2px solid #111;
}
.header-title {
    font-size: 1.5rem; font-weight: 800;
    background: linear-gradient(90deg, #00b8ff, #d900ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
    letter-spacing: 1px;
}

/* ===== EDITOR & INPUTS ===== */
.card { padding: 25px; }
.card h3 { font-size: 1.1rem; color: #fff; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; font-weight: 600; }
.card h3 i { color: #ff1493; }

textarea {
    width: 100%; height: 120px;
    border-radius: 16px; background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255,255,255,0.1); color: white;
    padding: 15px; font-size: 14px; resize: vertical;
    transition: all 0.3s;
}
textarea:focus, input:focus, select:focus {
    outline: none; 
    border-color: #008cff; 
    background: rgba(0, 0, 0, 0.5);
    box-shadow: 0 0 18px rgba(0, 140, 255, 0.20);
}
.preview {
    margin-top: 15px; padding: 15px; background: rgba(0, 0, 0, 0.3);
    border-radius: 16px; border-left: 4px solid #00a8ff;
    min-height: 65px; font-size: 14px; word-wrap: break-word; color: #ddd;
}

/* ===== TEXT FORMATTING BUTTONS ===== */
.formatting-section { margin-top: 20px; padding-top: 15px; border-top: 1px dashed rgba(255, 255, 255, 0.1); }
.formatting-title { font-size: 0.9rem; margin-bottom: 10px; color: #aaa; font-weight: 600; }
.format-btn {
    border: none; border-radius: 8px; padding: 6px 14px; margin: 4px; 
    font-weight: 600; cursor: pointer; transition: all 0.2s; color: #fff;
}
.btn-bold { background: linear-gradient(135deg, #0055ff, #00a8ff); }
.btn-italic { background: linear-gradient(135deg, #8a2be2, #c71585); }
.btn-curve { background: linear-gradient(135deg, #ff1493, #ff69b4); }
.btn-underline { background: linear-gradient(135deg, #00b894, #00cec9); }
.btn-strike { background: linear-gradient(135deg, #e17055, #fab1a0); }
.format-btn:hover { transform: translateY(-2px); filter: brightness(1.2); }

/* ===== SYMBOL BUTTONS ===== */
.symbols-container {
    display: flex; flex-wrap: wrap; gap: 6px; margin-top: 5px;
}
.symbol-btn {
    background: rgba(20, 20, 35, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    padding: 6px 12px;
    color: #fff;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.symbol-btn:hover {
    background: linear-gradient(135deg, #ff1493, #8a2be2);
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(138, 43, 226, 0.4);
}

/* ===== SYMBOLS DASHBOARD ===== */
.symbols-card {
    position: relative;
    overflow: hidden;
    border-color: rgba(61, 94, 131, 0.45);
}
.symbols-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00b7d8 0%, #7a32ff 55%, #ff008c 100%);
}
.symbols-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
}
.symbols-title h3 {
    margin: 0 0 4px;
    font-size: 1.1rem;
}
.symbols-subtitle {
    display: block;
    color: #8896aa;
    font-size: 12px;
}
.symbols-toggle {
    width: 48px;
    height: 48px;
    flex: 0 0 48px;
    border: 1px solid rgba(0, 183, 216, 0.45);
    border-radius: 14px;
    background: rgba(2, 7, 14, 0.78);
    color: #9aa9bd;
    font-size: 19px;
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 0 0 rgba(0,0,0,0);
}
.symbols-toggle:hover, .symbols-toggle.active {
    color: #fff;
    border-color: #00b7d8;
    background: linear-gradient(135deg, #00a8ff, #7a32ff);
    box-shadow: 0 0 18px rgba(0, 168, 255, 0.28);
    transform: translateY(-1px);
}
.symbols-panel {
    margin-top: 18px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.08);
}
.symbols-panel[hidden] { display: none; }
.symbols-panel .symbols-container {
    margin-top: 0;
}

/* ===== COLORS SECTION ===== */
.colors-header { display: flex; justify-content: flex-start; align-items: center; }
.colors-ribbon { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; margin-top: 15px; }
.c-dot { 
    height: 32px; 
    border-radius: 6px;
    cursor: pointer; border: 2px solid transparent; transition: 0.2s; box-shadow: 0 4px 10px rgba(0,0,0,0.4); 
}
.c-dot:hover { transform: scale(1.15); border-color: #fff; }

/* ===== INPUT FIELDS ===== */
input, select {
    width: 100%; padding: 14px 18px; margin-top: 12px;
    border-radius: 12px; background: rgba(2, 7, 14, 0.78);
    border: 1px solid rgba(80, 116, 153, 0.34); color: #fff; font-size: 14px; appearance: none;
}
select option { background: #0a1019; color: #fff; }

/* ===== AUTHENTICATION DASHBOARD ===== */
.auth-card {
    padding: 28px 30px 30px;
    position: relative;
    overflow: hidden;
    border-color: rgba(61, 94, 131, 0.45);
}
.auth-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #00b7d8 25%, #7a32ff 65%, #ff008c 100%);
    opacity: 0.9;
}
.auth-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    margin-bottom: 30px;
}
.auth-heading {
    display: flex;
    align-items: center;
    gap: 18px;
    min-width: 0;
}
.auth-icon {
    width: 82px;
    height: 82px;
    flex: 0 0 82px;
    display: grid;
    place-items: center;
    border-radius: 18px;
    font-size: 42px;
    background: linear-gradient(145deg, #04b7ff, #1469ed);
    box-shadow: 0 0 30px rgba(0, 156, 255, 0.42);
}
.auth-heading h3 {
    margin: 0;
    font-size: clamp(1.55rem, 4vw, 2.45rem);
    letter-spacing: 0.4px;
    color: #fff;
    font-weight: 800;
}
.get-token-btn {
    flex: 0 0 auto;
    min-width: 260px;
    padding: 20px 30px;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: #fff;
    text-decoration: none;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    background: linear-gradient(105deg, #ed008d 0%, #b00cff 48%, #8c20ff 100%);
    border: 1px solid rgba(255, 111, 211, 0.9);
    box-shadow: 0 0 30px rgba(224, 0, 167, 0.28), 0 8px 22px rgba(0,0,0,0.25);
    transition: transform .25s ease, filter .25s ease, box-shadow .25s ease;
}
.get-token-btn:hover {
    transform: translateY(-3px);
    filter: brightness(1.08);
    box-shadow: 0 0 38px rgba(224, 0, 167, 0.40), 0 10px 28px rgba(0,0,0,0.30);
}
.auth-tabs {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 28px;
}
.auth-tab {
    appearance: none;
    border: 1px solid rgba(70, 102, 142, 0.42);
    border-radius: 18px;
    padding: 18px 14px;
    min-height: 74px;
    background: rgba(2, 7, 14, 0.56);
    color: #9eabc1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    font-size: 1.12rem;
    font-weight: 800;
    cursor: pointer;
    transition: .25s ease;
}
.auth-tab i { font-size: 1.35rem; }
.auth-tab.active {
    color: #eaf7ff;
    border-color: #148cff;
    background: linear-gradient(105deg, rgba(16, 95, 155, 0.28), rgba(0, 174, 209, 0.10));
    box-shadow: 0 0 24px rgba(0, 120, 255, 0.18), inset 0 0 22px rgba(0, 150, 255, 0.05);
}
.auth-tab:hover { border-color: rgba(0, 156, 255, 0.7); color: #fff; }
.auth-label {
    display: block;
    margin: 0 0 10px 10px;
    color: #a9b9d2;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.region-select { margin-bottom: 12px; cursor: pointer; appearance: auto; }
.auth-input-wrap { position: relative; }
.auth-input {
    margin: 0;
    min-height: 72px;
    padding: 18px 22px;
    border-radius: 18px;
    background: rgba(2, 7, 14, 0.74);
    border: 1px solid rgba(80, 116, 153, 0.48);
    font-size: 1.18rem;
    color: #eef6ff;
}
.auth-input::placeholder { color: #707b8d; opacity: 1; }
.auth-input:focus {
    border-color: #168cff;
    box-shadow: 0 0 0 1px rgba(22,140,255,.28), 0 0 24px rgba(0, 140, 255, .12);
    background: rgba(2, 8, 16, 0.9);
}
.auth-password { margin-top: 14px; }
.auth-submit {
    margin-top: 26px;
    width: 100%;
    min-height: 70px;
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: #fff;
    background: linear-gradient(105deg, #ed008d 0%, #b00cff 48%, #8c20ff 100%);
    border: 1px solid rgba(255, 111, 211, 0.9);
    box-shadow: 0 0 30px rgba(224, 0, 167, 0.28), 0 8px 22px rgba(0,0,0,0.25);
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    transition: transform .25s ease, filter .25s ease, box-shadow .25s ease;
}
.auth-submit:hover {
    transform: translateY(-3px);
    filter: brightness(1.08);
    box-shadow: 0 0 38px rgba(224, 0, 167, 0.40), 0 10px 28px rgba(0,0,0,0.30);
}
.auth-submit:disabled { opacity: .55; }

/* ===== GET TOKEN / HOW TO USE ===== */
.eat-token-card {
    display: block; text-decoration: none; padding: 18px; text-align: center;
    border-radius: 18px;
    background: linear-gradient(105deg, rgba(237, 0, 141, 0.18), rgba(145, 16, 255, 0.18));
    border: 1px solid rgba(236, 0, 159, 0.55);
    box-shadow: 0 0 20px rgba(215, 0, 159, 0.14);
    transition: all 0.3s ease;
    margin-bottom: 14px;
}
.eat-token-card:hover { transform: translateY(-3px); border-color: #a739ff; box-shadow: 0 0 28px rgba(175, 25, 255, 0.28); }
.eat-token-text { font-size: 1.2rem; font-weight: 800; color: #fff; letter-spacing: 1px; }
.how-to-use-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    width: 100%;
    min-height: 58px;
    margin: 0 0 20px;
    border-radius: 16px;
    text-decoration: none;
    color: #fff;
    background: rgba(12, 18, 28, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 0 18px rgba(0,0,0,.18);
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: .8px;
    transition: .25s ease;
}
.how-to-use-btn i { color: #ff214f; font-size: 1.45rem; }
.how-to-use-btn:hover { border-color: rgba(255, 33, 79, .55); transform: translateY(-2px); }

/* ===== SOCIAL MEDIA PILL BUTTONS ===== */
.social-footer { display: flex; justify-content: space-between; gap: 10px; margin-top: 10px; }
.social-btn {
    flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px;
    padding: 12px 5px; border-radius: 30px; background: rgba(10, 16, 25, 0.82);
    border: 1px solid rgba(255,255,255,0.1); color: #c7d0df; text-decoration: none;
    font-size: 13px; font-weight: 600; transition: all 0.3s ease; backdrop-filter: blur(10px);
}
.social-btn:hover { transform: translateY(-3px); color: #fff; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
.social-btn i { font-size: 16px; }
.btn-tg:hover { border-color: #00a8ff; background: rgba(0, 168, 255, 0.1); }
.btn-tg i { color: #00a8ff; }
.btn-ig:hover { border-color: #ff1493; background: rgba(255, 20, 147, 0.1); }
.btn-ig i { color: #ff1493; }
.btn-yt:hover { border-color: #ff0000; background: rgba(255, 0, 0, 0.1); }
.btn-yt i { color: #ff0000; }

@media (max-width: 680px) {
    .auth-card { padding: 22px 18px 24px; }
    .auth-top { align-items: stretch; flex-direction: column; }
    .get-token-btn { width: 100%; min-width: 0; }
    .auth-tabs { gap: 8px; }
    .auth-tab { min-height: 66px; padding: 12px 6px; font-size: .88rem; gap: 7px; }
    .auth-tab i { font-size: 1.1rem; }
    .auth-input { min-height: 64px; font-size: 1rem; }
}

/* ===== RESULT OVERLAY ===== */
#overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.9); backdrop-filter: blur(15px); z-index: 3000;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    opacity: 0; visibility: hidden; transition: 0.3s;
}
#overlay.active { opacity: 1; visibility: visible; }
.res-icon { font-size: 70px; margin-bottom: 20px; }
.res-title { font-size: 26px; font-weight: 800; color: #fff; }
.res-body { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 16px; margin-top: 15px; text-align: left; max-width: 85%; color: #ddd; border: 1px solid rgba(255,255,255,0.1); }
.success .res-icon { color: #00ffc3; text-shadow: 0 0 20px rgba(0,255,195,0.5); }
.error .res-icon { color: #ff4757; text-shadow: 0 0 20px rgba(255,71,87,0.5); }
.result-card { width:min(92vw,560px); max-height:88vh; overflow:auto; background:rgba(10,15,25,.96); border:1px solid rgba(255,255,255,.12); border-radius:24px; padding:28px 22px 24px; text-align:center; box-shadow:0 20px 70px rgba(0,0,0,.55); }
.result-preview-label { color:#8e9bb0; font-size:12px; font-weight:700; letter-spacing:1.5px; margin:18px 0 8px; text-transform:uppercase; }
.result-preview { width:100%; min-height:100px; padding:18px; border-radius:16px; background:rgba(0,0,0,.34); border:1px solid rgba(0,183,216,.25); border-left:4px solid #00a8ff; text-align:left; word-wrap:break-word; white-space:pre-wrap; user-select:none; -webkit-user-select:none; pointer-events:none; cursor:default; }
.result-meta { margin-bottom:12px; color:#aebbd0; font-size:13px; }
.result-status { margin-bottom:12px; font-weight:800; font-size:15px; }
.result-cancel { width:100%; margin-top:18px; min-height:54px; border:1px solid rgba(255,255,255,.14); border-radius:15px; background:linear-gradient(105deg,#ed008d,#8c20ff); color:#fff; font-size:16px; font-weight:800; cursor:pointer; }
.result-cancel:hover { filter:brightness(1.08); transform:translateY(-1px); }


/* ===== WELCOME POPUP STYLES (DEEP BORDER, NO SHADOW) ===== */
#welcome-popup {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.85); backdrop-filter: blur(10px); z-index: 4000;
    display: flex; justify-content: center; align-items: center;
    opacity: 0; visibility: hidden; transition: 0.4s ease;
}
#welcome-popup.active { opacity: 1; visibility: visible; }
.popup-content {
    background: rgba(25, 20, 35, 0.95);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 3px solid #ff1493; /* Deep solid color border, no shadow */
    border-radius: 20px;
    padding: 30px;
    width: 90%; max-width: 400px;
    text-align: center;
    position: relative;
    transform: scale(0.8);
    transition: transform 0.4s ease;
}
#welcome-popup.active .popup-content { transform: scale(1); }
.popup-title { 
    font-size: 1.8rem; 
    font-weight: 800; 
    color: #fff; 
    margin-bottom: 10px;
}
.popup-text { font-size: 14px; color: #e0e0e0; margin-bottom: 25px; line-height: 1.5; font-weight: 400; }
.popup-links { display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; }
.popup-btn {
    display: flex; align-items: center; justify-content: center; gap: 10px;
    padding: 12px; border-radius: 12px; text-decoration: none; font-weight: 600;
    color: #fff; font-size: 15px; transition: 0.3s ease; border: 1px solid transparent;
}
.popup-btn.tg { background: rgba(0, 168, 255, 0.2); border-color: rgba(0, 168, 255, 0.6); }
.popup-btn.tg:hover { background: #00a8ff; }
.popup-btn.ig { background: rgba(255, 20, 147, 0.2); border-color: rgba(255, 20, 147, 0.6); }
.popup-btn.ig:hover { background: #ff1493; }
.popup-btn.yt { background: rgba(255, 0, 0, 0.2); border-color: rgba(255, 0, 0, 0.6); }
.popup-btn.yt:hover { background: #ff0000; }
.close-popup-btn {
    background: transparent; color: #aaa; border: none; font-size: 14px; cursor: pointer;
    text-decoration: underline; transition: 0.3s ease;
}
.close-popup-btn:hover { color: #fff; }

/* ===== FLOATING TELEGRAM HELP ===== */
.telegram-help { position:fixed; right:18px; bottom:18px; z-index:2500; display:flex; flex-direction:column; align-items:center; gap:7px; text-decoration:none; animation:telegramFloat 2.2s ease-in-out infinite; }
.telegram-help-label { display:flex; align-items:center; gap:6px; padding:5px 10px; border-radius:12px; background:rgba(8,15,25,.92); border:1px solid rgba(0,168,255,.35); color:#fff; font-size:11px; font-weight:700; box-shadow:0 5px 18px rgba(0,0,0,.28); white-space:nowrap; }
.telegram-help-label i { color:#00a8ff; font-size:12px; }
.telegram-help-icon { width:52px; height:52px; border-radius:50%; display:grid; place-items:center; background:#229ED9; color:#fff; font-size:25px; box-shadow:0 7px 22px rgba(34,158,217,.35); border:2px solid rgba(255,255,255,.18); transition:transform .2s ease, filter .2s ease; }
.telegram-help:hover .telegram-help-icon { transform:scale(1.06); filter:brightness(1.08); }
@keyframes telegramFloat { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-8px); } }
@media (max-width:680px) { .telegram-help { right:14px; bottom:14px; } .telegram-help-icon { width:50px; height:50px; font-size:24px; } }
</style>
</head>
<body>

<!-- WELCOME POPUP -->
<div id="welcome-popup">
    <div class="popup-content">
        <div class="popup-title">Welcome...🫡 <i class="fas fa-sparkles" style="color: #ff1493;"></i></div>
        <div class="popup-text">Stay connected with us for the latest updates, tips, and secure methods. Please join our community!</div>
        
        <div class="popup-links">
            <a href="https://t.me/LuckyOfficialChannel" target="_blank" class="popup-btn tg">
                <i class="fab fa-telegram"></i> Join Telegram
            </a>
            <a href="https://www.instagram.com/lllux96" target="_blank" class="popup-btn ig">
                <i class="fab fa-instagram"></i> Follow Instagram
            </a>
            <a href="https://youtube.com/@redluckyxyz" target="_blank" class="popup-btn yt">
                <i class="fab fa-youtube"></i> Subscribe YouTube
            </a>
        </div>
        
        <button class="close-popup-btn" onclick="closePopup()">Maybe Later</button>
    </div>
</div>

<!-- RESULT OVERLAY -->
<!-- FLOATING TELEGRAM HELP BUTTON -->
<a class="telegram-help" href="https://t.me/Redluckyxyz" target="_blank" rel="noopener noreferrer" aria-label="Any Help on Telegram">
    <span class="telegram-help-label"><i class="fas fa-comment-dots"></i> any help</span>
    <span class="telegram-help-icon"><i class="fab fa-telegram-plane"></i></span>
</a>

<div id="overlay">
    <div class="result-card">
        <i id="res-icon" class="fas fa-check-circle res-icon"></i>
        <div id="res-title" class="res-title"></div>
        <div id="res-body" class="res-body"></div>
        <button type="button" class="result-cancel" onclick="closeResult()">CANCEL</button>
    </div>
</div>

<div class="container">
    
    <!-- HEADER -->
    <div class="header-card">
        <div class="header-logo-container">
            <img src="https://i.ibb.co/mCQ9nwt5/file-00000000381c81fd8e48d208757b5a49.png" alt="Logo">
        </div>
        <div class="header-content">
            <div class="header-title">LUCKY X LONG BIO</div>
            <div style="font-size:12px; color:#aaa;">✅ 100% Safe method</div>
            <div style="font-size:12px; color:#aaa;">✅ OB55 New Version</div>
            <div style="font-size:12px; color:#aaa;">✅ Simple And Easy Steps</div>
        </div>
    </div>
    
    <!-- COLORS -->
    <div class="card">
        <div class="colors-header">
            <h3><i class="fas fa-palette"></i> Colors</h3>
        </div>
        <div class="colors-ribbon" id="colorRibbon"></div>
    </div>


    <!-- BIO EDITOR -->
    <div class="card">
        <h3><i class="fas fa-pen-nib"></i> Bio Editor</h3>
        <textarea id="bio" placeholder="Write your awesome bio here..."></textarea>
        <div id="charCount" style="text-align:right; font-size:12px; margin-top:5px; color:#888;">0 / 350</div>
        <div class="preview" id="preview">Live Preview</div>
        
        <div class="formatting-section">
            <div class="formatting-title">Text Formatting</div>
            <button class="format-btn btn-bold" onclick="insertSimple('[b]')">Bold</button>
            <button class="format-btn btn-italic" onclick="insertSimple('[i]')">Italic</button>
            <button class="format-btn btn-curve" onclick="insertSimple('[c]')">Curve</button>
            <button class="format-btn btn-underline" onclick="insertSimple('[u]')">Underline</button>
            <button class="format-btn btn-strike" onclick="insertSimple('[s]')">Strike</button>


        </div>
    </div>

    <!-- SYMBOLS DASHBOARD -->
    <div class="card symbols-card">
        <div class="symbols-header">
            <div class="symbols-title">
                <h3><i class="fas fa-star"></i> Symbols</h3>
                <span class="symbols-subtitle">Tap the eye to show or hide symbols</span>
            </div>
            <button type="button" id="symbolsToggle" class="symbols-toggle" onclick="toggleSymbols()" aria-label="Show symbols" aria-expanded="false" title="Show symbols">
                <i id="symbolsEyeIcon" class="fas fa-eye-slash"></i>
            </button>
        </div>
        <div id="symbolsPanel" class="symbols-panel" hidden>
            <div class="symbols-container">

                <button class="symbol-btn" onclick="insertSimple('么')">么</button>
                <button class="symbol-btn" onclick="insertSimple('〆')">〆</button>
                <button class="symbol-btn" onclick="insertSimple('⸙')">⸙</button>
                <button class="symbol-btn" onclick="insertSimple('ᥫ᭡')">ᥫ᭡</button>
                <button class="symbol-btn" onclick="insertSimple('✓')">✓</button>
                <button class="symbol-btn" onclick="insertSimple('々')">々</button>
                <button class="symbol-btn" onclick="insertSimple('ཧོ')">ཧོ</button>
                <button class="symbol-btn" onclick="insertSimple('亗')">亗</button>
                <button class="symbol-btn" onclick="insertSimple('☠︎︎')">☠︎︎</button>
                <button class="symbol-btn" onclick="insertSimple('᭄')">᭄</button>
                <button class="symbol-btn" onclick="insertSimple('모')">모</button>
                <button class="symbol-btn" onclick="insertSimple('☯')">☯</button>
                <button class="symbol-btn" onclick="insertSimple('ꪇ༊')">ꪇ༊</button>
                <button class="symbol-btn" onclick="insertSimple('✿')">✿</button>
                <button class="symbol-btn" onclick="insertSimple('♡')">♡</button>
                <button class="symbol-btn" onclick="insertSimple('ᰔᩚ')">ᰔᩚ</button>
                <button class="symbol-btn" onclick="insertSimple('☆')">☆</button>
                <button class="symbol-btn" onclick="insertSimple('﷽')">﷽</button>
                <button class="symbol-btn" onclick="insertSimple('❖')">❖</button>
                <button class="symbol-btn" onclick="insertSimple('ꔪ')">ꔪ</button>
                <button class="symbol-btn" onclick="insertSimple('✤')">✤</button>
                <button class="symbol-btn" onclick="insertSimple('☆')">☆</button>
                <button class="symbol-btn" onclick="insertSimple('𓃮')">𓃮</button>
                <button class="symbol-btn" onclick="insertSimple('⛥')">⛥</button>
                <button class="symbol-btn" onclick="insertSimple('ᯓ ᡣ𐭩')">ᯓ ᡣ𐭩</button>
                <button class="symbol-btn" onclick="insertSimple('ᯤ')">ᯤ</button>
                <button class="symbol-btn" onclick="insertSimple('┇')">┇</button>
                <button class="symbol-btn" onclick="insertSimple('☪︎')">☪︎</button>
                <button class="symbol-btn" onclick="insertSimple('☘︎')">☘︎</button>
                <button class="symbol-btn" onclick="insertSimple('𑣲')">𑣲</button>
                <button class="symbol-btn" onclick="insertSimple('𐙚')">𐙚</button>
                <button class="symbol-btn" onclick="insertSimple('𖹭')">𖹭</button>
            
            </div>
        </div>
    </div>

    <!-- AUTHENTICATION DASHBOARD -->
    <div class="card auth-card">
        <div class="auth-top">
            <div class="auth-heading">
                <div class="auth-icon">🔐</div>
                <h3>Authentication</h3>
            </div>
            <a href="http://eat-to-access.gt.tc" target="_blank" class="get-token-btn">✨ GET TOKEN</a>
        </div>

        <div class="auth-tabs" role="tablist" aria-label="Authentication method">
            <button type="button" class="auth-tab active" data-method="access" onclick="setAuthMethod('access')">
                <i class="fas fa-unlock-alt"></i><span>Access</span>
            </button>
            <button type="button" class="auth-tab" data-method="uid" onclick="setAuthMethod('uid')">
                <i class="fas fa-user"></i><span>UID+PW</span>
            </button>
            <button type="button" class="auth-tab" data-method="jwt" onclick="setAuthMethod('jwt')">
                <i class="fas fa-key"></i><span>JWT</span>
            </button>
        </div>

        <input type="hidden" id="method" value="access">

        <label class="auth-label" for="serverSelect">REGION</label>
        <select id="serverSelect" class="auth-input region-select">
            <option value="IND">🇮🇳 IND - India</option>
            <option value="BD">🇧🇩 BD - Bangladesh</option>
            <option value="SG">🇸🇬 SG - Singapore</option>
            <option value="BR">🇧🇷 BR - Brazil</option>
            <option value="US">🇺🇸 US - USA</option>
            <option value="EU">🇪🇺 EU - Europe</option>
        </select>

        <label id="authLabel" class="auth-label" for="token">ACCESS TOKEN</label>
        <div class="auth-input-wrap">
            <input id="token" class="auth-input" placeholder="Format: 660b275a..." autocomplete="off">
            <input id="password" class="auth-input auth-password" placeholder="Enter Password" type="password" autocomplete="off" style="display:none;">
        </div>

        <button id="submitBtn" class="gradient-btn auth-submit" onclick="handleSubmit()">↪️ UPDATE BIO (ACCESS)</button>
    </div>

    <!-- HOW TO USE -->
    <a id="howToUseBtn" href="#" target="_blank" rel="noopener noreferrer" class="how-to-use-btn">
        <i class="fab fa-youtube"></i> HOW TO USE
    </a>

    <!-- SOCIAL MEDIA PILL BUTTONS -->
    <div class="social-footer">
        <a href="https://t.me/LuckyOfficialChannel" target="_blank" class="social-btn btn-tg">
            <i class="fab fa-telegram"></i> Telegram
        </a>
        <a href="https://www.instagram.com/lllux96" target="_blank" class="social-btn btn-ig">
            <i class="fab fa-instagram"></i> Instagram
        </a>
        <a href="https://youtube.com/@redluckyxyz" target="_blank" class="social-btn btn-yt">
            <i class="fab fa-youtube"></i> YouTube
        </a>
    </div>

</div>

<script>
// ===== WELCOME POPUP LOGIC =====
window.onload = function() {
    setTimeout(() => {
        document.getElementById('welcome-popup').classList.add('active');
    }, 800); 
};

function closePopup() {
    document.getElementById('welcome-popup').classList.remove('active');
}

// ===== SAKURA FLOWER ANIMATION LOGIC =====
function createSakura() {
    const sakura = document.createElement('div');
    sakura.classList.add('sakura');
    sakura.innerHTML = '🌸';
    sakura.style.left = Math.random() * 100 + 'vw';
    sakura.style.animationDuration = Math.random() * 4 + 5 + 's'; 
    sakura.style.fontSize = Math.random() * 10 + 12 + 'px';
    document.body.appendChild(sakura);
    
    setTimeout(() => { sakura.remove(); }, 9000);
}
setInterval(createSakura, 500);

// UTILITY FUNCTIONS
function closeResult() { document.getElementById('overlay').className = ""; }

function showResult(type, title, html, bio) {
    const ov = document.getElementById('overlay');
    ov.className = type + " active";
    document.getElementById('res-icon').className = type === 'success' ? "fas fa-check-circle res-icon" : "fas fa-times-circle res-icon";
    document.getElementById('res-title').innerText = title;
    const preview = document.getElementById('preview').cloneNode(true);
    preview.removeAttribute('id'); preview.className = 'result-preview';
    preview.querySelectorAll('*').forEach(el => { el.removeAttribute('onclick'); el.removeAttribute('tabindex'); });
    document.getElementById('res-body').innerHTML = html + '<div class="result-preview-label">LIVE PREVIEW</div>';
    document.getElementById('res-body').appendChild(preview);
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

function insertColor(color) { insertSimple('[' + color + ']'); }

function setAuthMethod(method) {
    const methodField = document.getElementById("method");
    const tokenField = document.getElementById("token");
    const pwdField = document.getElementById("password");
    const label = document.getElementById("authLabel");
    const submitBtn = document.getElementById("submitBtn");

    methodField.value = method;
    document.querySelectorAll(".auth-tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.method === method);
    });

    if (method === "access") {
        label.textContent = "ACCESS TOKEN";
        tokenField.placeholder = "Format: 660b275a...";
        pwdField.style.display = "none";
        submitBtn.textContent = "↪️ UPDATE BIO (ACCESS)";
    } else if (method === "uid") {
        label.textContent = "UID + PASSWORD";
        tokenField.placeholder = "Enter UID";
        pwdField.placeholder = "Enter Password";
        pwdField.style.display = "block";
        submitBtn.textContent = "↪️ UPDATE BIO (UID+PW)";
    } else {
        label.textContent = "JWT TOKEN";
        tokenField.placeholder = "Format: eyJhbGci...";
        pwdField.style.display = "none";
        submitBtn.textContent = "↪️ UPDATE BIO (JWT)";
    }
}

function togglePassword() {
    setAuthMethod(document.getElementById("method").value || "access");
}

let lastValidBio = "";
function updatePreview() {
    let bio = document.getElementById("bio");
    if (bio.value.length > 350) { bio.value = lastValidBio; return; }
    lastValidBio = bio.value;
    document.getElementById("charCount").innerText = bio.value.length + " / 350";
    let raw = bio.value;
    let text = raw.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
    let result = ''; let i = 0; let currentColor = null;
    let currentBold = false, currentItalic = false, currentCurve = false, currentUnderline = false, currentStrike = false;
    
    function applyCurrent() {
        let style = '';
        if (currentColor) style += `color:#${currentColor};`;
        if (currentBold) style += `font-weight:bold;`;
        if (currentItalic || currentCurve) style += `font-style:italic;`;
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
            if (endIdx === -1) { buffer += text[i]; i++; continue; }
            let tag = text.substring(i+1, endIdx);
            i = endIdx + 1;
            if (/^[0-9A-Fa-f]{6}$/.test(tag)) { currentColor = tag; }
            else if (tag === 'b') { currentBold = !currentBold; }
            else if (tag === 'i') { currentItalic = !currentItalic; }
            else if (tag === 'c') { currentCurve = !currentCurve; }
            else if (tag === 'u') { currentUnderline = !currentUnderline; }
            else if (tag === 's') { currentStrike = !currentStrike; }
            else { buffer += '[' + tag + ']'; }
        } else { buffer += text[i]; i++; }
    }
    if (buffer) {
        let open = applyCurrent();
        result += open + buffer + (open ? '</span>' : '');
    }
    document.getElementById("preview").innerHTML = result || "Live Preview";
}

// SYMBOLS SHOW / HIDE TOGGLE
function toggleSymbols() {
    const panel = document.getElementById("symbolsPanel");
    const button = document.getElementById("symbolsToggle");
    const icon = document.getElementById("symbolsEyeIcon");
    const isHidden = panel.hasAttribute("hidden");

    if (isHidden) {
        panel.removeAttribute("hidden");
        button.classList.add("active");
        icon.className = "fas fa-eye";
        button.setAttribute("aria-expanded", "true");
        button.setAttribute("aria-label", "Hide symbols");
        button.setAttribute("title", "Hide symbols");
    } else {
        panel.setAttribute("hidden", "");
        button.classList.remove("active");
        icon.className = "fas fa-eye-slash";
        button.setAttribute("aria-expanded", "false");
        button.setAttribute("aria-label", "Show symbols");
        button.setAttribute("title", "Show symbols");
    }
}

// COLORS RIBBON
const colors = ["#FF0000","#DC143C","#FF7F50","#FF8C00","#FFD700","#FFFF00","#32CD32","#00FF00","#00FA9A","#00FFFF","#00BFFF","#1E90FF","#4682B4","#0000FF","#8A2BE2","#9370DB","#FF00FF","#FF1493","#FF69B4","#FFFFFF","#C0C0C0"];
const ribbon = document.getElementById("colorRibbon");
colors.forEach(col => {
    let dot = document.createElement("div");
    dot.className = "c-dot";
    dot.style.backgroundColor = col;
    dot.onclick = () => insertColor(col.substring(1));
    ribbon.appendChild(dot);
});

document.getElementById("bio").addEventListener("input", updatePreview);
updatePreview();
setAuthMethod("access");

// Put your YouTube tutorial URL here later.
const HOW_TO_USE_URL = "#";
document.getElementById("howToUseBtn").href = HOW_TO_USE_URL;

// MAIN SUBMIT HANDLER
async function handleSubmit() {
    const method = document.getElementById("method").value;
    const server = document.getElementById("serverSelect").value;
    const token = document.getElementById("token").value.trim();
    const bio = document.getElementById("bio").value.trim();
    const password = document.getElementById("password").value.trim();
    const btn = document.getElementById("submitBtn");

    if (!bio) { alert("Bio is required!"); return; }
    if (bio.length < 3) { alert("Bio too short! Minimum 3 characters."); return; }
    if (!token) {
        alert(method === "uid" ? "UID is required!" :
              method === "access" ? "Access Token is required!" :
              "JWT Token is required!");
        return;
    }
    if (method === "uid" && !password) {
        alert("Password is required!");
        return;
    }

    const body = { method, bio, token, server };
    if (method === "uid") body.password = password;

    const original = btn.innerHTML;
    btn.innerHTML = "⏳ Processing...";
    btn.disabled = true;

    try {
        const res = await fetch("/api/update", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body)
        });

        let data;
        try { data = await res.json(); }
        catch (_) { throw new Error("Invalid response received from server."); }

        if (res.ok && data.status === "success") {
            showResult("success", "BIO ADD SUCCESSFULLY", `
                <div style="margin:5px 0;"><strong>🆔 UID:</strong> ${data.uid || data.user_id || "N/A"}</div>
                <div style="margin:5px 0;"><strong>👤 Name:</strong> ${data.name || "N/A"}</div>
                <div style="margin-top:10px; color:#00ffc3;">✅ ${data.message || "Bio updated successfully"}</div>
            `, bio);
            document.getElementById("token").value = "";
            document.getElementById("password").value = "";
            document.getElementById("bio").value = "";
            lastValidBio = "";
            updatePreview();
        } else {
            showResult("error", "BIO FAILED", `<div class="result-status" style="color:#ff6675;">${data.message || data.error || "Bio update failed."}</div>`, bio);
        }
    } catch (e) {
        showResult("error", "BIO FAILED", `<div class="result-status" style="color:#ff6675;">${e.message || "Request failed."}</div>`, bio);
    } finally {
        btn.innerHTML = original;
        btn.disabled = false;
    }
}

</script>
</body>
</html>
"""

# ===== API CONFIGURATION =====
ACCESS_API_URL = "https://star-bio-api.lovable.app/api/public/bio-upload"
JWT_API_URL = "https://star-bio-api.lovable.app/api/public/bio-upload"
UID_API_URL = "https://star-bio-api.lovable.app/api/public/bio-upload"


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/update', methods=['POST'])
def update_bio():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"status": "error", "message": "Missing JSON body"}), 400

        method = str(data.get("method", "jwt")).strip().lower()
        bio = str(data.get("bio", "")).strip()
        server = str(data.get("server", "IND")).strip().upper()
        token = str(data.get("token", "")).strip()
        password = str(data.get("password", "")).strip()

        if not bio:
            return jsonify({"status": "error", "message": "Bio is required"}), 400
        if len(bio) < 3:
            return jsonify({"status": "error", "message": "Bio too short. Minimum 3 characters."}), 400
        if method not in ("jwt", "access", "uid"):
            return jsonify({"status": "error", "message": "Unsupported authentication method."}), 400

        if method == "access":
            if not token:
                return jsonify({"status": "error", "message": "Access Token is required"}), 400
            api_url = ACCESS_API_URL
            params = {"bio": bio, "access": token}

        elif method == "jwt":
            if not token:
                return jsonify({"status": "error", "message": "JWT Token is required"}), 400
            api_url = JWT_API_URL
            params = {"bio": bio, "jwt": token}

        else:
            if not token:
                return jsonify({"status": "error", "message": "UID is required"}), 400
            if not password:
                return jsonify({"status": "error", "message": "Password is required"}), 400
            api_url = UID_API_URL
            # Exact format supplied in api.txt:
            # ?bio={uid}&uid={uid}&password={password}
            params = {"bio": token, "uid": token, "password": password}

        response = requests.get(
            api_url,
            params=params,
            timeout=30,
            headers={
                "Accept": "application/json",
                "User-Agent": "Lucky-X-Long-Bio/1.0"
            }
        )

        try:
            api_data = response.json()
        except ValueError:
            api_data = {"message": response.text.strip()}

        if not response.ok:
            return jsonify({
                "status": "error",
                "message": (
                    api_data.get("message")
                    or api_data.get("error")
                    or api_data.get("status")
                    or f"External API returned HTTP {response.status_code}"
                ),
                "http_code": response.status_code
            }), 502

        success_value = api_data.get("success")
        status_value = str(api_data.get("status", "")).lower()

        if success_value is False or status_value in ("error", "failed", "failure", "false"):
            return jsonify({
                "status": "error",
                "message": (
                    api_data.get("message")
                    or api_data.get("error")
                    or api_data.get("status")
                    or "API returned failure"
                ),
                "server_response": api_data
            })

        return jsonify({
            "status": "success",
            "message": (
                api_data.get("message")
                or api_data.get("status")
                or "Bio updated successfully"
            ),
            "uid": api_data.get("uid") or api_data.get("user_id"),
            "name": api_data.get("name"),
            "region_used": server,
            "server_response": api_data
        })

    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "External API request timed out."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"API request failed: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
