#!/usr/bin/env python3
"""
===============================================================================
 AETHER-4D // RIEMANNIAN STEREOGRAPHIC MANIFOLD & HELMHOLTZ EIGENMODE STUDIO
===============================================================================
 Run in VS Code WSL Ubuntu Terminal:
     python3 aether_manifold.py
===============================================================================
"""

import http.server
import json
import os
import socket
import subprocess
import sys
import threading
import time
from urllib.parse import urlparse

# ANSI Terminal Colors for Live VS Code Ubuntu Terminal Telemetry
BLUE = "\033[94m"
VERMILION = "\033[91m"
GOLD = "\033[93m"
TEAL = "\033[96m"
GREEN = "\033[92m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

HTML_PAYLOAD = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AETHER-4D // Riemannian Stereographic Manifold & Helmholtz Eigenmode Studio</title>
  <style>
    :root {
      --bg-studio: #f3f1ec;
      --card-glass: rgba(255, 255, 255, 0.78);
      --card-border: rgba(20, 24, 33, 0.11);
      --ink: #12151c;
      --ink-muted: #5c6474;
      --klein: #0038ff;
      --vermilion: #ff441f;
      --gold: #c88a14;
      --teal: #0b7a68;
      --surface-pill: rgba(18, 21, 28, 0.055);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    body {
      background: var(--bg-studio);
      color: var(--ink);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      overflow: hidden;
      width: 100vw;
      height: 100vh;
    }

    #canvas-container {
      position: fixed;
      inset: 0;
      z-index: 1;
    }

    /* Subtle Swiss Architectural Drafting Grid Overlay */
    .drafting-grid {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 2;
      background-image:
        linear-gradient(to right, rgba(18, 21, 28, 0.035) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(18, 21, 28, 0.035) 1px, transparent 1px);
      background-size: 56px 56px;
      mask-image: radial-gradient(circle at center, rgba(0,0,0,0.65) 15%, transparent 80%);
    }

    /* Daylight Frosted Acrylic Studio Card */
    .studio-card {
      background: var(--card-glass);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      backdrop-filter: blur(20px) saturate(140%);
      box-shadow:
        0 14px 36px rgba(18, 22, 32, 0.08),
        0 2px 6px rgba(18, 22, 32, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }

    /* ==================== TOP-LEFT SWISS LAB MASTHEAD ==================== */
    .top-left-masthead {
      position: fixed;
      top: 16px;
      left: 16px;
      width: 440px;
      z-index: 10;
      padding: 14px 18px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: opacity 0.3s ease;
    }

    .brand-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .brand-left {
      display: flex;
      align-items: center;
      gap: 11px;
    }

    .swiss-badge {
      width: 34px;
      height: 34px;
      border-radius: 10px;
      background: var(--klein);
      color: #fff;
      font-weight: 900;
      font-size: 13px;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 6px 16px rgba(0, 56, 255, 0.32);
    }

    .lab-title {
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 1.4px;
      text-transform: uppercase;
      color: var(--ink);
    }

    .lab-sub {
      font-size: 10px;
      font-weight: 600;
      letter-spacing: 1.1px;
      color: var(--vermilion);
      text-transform: uppercase;
    }

    .live-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(11, 122, 104, 0.10);
      border: 1px solid rgba(11, 122, 104, 0.28);
      color: var(--teal);
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.8px;
    }

    .live-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--teal);
      animation: blink 1.4s infinite;
    }

    @keyframes blink {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.3); }
    }

    .equation-strip {
      background: rgba(255, 255, 255, 0.75);
      border: 1px solid rgba(18, 21, 28, 0.08);
      border-radius: 11px;
      padding: 8px 12px;
      font-family: 'Cambria Math', 'Times New Roman', serif;
      font-size: 15px;
      color: var(--ink);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .equation-strip .kb { color: var(--klein); font-weight: 700; }
    .equation-strip .vm { color: var(--vermilion); font-weight: 700; }
    .equation-strip .gd { color: var(--gold); font-weight: 700; }

    /* Telemetry Mini Strip */
    .telemetry-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 7px;
    }

    .t-cell {
      background: var(--surface-pill);
      border-radius: 9px;
      padding: 6px 8px;
    }

    .t-lbl {
      font-size: 9px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.7px;
      color: var(--ink-muted);
    }

    .t-num {
      font-family: 'Consolas', 'SF Mono', monospace;
      font-size: 12.5px;
      font-weight: 800;
      color: var(--ink);
      margin-top: 2px;
    }

    /* ==================== TOP-RIGHT STUDIO GALLERY & MODE DECK ==================== */
    .top-right-deck {
      position: fixed;
      top: 16px;
      right: 16px;
      width: 340px;
      z-index: 10;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: opacity 0.3s ease;
    }

    .deck-hdr {
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1.6px;
      color: var(--ink-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .mode-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 7px;
    }

    .studio-btn {
      background: rgba(255, 255, 255, 0.75);
      border: 1px solid rgba(18, 21, 28, 0.12);
      color: var(--ink);
      padding: 9px 10px;
      border-radius: 11px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.16s ease;
      text-align: left;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
    }

    .studio-btn:hover {
      border-color: var(--klein);
      transform: translateY(-1px);
      background: #fff;
    }

    .studio-btn.active {
      background: var(--klein);
      border-color: var(--klein);
      color: #fff;
      box-shadow: 0 6px 16px rgba(0, 56, 255, 0.28);
    }

    .finish-row {
      display: flex;
      gap: 6px;
    }

    .finish-row .studio-btn {
      flex: 1;
      justify-content: center;
      padding: 7px 6px;
      font-size: 10.5px;
    }

    /* ==================== BOTTOM-LEFT CHLADNI EIGENMODE ANALYZER ==================== */
    .bottom-left-analyzer {
      position: fixed;
      bottom: 16px;
      left: 16px;
      width: 305px;
      z-index: 10;
      padding: 13px 15px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: opacity 0.3s ease;
    }

    .chladni-frame {
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(18, 21, 28, 0.14);
      background: #faf9f5;
    }

    .chladni-tag {
      position: absolute;
      top: 6px;
      left: 8px;
      background: rgba(255, 255, 255, 0.88);
      border: 1px solid rgba(18, 21, 28, 0.12);
      padding: 2px 7px;
      border-radius: 6px;
      font-family: 'Consolas', monospace;
      font-size: 9.5px;
      font-weight: 700;
      color: var(--ink);
      pointer-events: none;
    }

    #chladniCanvas {
      display: block;
      width: 100%;
      height: 175px;
      cursor: pointer;
    }

    .chladni-sub {
      font-size: 10px;
      color: var(--ink-muted);
      text-align: center;
      font-weight: 500;
    }

    /* ==================== BOTTOM-RIGHT PRECISION PARAMETER CONSOLE ==================== */
    .bottom-right-console {
      position: fixed;
      bottom: 16px;
      right: 16px;
      width: 340px;
      z-index: 10;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 9px;
      transition: opacity 0.3s ease;
    }

    /* Quantum / Harmonic Number Steppers */
    .quantum-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 7px;
      margin-bottom: 2px;
    }

    .q-box {
      background: var(--surface-pill);
      border-radius: 10px;
      padding: 6px 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }

    .q-title {
      font-size: 9.5px;
      font-weight: 800;
      color: var(--ink-muted);
      text-transform: uppercase;
    }

    .q-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .q-step {
      width: 22px;
      height: 22px;
      border-radius: 6px;
      border: 1px solid rgba(18, 21, 28, 0.15);
      background: #fff;
      color: var(--ink);
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .q-step:hover {
      background: var(--klein);
      color: #fff;
      border-color: var(--klein);
    }

    .q-val {
      font-family: 'Consolas', monospace;
      font-size: 14px;
      font-weight: 800;
      color: var(--klein);
    }

    /* Sliders */
    .slider-item {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .slider-hdr {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 600;
      color: var(--ink);
    }

    .slider-readout {
      font-family: 'Consolas', monospace;
      font-weight: 800;
      color: var(--vermilion);
    }

    input[type="range"] {
      -webkit-appearance: none;
      appearance: none;
      width: 100%;
      height: 5px;
      background: rgba(18, 21, 28, 0.14);
      border-radius: 99px;
      outline: none;
    }

    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 15px;
      height: 15px;
      border-radius: 50%;
      background: var(--klein);
      border: 2.5px solid #fff;
      box-shadow: 0 2px 8px rgba(0, 56, 255, 0.4);
      cursor: pointer;
    }

    /* ==================== BOTTOM-CENTER TURNTABLE & 4D TRANSPORT BAR ==================== */
    .center-transport {
      position: fixed;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 10;
      padding: 8px 14px;
      display: flex;
      align-items: center;
      gap: 7px;
      border-radius: 999px;
      transition: opacity 0.3s ease;
    }

    .pill-btn {
      background: rgba(255, 255, 255, 0.85);
      border: 1px solid rgba(18, 21, 28, 0.14);
      color: var(--ink);
      padding: 7px 13px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .pill-btn:hover {
      border-color: var(--klein);
      transform: translateY(-2px);
      background: #fff;
    }

    .pill-btn.active {
      background: var(--ink);
      border-color: var(--ink);
      color: #fff;
    }

    .pill-btn.accent-vermilion {
      background: var(--vermilion);
      border-color: var(--vermilion);
      color: #fff;
      box-shadow: 0 5px 14px rgba(255, 68, 31, 0.32);
    }

    .pill-btn.accent-vermilion:hover {
      background: #e03512;
    }

    .divider-v {
      width: 1px;
      height: 20px;
      background: rgba(18, 21, 28, 0.14);
      margin: 0 2px;
    }

    .ui-hidden .top-left-masthead,
    .ui-hidden .top-right-deck,
    .ui-hidden .bottom-left-analyzer,
    .ui-hidden .bottom-right-console,
    .ui-hidden .center-transport {
      opacity: 0;
      pointer-events: none;
    }

    @media (max-width: 1180px) {
      .bottom-left-analyzer { display: none; }
      .top-left-masthead { width: 350px; }
    }
  </style>

  <script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
      }
    }
  </script>
