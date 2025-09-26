# Product Requirements Document: Mountain Cabin Interior Design Playable Ad

## 1. Overview

This document outlines the product requirements for a responsive HTML5 playable ad for the "Venue" interior design mobile game. The ad provides a short, interactive experience where users can customize the interior of a mountain cabin. The primary goal of the ad is to drive user acquisition by showcasing the core gameplay mechanic in an engaging format, ultimately leading to app installs.

## 2. Project Goals

* **Primary Goal:** Increase app installs by providing a compelling and interactive preview of the game.
* **Secondary Goal:** Boost user engagement by demonstrating the game's creative and customization features.
* **Technical Goal:** Deliver a lightweight, fast-loading, and highly responsive ad that performs seamlessly across all mobile devices and webviews.

## 3. Target Audience

The target audience is players of casual, simulation, and interior design mobile games. These users enjoy creative expression, customization, and relaxing gameplay.

## 4. Key Features

### 4.1. Interactive Cabin Scene
The ad features a high-quality, static image of a mountain cabin interior which serves as the main canvas for the user's interactions.

### 4.2. Interactive Hotspots
There are six interactive zones in the cabin, each marked by a circular hotspot to draw user attention.
* **Windows**
* **Chandelier**
* **Bed Frame**
* **Bed Sheets**
* **Floor**
* **Walls**

### 4.3. Object Customization
* Clicking a hotspot opens a scrollable right-side catalog with variants and names.
* Each catalog contains up to six design variants for the corresponding object.
* Selecting a variant previews it; confirming applies it to the scene.

### 4.4. Completion & CTA
* When all six zones are confirmed, show a final overlay with a congratulatory message, five animated white stars, and a CTA button.
* The CTA navigates in the same tab to a configurable store URL.

### 4.5. Tutorial
* On load, the Windows catalog auto-opens and a hand guides attention across items until the user interacts (mouse/touch).
* The tutorial ends immediately on interaction; normal flow continues.

## 5. Design & UX Requirements

### 5.1. Layout & Responsiveness
* Designed for portrait 720×1280; scales responsively to fill the viewport.

### 5.2. Visual Hierarchy & Layering
* Layer order (back → front): Walls (0), Floor (2), Bed Sheets (3), Bed Frame (4), Windows (5), Chandelier (6), Hotspots (10).
* Hotspots always remain clickable above layers.

### 5.3. Transitions
* Windows: fade 0.5 → 1.0 opacity.
* Bed Sheets: fade 0.3 → 1.0 opacity.
* Floor: fade 0.4 → 1.0 opacity.
* Chandelier: direct fade 0 → 1 without overlay.
* Walls/Bed Frame: smooth overlay cross-fade.
* Global timing: ~0.4s ease-in-out; images are preloaded for smoothness.

### 5.4. Feedback & Effects
* On confirm, an achievement effect spawns three jumping white stars with a subtle glow near the hotspot.

## 6. Technical Specifications

### 6.1. Platform
* **Technology:** Vanilla HTML, CSS, JavaScript.
* **Dependencies:** None (no third-party frameworks/libraries).

### 6.2. Assets
* Walls use transparent PNGs (resized and optimized ~120–170KB each) to composite correctly over the scene.
* Thumbnails and view images are loaded on demand with cache-busting querystrings.

### 6.3. Configuration & Debugging
* All settings live under a `CONFIG` object (zones, coordinates, tutorial, URLs).
* Optional debug HUD shows mouse and container metrics.

---