</head>
<body>

  <div id="canvas-container"></div>
  <div class="drafting-grid"></div>

  <!-- ==================== TOP-LEFT SWISS LAB MASTHEAD ==================== -->
  <div class="top-left-masthead studio-card">
    <div class="brand-row">
      <div class="brand-left">
        <div class="swiss-badge">4D</div>
        <div>
          <div class="lab-title">AETHER-4D // Riemannian &amp; Eigenmode Lab</div>
          <div class="lab-sub" id="labSubtitle">STEREOGRAPHIC S³ → R³ PROJECTION &amp; HELMHOLTZ HARMONICS</div>
        </div>
      </div>
      <span class="live-pill"><span class="live-dot"></span>PBR STUDIO</span>
    </div>

    <div class="equation-strip">
      <span>
        <b>P</b>(x) = <span class="kb">x<sub>1..3</sub></span> / (1 − <span class="vm">x₄</span>) , &nbsp;
        ∇²<span class="kb">Ψ</span> + <span class="gd">k<sub>n,ℓ</sub>²</span><span class="kb">Ψ</span> = 0
      </span>
      <span style="font-size:11px;font-family:Consolas,monospace;color:var(--ink-muted);" id="so4Readout">SO(4) ψ=0.00</span>
    </div>

    <div class="telemetry-strip">
      <div class="t-cell">
        <div class="t-lbl">Eigenfreq f</div>
        <div class="t-num" id="valFreq" style="color:var(--klein);">1,428 Hz</div>
      </div>
      <div class="t-cell">
        <div class="t-lbl">Euler χ(M)</div>
        <div class="t-num" id="valEuler" style="color:var(--vermilion);">χ = 0 (T²)</div>
      </div>
      <div class="t-cell">
        <div class="t-lbl">4D Curvature</div>
        <div class="t-num" id="valCurvature" style="color:var(--gold);">+1.84 κ</div>
      </div>
      <div class="t-cell">
        <div class="t-lbl">Resonators</div>
        <div class="t-num" id="valInstances">4,800 GPU</div>
      </div>
    </div>
  </div>

  <!-- ==================== TOP-RIGHT STUDIO GALLERY & MODE DECK ==================== -->
  <div class="top-right-deck studio-card">
    <div class="deck-hdr">
      <span>1. Mathematical Manifold Engine</span>
      <span style="color:var(--klein);">4 GEOMETRIES</span>
    </div>
    <div class="mode-grid">
      <button class="studio-btn active" data-mode="hopf">🌀 4D Hopf Fibration</button>
      <button class="studio-btn" data-mode="helmholtz">🔊 3D Bessel Levitation</button>
      <button class="studio-btn" data-mode="calabi">🎻 Calabi–Yau String</button>
      <button class="studio-btn" data-mode="chladni">💠 Chladni Tensor Shell</button>
    </div>

    <div class="deck-hdr" style="margin-top:4px;">
      <span>2. Daylight Studio Finish</span>
    </div>
    <div class="finish-row">
      <button class="studio-btn active" data-theme="bauhaus">🎨 Bauhaus Klein</button>
      <button class="studio-btn" data-theme="kyoto">🌿 Jade &amp; Terra</button>
      <button class="studio-btn" data-theme="platinum">💎 Platinum Pearl</button>
    </div>
  </div>

  <!-- ==================== BOTTOM-LEFT CHLADNI EIGENMODE ANALYZER ==================== -->
  <div class="bottom-left-analyzer studio-card">
    <div class="deck-hdr">
      <span>2D Chladni Biharmonic Plate</span>
      <span id="chladniModeTag" style="color:var(--vermilion);font-family:Consolas,monospace;">(ℓ=3, m=2, n=2)</span>
    </div>
    <div class="chladni-frame">
      <div class="chladni-tag">NODAL CONTOUR Ψ(x,y) = 0</div>
      <canvas id="chladniCanvas" width="220" height="175"></canvas>
    </div>
    <div class="chladni-sub">Click plate to excite higher harmonic eigenmode</div>
  </div>

  <!-- ==================== BOTTOM-RIGHT PRECISION PARAMETER CONSOLE ==================== -->
  <div class="bottom-right-console studio-card">
    <div class="deck-hdr">
      <span>Quantum &amp; Harmonic Indices (ℓ, m, n)</span>
    </div>

    <div class="quantum-row">
      <div class="q-box">
        <span class="q-title">Degree (ℓ)</span>
        <div class="q-controls">
          <button class="q-step" id="btnLDec">−</button>
          <span class="q-val" id="valL">3</span>
          <button class="q-step" id="btnLInc">+</button>
        </div>
      </div>
      <div class="q-box">
        <span class="q-title">Order (m)</span>
        <div class="q-controls">
          <button class="q-step" id="btnMDec">−</button>
          <span class="q-val" id="valM">2</span>
          <button class="q-step" id="btnMInc">+</button>
        </div>
      </div>
      <div class="q-box">
        <span class="q-title">Radial (n)</span>
        <div class="q-controls">
          <button class="q-step" id="btnNDec">−</button>
          <span class="q-val" id="valN">2</span>
          <button class="q-step" id="btnNInc">+</button>
        </div>
      </div>
    </div>

    <div class="slider-item">
      <div class="slider-hdr">
        <span>4D Clifford Inside-Out Velocity (Ω_4D)</span>
        <span class="slider-readout" id="lblSpeed4D">0.85 rad/s</span>
      </div>
      <input type="range" id="slSpeed4D" min="0" max="3.0" step="0.05" value="0.85" />
    </div>

    <div class="slider-item">
      <div class="slider-hdr">
        <span>3D Turntable Spin Speed (Ω_3D)</span>
        <span class="slider-readout" id="lblSpeed3D">0.65 rad/s</span>
      </div>
      <input type="range" id="slSpeed3D" min="0" max="3.5" step="0.05" value="0.65" />
    </div>

    <div class="slider-item">
      <div class="slider-hdr">
        <span>4D Stereographic Pole Depth (η)</span>
        <span class="slider-readout" id="lblPole">0.68</span>
      </div>
      <input type="range" id="slPole" min="0.15" max="0.88" step="0.01" value="0.68" />
    </div>

    <div class="slider-item">
      <div class="slider-hdr">
        <span>Harmonic Wave Modulation</span>
        <span class="slider-readout" id="lblWaveAmp">1.15x</span>
      </div>
      <input type="range" id="slWaveAmp" min="0.0" max="2.5" step="0.05" value="1.15" />
    </div>

    <div class="slider-item">
      <div class="slider-hdr">
        <span>Exploded Architectural View</span>
        <span class="slider-readout" id="lblExplode">0.00</span>
      </div>
      <input type="range" id="slExplode" min="0.0" max="1.5" step="0.02" value="0.00" />
    </div>
  </div>

  <!-- ==================== BOTTOM-CENTER TURNTABLE & 4D TRANSPORT BAR ==================== -->
  <div class="center-transport studio-card">
    <button class="pill-btn active" id="btnSpin3D">⏸ 3D Spin</button>
    <button class="pill-btn" id="btnReverse3D">⇄ Reverse</button>
    <button class="pill-btn active" id="btnSpin4D">🔄 4D Inside-Out</button>
    <button class="pill-btn" id="btnGimbal">🧭 3-Axis Gimbal</button>

    <div class="divider-v"></div>

    <button class="pill-btn accent-vermilion" id="btnResonancePulse">⚡ Harmonic Pulse</button>
    <button class="pill-btn active" id="btnToggleRibbons">🎗️ Tori Ribbons</button>
    <button class="pill-btn active" id="btnToggleDipoles">🔹 4,800 Resonators</button>

    <div class="divider-v"></div>

    <button class="pill-btn" id="camStudio">Studio</button>
    <button class="pill-btn" id="camZenith">Zenith</button>
    <button class="pill-btn" id="camCinema" title="Shortcut: H">👁️ Clean View</button>
  </div>

  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
    import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

    // =========================================================================
    // 1. DAYLIGHT PBR STUDIO SCENE, SOFT SHADOWS & PROCEDURAL HDRI ENVIRONMENT
    // =========================================================================
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf3f1ec);
    scene.fog = new THREE.Fog(0xf3f1ec, 16, 42);

    const camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 150);
    camera.position.set(0, 3.2, 11.8);

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.08;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Generate Studio Softbox Reflection Environment for PBR Clearcoat & Metals
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 28;
    controls.minDistance = 3.0;
    controls.target.set(0, 0.2, 0);

    // Overhead Museum Softbox Key Light with High-Res Soft Shadow Map
    const dirLight = new THREE.DirectionalLight(0xfffdf8, 2.4);
    dirLight.position.set(6, 14, 8);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 2;
    dirLight.shadow.camera.far = 28;
    const d = 6.5;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    dirLight.shadow.bias = -0.0005;
    scene.add(dirLight);

    const fillLight = new THREE.DirectionalLight(0xdbeafe, 1.1);
    fillLight.position.set(-8, 5, -6);
    scene.add(fillLight);

    // Architectural Cyclorama Shadow-Catching Floor + Precision Turntable Dial
    const floorGroup = new THREE.Group();
    floorGroup.position.y = -3.65;

    const shadowPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(60, 60).rotateX(-Math.PI / 2),
      new THREE.ShadowMaterial({ opacity: 0.16 })
    );
    shadowPlane.receiveShadow = true;
    floorGroup.add(shadowPlane);

    // Brushed Aluminum & Vermilion Turntable Rings on the Gallery Floor
    const dialRing1 = new THREE.Mesh(
      new THREE.RingGeometry(3.5, 3.55, 128).rotateX(-Math.PI / 2),
      new THREE.MeshBasicMaterial({ color: 0x12151c, transparent: true, opacity: 0.22, side: THREE.DoubleSide })
    );
    const dialRing2 = new THREE.Mesh(
      new THREE.RingGeometry(4.6, 4.63, 128).rotateX(-Math.PI / 2),
      new THREE.MeshBasicMaterial({ color: 0xff441f, transparent: true, opacity: 0.35, side: THREE.DoubleSide })
    );
    floorGroup.add(dialRing1, dialRing2);
    scene.add(floorGroup);

    // =========================================================================
    // 2. SIMULATION STATE, STUDIO THEMES & WSL TELEMETRY BRIDGE
    // =========================================================================
    const state = {
      mode: 'hopf',        // 'hopf', 'helmholtz', 'calabi', 'chladni'
      theme: 'bauhaus',    // 'bauhaus', 'kyoto', 'platinum'
      spin3D: true,
      spinDir: 1,
      spin4D: true,
      gimbal: false,
      showRibbons: true,
      showDipoles: true,
      speed3D: 0.65,
      speed4D: 0.85,
      poleDepth: 0.68,
      waveAmp: 1.15,
      explode: 0.0,
      L: 3,
      M: 2,
      N: 2,
      phase4D: 0.0,
      pulseBoost: 0.0
    };

    const THEMES = {
      bauhaus: {
        bg: 0xf3f1ec,
        primary: 0x0038ff,    // International Klein Blue
        secondary: 0xff441f,  // Braun Vermilion Orange
        tertiary: 0xd99b26,   // Brushed Champagne Gold
        ceramic: 0xffffff     // Glazed White Porcelain
      },
      kyoto: {
        bg: 0xf5f0e6,
        primary: 0x0b7a5c,    // Imperial Botanical Jade
        secondary: 0xd94e34,  // Kyoto Terracotta
        tertiary: 0xb8860b,   // Burnished Bronze
        ceramic: 0xfcfaf2     // Warm Ivory Ceramic
      },
      platinum: {
        bg: 0xedf1f7,
        primary: 0x1d4ed8,    // Sapphire Cobalt
        secondary: 0x7c3aed,  // Amethyst Quartz
        tertiary: 0x0ea5e9,   // Glacier Cyan
        ceramic: 0xf8fafc     // Swiss Alabaster
      }
    };

    let teleTimer = null;
    function sendTelemetryToWSL(eventLabel = "STATE_UPDATE") {
      if (teleTimer) clearTimeout(teleTimer);
      teleTimer = setTimeout(() => {
        const freq = Math.round(240 * Math.sqrt(state.L * (state.L + 1) + state.N * state.N * 2.4 + state.M * 1.5));
        fetch('/api/telemetry', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            event: eventLabel,
            mode: state.mode,
            theme: state.theme,
            L: state.L,
            M: state.M,
            N: state.N,
            freq,
            pole: state.poleDepth
          })
        }).catch(() => {});
      }, 100);
    }

    // =========================================================================
    // 3. MATHEMATICAL KERNELS (SPHERICAL HARMONICS, BESSEL & 4D HOPF FIBRATION)
    // =========================================================================
    // Associated Legendre Polynomial Evaluation P_l^m(x)
    function assocLegendre(l, m, x) {
      const absM = Math.min(l, Math.abs(m));
      let pmm = 1.0;
      if (absM > 0) {
        const somx2 = Math.sqrt(Math.max(0, (1.0 - x) * (1.0 + x)));
        let fact = 1.0;
        for (let i = 1; i <= absM; i++) {
          pmm *= -fact * somx2;
          fact += 2.0;
        }
      }
      if (l === absM) return pmm;
      let pmmp1 = x * (2.0 * absM + 1.0) * pmm;
      if (l === absM + 1) return pmmp1;
      let pll = 0.0;
      for (let ll = absM + 2; ll <= l; ll++) {
        pll = ((2.0 * ll - 1.0) * x * pmmp1 - (ll + absM - 1.0) * pmm) / (ll - absM);
        pmm = pmmp1;
        pmmp1 = pll;
      }
      return pll;
    }

    // Spherical Bessel Function j_l(x)
    function sphericalBessel(l, x) {
      const ax = Math.max(1e-4, Math.abs(x));
      if (l === 0) return Math.sin(ax) / ax;
      if (l === 1) return Math.sin(ax) / (ax * ax) - Math.cos(ax) / ax;
      let j0 = Math.sin(ax) / ax;
      let j1 = Math.sin(ax) / (ax * ax) - Math.cos(ax) / ax;
      let jl = j1;
      for (let k = 2; k <= l; k++) {
        jl = ((2 * k - 1) / ax) * j1 - j0;
        j0 = j1;
        j1 = jl;
      }
      return jl;
    }

    // 4D S^3 -> R^3 Stereographic Projection with SO(4) Clifford Isoclinic Rotation
    function project4DPoint(x1, x2, x3, x4, psi4D, etaPole) {
      // Rotate in (x1, x4) and (x2, x3) planes (Clifford double rotation in SO(4))
      const c1 = Math.cos(psi4D);
      const s1 = Math.sin(psi4D);
      const c2 = Math.cos(psi4D * 0.5);
      const s2 = Math.sin(psi4D * 0.5);

      const rx1 = x1 * c1 - x4 * s1;
      const rx4 = x1 * s1 + x4 * c1;
      const rx2 = x2 * c2 - x3 * s2;
      const rx3 = x2 * s2 + x3 * c2;

      const denom = Math.max(0.12, 1.0 - etaPole * rx4);
      const scale = 1.45 / denom;
      return new THREE.Vector3(rx1 * scale, rx2 * scale, rx3 * scale);
    }

    // =========================================================================
    // 4. DUAL-LAYER 3D GEOMETRY ENGINE (4,800 GPU INSTANCES + 32 4D TORI RIBBONS)
    // =========================================================================
    const sculptureGroup = new THREE.Group();
    scene.add(sculptureGroup);

    // Layer A: 4,800 GPU-Instanced Precision Tensor Resonators
    const INSTANCE_COUNT = 4800;
    const resonatorGeo = new THREE.CapsuleGeometry(0.036, 0.11, 6, 12);
    const resonatorMat = new THREE.MeshPhysicalMaterial({
      color: 0xffffff,
      roughness: 0.16,
      metalness: 0.15,
      clearcoat: 1.0,
      clearcoatRoughness: 0.08
    });

    const instancedResonators = new THREE.InstancedMesh(resonatorGeo, resonatorMat, INSTANCE_COUNT);
    instancedResonators.castShadow = true;
    instancedResonators.receiveShadow = true;
    sculptureGroup.add(instancedResonators);

    // Precompute Fibonacci Sphere / 4D Lattice Seeds for all 4,800 Resonators
    const seeds = [];
    const goldenRatio = (1 + Math.sqrt(5)) / 2;
    for (let i = 0; i < INSTANCE_COUNT; i++) {
      const frac = (i + 0.5) / INSTANCE_COUNT;
      const theta = Math.acos(1 - 2 * frac);
      const phi = (2 * Math.PI * i) / goldenRatio;
      const shell = (i % 6) / 5.0; // 6 concentric radial shells
      seeds.push({ theta, phi, shell, idx: i });
    }

    // Layer B: 32 Interlocking 4D Stereographic Ribbon Rings
    const NUM_RIBBONS = 32;
    const SEGMENTS_PER_RIBBON = 84;
    const ribbonMeshes = [];
    const ribbonMats = [
      new THREE.MeshPhysicalMaterial({ color: 0x0038ff, roughness: 0.18, metalness: 0.25, clearcoat: 1.0, side: THREE.DoubleSide }),
      new THREE.MeshPhysicalMaterial({ color: 0xff441f, roughness: 0.20, metalness: 0.15, clearcoat: 1.0, side: THREE.DoubleSide }),
      new THREE.MeshPhysicalMaterial({ color: 0xd99b26, roughness: 0.22, metalness: 0.82, clearcoat: 0.8, side: THREE.DoubleSide }),
      new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.15, metalness: 0.05, clearcoat: 1.0, side: THREE.DoubleSide })
    ];

    for (let r = 0; r < NUM_RIBBONS; r++) {
      const geom = new THREE.BufferGeometry();
      const positions = new Float32Array((SEGMENTS_PER_RIBBON + 1) * 2 * 3);
      const indices = [];
      for (let s = 0; s < SEGMENTS_PER_RIBBON; s++) {
        const i0 = s * 2;
        const i1 = i0 + 1;
        const i2 = i0 + 2;
        const i3 = i0 + 3;
        indices.push(i0, i1, i2, i1, i3, i2);
      }
      geom.setIndex(indices);
      geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));

      const mesh = new THREE.Mesh(geom, ribbonMats[r % 4]);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      sculptureGroup.add(mesh);
      ribbonMeshes.push(mesh);
    }

    function applyStudioTheme(themeName) {
      const t = THEMES[themeName];
      scene.background.setHex(t.bg);
      scene.fog.color.setHex(t.bg);
      document.body.style.background = `#${t.bg.toString(16).padStart(6, '0')}`;

      ribbonMats[0].color.setHex(t.primary);
      ribbonMats[1].color.setHex(t.secondary);
      ribbonMats[2].color.setHex(t.tertiary);
      ribbonMats[3].color.setHex(t.ceramic);
      updateInstanceColors();
    }

    const dummyObj = new THREE.Object3D();
    const tmpColor = new THREE.Color();
    const upVec = new THREE.Vector3(0, 1, 0);

    function updateInstanceColors() {
      const t = THEMES[state.theme];
      const cPrimary = new THREE.Color(t.primary);
      const cSecondary = new THREE.Color(t.secondary);
      const cTertiary = new THREE.Color(t.tertiary);
      const cCeramic = new THREE.Color(t.ceramic);

      for (let i = 0; i < INSTANCE_COUNT; i++) {
        const mod = i % 4;
        if (mod === 0) tmpColor.copy(cPrimary);
        else if (mod === 1) tmpColor.copy(cSecondary);
        else if (mod === 2) tmpColor.copy(cTertiary);
        else tmpColor.copy(cCeramic);
        instancedResonators.setColorAt(i, tmpColor);
      }
      instancedResonators.instanceColor.needsUpdate = true;
    }
    updateInstanceColors();

    // Update All 4,800 GPU Resonators & 32 4D Ribbon Tori Every Frame
    const pCurr = new THREE.Vector3();
    const pNext = new THREE.Vector3();
    const tangent = new THREE.Vector3();
    const binormal = new THREE.Vector3();

    function updateManifoldGeometry(elapsed) {
      const L = state.L;
      const M = Math.min(L, state.M);
      const N = state.N;
      const psi4D = state.phase4D;
      const eta = state.poleDepth;
      const waveAmp = state.waveAmp * (1.0 + state.pulseBoost);
      const explode = state.explode;

      // 1. Update 32 Parametric 4D / Eigenmode Ribbons
      for (let r = 0; r < NUM_RIBBONS; r++) {
        const mesh = ribbonMeshes[r];
        mesh.visible = state.showRibbons;
        if (!state.showRibbons) continue;

        const posArr = mesh.geometry.attributes.position.array;
        const uFrac = r / NUM_RIBBONS;
        const uAngle = uFrac * Math.PI * 2;

        // Base latitude on S^2 for Hopf fibration
        const baseTheta = 0.28 + (r % 8) * 0.34;
        const ribbonWidth = 0.085;

        for (let s = 0; s <= SEGMENTS_PER_RIBBON; s++) {
          const vFrac = s / SEGMENTS_PER_RIBBON;
          const vAngle = vFrac * Math.PI * 2;

          evalRibbonCurve(r, uAngle, vAngle, baseTheta, psi4D, eta, L, M, N, waveAmp, explode, elapsed, pCurr);
          evalRibbonCurve(r, uAngle, vAngle + 0.04, baseTheta, psi4D, eta, L, M, N, waveAmp, explode, elapsed, pNext);

          tangent.subVectors(pNext, pCurr).normalize();
          binormal.crossVectors(tangent, pCurr).normalize().multiplyScalar(ribbonWidth);

          const idx6 = s * 6;
          posArr[idx6]     = pCurr.x - binormal.x;
          posArr[idx6 + 1] = pCurr.y - binormal.y;
          posArr[idx6 + 2] = pCurr.z - binormal.z;
          posArr[idx6 + 3] = pCurr.x + binormal.x;
          posArr[idx6 + 4] = pCurr.y + binormal.y;
          posArr[idx6 + 5] = pCurr.z + binormal.z;
        }
        mesh.geometry.attributes.position.needsUpdate = true;
        mesh.geometry.computeVertexNormals();
      }

      // 2. Update 4,800 GPU-Instanced Tensor Resonators
      instancedResonators.visible = state.showDipoles;
      if (state.showDipoles) {
        for (let i = 0; i < INSTANCE_COUNT; i++) {
          const sd = seeds[i];
          const theta = sd.theta;
          const phi = sd.phi;

          if (state.mode === 'hopf') {
            // 4D Hopf Fibration Fibers in S^3
            const alpha = theta * 0.5;
            const beta = phi;
            const gamma = (sd.shell * Math.PI * 2) + elapsed * 0.6;
            const x1 = Math.cos(alpha) * Math.cos(beta + gamma);
            const x2 = Math.cos(alpha) * Math.sin(beta + gamma);
            const x3 = Math.sin(alpha) * Math.cos(beta - gamma);
            const x4 = Math.sin(alpha) * Math.sin(beta - gamma);

            const pos3 = project4DPoint(x1, x2, x3, x4, psi4D, eta);
            const harm = assocLegendre(L, M, Math.cos(theta)) * Math.cos(M * phi + elapsed * 2.0);
            pos3.multiplyScalar(1.0 + 0.06 * waveAmp * harm + explode * 0.45 * sd.shell);

            dummyObj.position.copy(pos3);
            dummyObj.lookAt(0, 0, 0);
            const sc = 0.75 + 0.45 * Math.abs(Math.sin(gamma + harm));
            dummyObj.scale.set(sc, sc * 1.3, sc);
          } else if (state.mode === 'helmholtz') {
            // 3D Helmholtz Spherical Bessel Standing-Wave Eigenmodes
            const kr = (1.2 + sd.shell * 2.2) * N * 1.4;
            const jl = sphericalBessel(L, kr);
            const ylm = assocLegendre(L, M, Math.cos(theta)) * Math.cos(M * phi);
            const standingWave = jl * ylm * Math.cos(elapsed * 2.8);

            const rBase = 1.15 + sd.shell * 1.85 + explode * 0.6 * sd.shell;
            const rDisp = Math.max(0.45, rBase + waveAmp * 0.42 * standingWave);

            dummyObj.position.set(
              rDisp * Math.sin(theta) * Math.cos(phi),
              rDisp * Math.cos(theta),
              rDisp * Math.sin(theta) * Math.sin(phi)
            );
            dummyObj.lookAt(0, 0, 0);
            dummyObj.rotateX(Math.PI * 0.5);
            const sc = 0.65 + 0.85 * Math.min(1.2, Math.abs(standingWave));
            dummyObj.scale.set(sc, sc * 1.4, sc);
          } else if (state.mode === 'calabi') {
            // 6D Calabi-Yau String Manifold Cross-Section
            const nDim = Math.max(3, L + 1);
            const k1 = i % nDim;
            const k2 = Math.floor(i / nDim) % nDim;
            const u = (sd.theta - Math.PI * 0.5) * 0.85;
            const v = sd.phi;

            const phase1 = (2 * Math.PI * k1) / nDim + psi4D * 0.5;
            const phase2 = (2 * Math.PI * k2) / nDim - psi4D * 0.5;

            const rScale = 2.35 + explode * 0.35 * (k1 % 3);
            const x = rScale * Math.cos(u) * Math.cos(v + phase1);
            const y = rScale * Math.sin(u) * Math.cos(v + phase2);
            const z = rScale * Math.sin(v + (phase1 - phase2) * 0.5) * (0.75 + 0.25 * Math.cos(M * u + elapsed * 2.0));

            dummyObj.position.set(x, y, z);
            dummyObj.lookAt(0, 0, 0);
            dummyObj.scale.set(0.9, 1.3, 0.9);
          } else {
            // 3D Biharmonic Chladni Cymatic Tensor Shell
            const chladni =
              Math.cos(L * theta) * Math.cos(M * phi) -
              Math.cos(M * theta) * Math.cos(L * phi);
            const rShell = 2.25 + 0.38 * waveAmp * chladni * Math.cos(elapsed * 2.4 + N * sd.shell) + (sd.shell - 0.5) * (0.45 + explode);

            dummyObj.position.set(
              rShell * Math.sin(theta) * Math.cos(phi),
              rShell * Math.cos(theta),
              rShell * Math.sin(theta) * Math.sin(phi)
            );
            dummyObj.lookAt(0, 0, 0);
            const sc = 0.7 + 0.6 * Math.abs(chladni);
            dummyObj.scale.set(sc, sc * 1.25, sc);
          }

          dummyObj.updateMatrix();
          instancedResonators.setMatrixAt(i, dummyObj.matrix);
        }
        instancedResonators.instanceMatrix.needsUpdate = true;
      }
    }

    function evalRibbonCurve(r, uAngle, vAngle, baseTheta, psi4D, eta, L, M, N, waveAmp, explode, elapsed, outVec) {
      if (state.mode === 'hopf') {
        const alpha = baseTheta * 0.5 + 0.06 * waveAmp * Math.sin(L * vAngle + elapsed * 1.5);
        const x1 = Math.cos(alpha) * Math.cos(uAngle + vAngle);
        const x2 = Math.cos(alpha) * Math.sin(uAngle + vAngle);
        const x3 = Math.sin(alpha) * Math.cos(uAngle - vAngle * M);
        const x4 = Math.sin(alpha) * Math.sin(uAngle - vAngle * M);
        const p = project4DPoint(x1, x2, x3, x4, psi4D, eta);
        outVec.copy(p).multiplyScalar(1.0 + explode * 0.15 * (r % 4));
      } else if (state.mode === 'helmholtz') {
        const rad = 1.65 + (r % 4) * 0.48 + explode * 0.25 * (r % 4);
        const mod = 0.28 * waveAmp * Math.sin(L * vAngle + elapsed * 2.2) * Math.cos(M * uAngle);
        const R = rad + mod;
        outVec.set(
          R * Math.cos(vAngle) * Math.cos(uAngle),
          R * Math.sin(vAngle) + 0.25 * Math.sin(N * uAngle + psi4D),
          R * Math.cos(vAngle) * Math.sin(uAngle)
        );
      } else if (state.mode === 'calabi') {
        const nSym = Math.max(3, L + 1);
        const p1 = (2 * Math.PI * (r % nSym)) / nSym;
        const R = 2.1 + 0.45 * Math.cos(M * vAngle + psi4D) + explode * 0.2 * (r % 4);
        outVec.set(
          R * Math.cos(vAngle + p1) * Math.cos(uAngle),
          R * Math.sin(vAngle * N * 0.5 + psi4D),
          R * Math.sin(vAngle + p1) * Math.sin(uAngle)
        );
      } else {
        const ch = Math.cos(L * vAngle) * Math.sin(M * uAngle);
        const R = 2.15 + 0.42 * waveAmp * ch * Math.cos(elapsed * 2.0) + explode * 0.2 * (r % 4);
        outVec.set(
          R * Math.sin(vAngle) * Math.cos(uAngle + 0.3 * Math.sin(L * vAngle)),
          R * Math.cos(vAngle),
          R * Math.sin(vAngle) * Math.sin(uAngle + 0.3 * Math.sin(L * vAngle))
        );
      }
    }

    // =========================================================================
    // 5. LIVE 2D CHLADNI BIHARMONIC NODAL PLATE ANALYZER (BOTTOM-LEFT)
    // =========================================================================
    const chCanvas = document.getElementById('chladniCanvas');
    const chCtx = chCanvas.getContext('2d');
    const CW = chCanvas.width;
    const CH = chCanvas.height;
    const chImg = chCtx.createImageData(CW, CH);

    function renderChladniPlate(elapsed) {
      const data = chImg.data;
      const L = state.L;
      const M = Math.max(1, state.M);
      const N = state.N;
      const tOsc = Math.cos(elapsed * 2.2) * 0.25;

      let p = 0;
      for (let py = 0; py < CH; py++) {
        const y = (py / CH - 0.5) * 2.0;
        for (let px = 0; px < CW; px++) {
          const x = (px / CW - 0.5) * 2.0;

          // Classic Chladni eigenfunction u(x,y) = cos(n*pi*x)*cos(m*pi*y) - cos(m*pi*x)*cos(n*pi*y)
          const val =
            Math.cos(L * Math.PI * x * 0.85) * Math.cos(M * Math.PI * y * 0.85) -
            Math.cos(M * Math.PI * x * 0.85) * Math.cos(L * Math.PI * y * 0.85) +
            tOsc * Math.cos(N * Math.PI * (x * x + y * y));

          const absV = Math.abs(val);

          if (absV < 0.085) {
            // Sharp Nodal Line (International Klein Blue)
            data[p] = 0; data[p + 1] = 56; data[p + 2] = 255; data[p + 3] = 255;
          } else if (absV < 0.17) {
            // Vermilion Harmonic Contour
            data[p] = 255; data[p + 1] = 68; data[p + 2] = 31; data[p + 3] = 255;
          } else {
            // Crisp Daylight Paper Field
            const shade = Math.max(228, Math.floor(250 - absV * 10));
            data[p] = shade; data[p + 1] = shade - 1; data[p + 2] = shade - 5; data[p + 3] = 255;
          }
          p += 4;
        }
      }
      chCtx.putImageData(chImg, 0, 0);
    }

    // Click Chladni Plate to step to next harmonic eigenmode
    chCanvas.addEventListener('click', () => {
      state.L = (state.L % 7) + 2;
      state.M = ((state.M + 1) % state.L);
      syncQuantumLabels();
      sendTelemetryToWSL("CHLADNI_PLATE_EXCITED");
    });

    // =========================================================================
    // 6. UI CONTROLS, QUANTUM STEPPERS & TRANSPORT BUTTONS
    // =========================================================================
    function syncQuantumLabels() {
      document.getElementById('valL').textContent = state.L;
      document.getElementById('valM').textContent = state.M;
      document.getElementById('valN').textContent = state.N;
      document.getElementById('chladniModeTag').textContent = `(ℓ=${state.L}, m=${state.M}, n=${state.N})`;

      const freq = Math.round(240 * Math.sqrt(state.L * (state.L + 1) + state.N * state.N * 2.4 + state.M * 1.5));
      document.getElementById('valFreq').textContent = `${freq.toLocaleString()} Hz`;
      const curv = (1.1 + state.poleDepth * 1.2 + state.L * 0.08).toFixed(2);
      document.getElementById('valCurvature').textContent = `+${curv} κ`;
    }

    document.getElementById('btnLDec').addEventListener('click', () => { state.L = Math.max(1, state.L - 1); state.M = Math.min(state.L, state.M); syncQuantumLabels(); sendTelemetryToWSL("STEP_DEGREE_L"); });
    document.getElementById('btnLInc').addEventListener('click', () => { state.L = Math.min(8, state.L + 1); syncQuantumLabels(); sendTelemetryToWSL("STEP_DEGREE_L"); });
    document.getElementById('btnMDec').addEventListener('click', () => { state.M = Math.max(0, state.M - 1); syncQuantumLabels(); sendTelemetryToWSL("STEP_ORDER_M"); });
    document.getElementById('btnMInc').addEventListener('click', () => { state.M = Math.min(state.L, state.M + 1); syncQuantumLabels(); sendTelemetryToWSL("STEP_ORDER_M"); });
    document.getElementById('btnNDec').addEventListener('click', () => { state.N = Math.max(1, state.N - 1); syncQuantumLabels(); sendTelemetryToWSL("STEP_RADIAL_N"); });
    document.getElementById('btnNInc').addEventListener('click', () => { state.N = Math.min(6, state.N + 1); syncQuantumLabels(); sendTelemetryToWSL("STEP_RADIAL_N"); });

    const MODE_META = {
      hopf:      { euler: 'χ = 0 (T²)',  sub: 'STEREOGRAPHIC S³ → R³ PROJECTION & CLIFFORD TORI' },
      helmholtz: { euler: 'χ = 2 (S²)',  sub: '3D HELMHOLTZ BESSEL ACOUSTIC LEVITATION SHELLS' },
      calabi:    { euler: 'χ = −200',    sub: '6D CALABI–YAU QUINTIC HYPERSURFACE PROJECTION' },
      chladni:   { euler: '∇⁴u = λu',    sub: 'BIHARMONIC CHLADNI CYMATIC EIGENMODE RESONANCE' }
    };

    document.querySelectorAll('[data-mode]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-mode]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.mode = btn.dataset.mode;
        document.getElementById('valEuler').textContent = MODE_META[state.mode].euler;
        document.getElementById('labSubtitle').textContent = MODE_META[state.mode].sub;
        sendTelemetryToWSL(`MODE_${state.mode.toUpperCase()}`);
      });
    });

    document.querySelectorAll('[data-theme]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-theme]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.theme = btn.dataset.theme;
        applyStudioTheme(state.theme);
        sendTelemetryToWSL(`THEME_${state.theme.toUpperCase()}`);
      });
    });

    // Bottom Transport Controls
    const btnSpin3D = document.getElementById('btnSpin3D');
    btnSpin3D.addEventListener('click', () => {
      state.spin3D = !state.spin3D;
      btnSpin3D.textContent = state.spin3D ? '⏸ 3D Spin' : '▶ 3D Spin';
      btnSpin3D.classList.toggle('active', state.spin3D);
    });

    document.getElementById('btnReverse3D').addEventListener('click', () => {
      state.spinDir *= -1;
    });

    const btnSpin4D = document.getElementById('btnSpin4D');
    btnSpin4D.addEventListener('click', () => {
      state.spin4D = !state.spin4D;
      btnSpin4D.classList.toggle('active', state.spin4D);
      sendTelemetryToWSL(state.spin4D ? "4D_CLIFFORD_ON" : "4D_CLIFFORD_OFF");
    });

    const btnGimbal = document.getElementById('btnGimbal');
    btnGimbal.addEventListener('click', () => {
      state.gimbal = !state.gimbal;
      btnGimbal.classList.toggle('active', state.gimbal);
      if (!state.gimbal) {
        sculptureGroup.rotation.x = 0;
        sculptureGroup.rotation.z = 0;
      }
    });

    document.getElementById('btnResonancePulse').addEventListener('click', () => {
      state.pulseBoost = 1.8;
      sendTelemetryToWSL("HARMONIC_RESONANCE_PULSE");
    });

    const btnToggleRibbons = document.getElementById('btnToggleRibbons');
    btnToggleRibbons.addEventListener('click', () => {
      state.showRibbons = !state.showRibbons;
      btnToggleRibbons.classList.toggle('active', state.showRibbons);
    });

    const btnToggleDipoles = document.getElementById('btnToggleDipoles');
    btnToggleDipoles.addEventListener('click', () => {
      state.showDipoles = !state.showDipoles;
      btnToggleDipoles.classList.toggle('active', state.showDipoles);
    });

    let camTarget = null;
    function moveCam(x, y, z) { camTarget = new THREE.Vector3(x, y, z); }
    document.getElementById('camStudio').addEventListener('click', () => moveCam(0, 3.2, 11.8));
    document.getElementById('camZenith').addEventListener('click', () => moveCam(0, 12.5, 0.01));
    document.getElementById('camCinema').addEventListener('click', () => document.body.classList.toggle('ui-hidden'));

    // Sliders
    document.getElementById('slSpeed4D').addEventListener('input', (e) => {
      state.speed4D = parseFloat(e.target.value);
      document.getElementById('lblSpeed4D').textContent = `${state.speed4D.toFixed(2)} rad/s`;
    });

    document.getElementById('slSpeed3D').addEventListener('input', (e) => {
      state.speed3D = parseFloat(e.target.value);
      document.getElementById('lblSpeed3D').textContent = `${state.speed3D.toFixed(2)} rad/s`;
    });

    document.getElementById('slPole').addEventListener('input', (e) => {
      state.poleDepth = parseFloat(e.target.value);
      document.getElementById('lblPole').textContent = state.poleDepth.toFixed(2);
      syncQuantumLabels();
    });

    document.getElementById('slWaveAmp').addEventListener('input', (e) => {
      state.waveAmp = parseFloat(e.target.value);
      document.getElementById('lblWaveAmp').textContent = `${state.waveAmp.toFixed(2)}x`;
    });

    document.getElementById('slExplode').addEventListener('input', (e) => {
      state.explode = parseFloat(e.target.value);
      document.getElementById('lblExplode').textContent = state.explode.toFixed(2);
    });

    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space') { e.preventDefault(); btnSpin3D.click(); }
      else if (e.key === 'h' || e.key === 'H') document.body.classList.toggle('ui-hidden');
    });

    sendTelemetryToWSL("INITIALIZE_AETHER_4D");

    // =========================================================================
    // 7. 60FPS ANIMATION LOOP
    // =========================================================================
    const clock = new THREE.Clock();

    function animate() {
      requestAnimationFrame(animate);

      const dt = Math.min(clock.getDelta(), 0.05);
      const elapsed = clock.getElapsedTime();

      if (state.pulseBoost > 0.01) {
        state.pulseBoost *= Math.exp(-dt * 3.0);
      } else {
        state.pulseBoost = 0;
      }

      if (state.spin4D) {
        state.phase4D += dt * state.speed4D * state.spinDir;
        document.getElementById('so4Readout').textContent = `SO(4) ψ=${(state.phase4D % 6.283).toFixed(2)}`;
      }

      if (state.spin3D) {
        sculptureGroup.rotation.y += dt * state.speed3D * state.spinDir;
        if (state.gimbal) {
          sculptureGroup.rotation.x = Math.sin(elapsed * 0.55) * 0.45;
          sculptureGroup.rotation.z = Math.cos(elapsed * 0.40) * 0.35;
        }
      }

      updateManifoldGeometry(elapsed);
      renderChladniPlate(elapsed);

      if (camTarget) {
        camera.position.lerp(camTarget, dt * 5.0);
        controls.target.lerp(new THREE.Vector3(0, 0.2, 0), dt * 5.0);
        if (camera.position.distanceTo(camTarget) < 0.08) camTarget = null;
      }

      controls.update();
      renderer.render(scene, camera);
    }

    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>
"""


class AetherManifoldHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(HTML_PAYLOAD.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/telemetry":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8")
            try:
                data = json.loads(raw)
                ts = time.strftime("%H:%M:%S")
                ev = data.get("event", "UPDATE")
                mode = data.get("mode", "hopf").upper()
                l_val = data.get("L", 3)
                m_val = data.get("M", 2)
                n_val = data.get("N", 2)
                freq = data.get("freq", 1428)
                pole = data.get("pole", 0.68)

                print(
                    f"{DIM}[{ts}]{RESET} "
                    f"{BLUE}{BOLD}[AETHER-4D]{RESET} "
                    f"Event={VERMILION}{ev:<22}{RESET} | "
                    f"Manifold={GOLD}{mode:<9}{RESET} | "
                    f"(ℓ,m,n)=({l_val},{m_val},{n_val}) | "
                    f"Eigenfreq={TEAL}{freq:<5} Hz{RESET} | "
                    f"Pole η={GREEN}{pole:.2f}{RESET}",
                    flush=True,
                )
            except Exception:
                pass

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


def find_free_port(start_port=8095):
    for port in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


def open_browser_from_wsl(url):
    time.sleep(0.8)
    try:
        with open("/proc/version", "r") as f:
            proc_ver = f.read().lower()
        if "microsoft" in proc_ver or "wsl" in proc_ver:
            subprocess.Popen(
                ["cmd.exe", "/c", "start", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
    except Exception:
        pass

    try:
        subprocess.Popen(
            ["xdg-open", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def main():
    port = find_free_port(8095)
    url = f"http://localhost:{port}"

    os.system("clear" if os.name == "posix" else "cls")
    print(f"{BLUE}{BOLD}" + "=" * 92 + f"{RESET}")
    print(
        f"{GOLD}{BOLD}   AETHER-4D // RIEMANNIAN STEREOGRAPHIC MANIFOLD & HELMHOLTZ EIGENMODE STUDIO{RESET}"
    )
    print(
        f"{DIM}   Mathematics: P(x) = x_1..3 / (1 - η·x_4)  |  ∇²Ψ + k²Ψ = 0  |  4,800 GPU Instanced Resonators{RESET}"
    )
    print(f"{BLUE}{BOLD}" + "=" * 92 + f"{RESET}")
    print(
        f" {GREEN}✔{RESET} {BOLD}WSL Ubuntu Aether-4D Studio Active:{RESET}   {TEAL}{BOLD}{url}{RESET}"
    )
    print(
        f" {GREEN}✔{RESET} {BOLD}VS Code Quick Open:{RESET}                  {GOLD}Ctrl + Click{RESET} the link above"
    )
    print(
        f" {GREEN}✔{RESET} {BOLD}Stop Server:{RESET}                         Press {VERMILION}Ctrl + C{RESET} in this Ubuntu terminal"
    )
    print(f"{BLUE}" + "-" * 92 + f"{RESET}")
    print(
        f"{BOLD} LIVE SO(4) RIEMANNIAN & HELMHOLTZ EIGENMODE TELEMETRY STREAM:{RESET}"
    )

    threading.Thread(target=open_browser_from_wsl, args=(url,), daemon=True).start()

    server = http.server.ThreadingHTTPServer(("0.0.0.0", port), AetherManifoldHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(
            f"\n{VERMILION}[AETHER-4D STOPPED]{RESET} Shutting down 4D Manifold Studio."
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
