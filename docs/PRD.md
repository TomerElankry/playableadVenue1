# Product Requirements Document: Mountain Cabin Interior Design Playable Ad

## 1. Overview

This document outlines the product requirements for a responsive HTML5 playable ad for the "Venue" interior design mobile game. The ad provides a short, interactive experience where users can customize the interior of a mountain cabin. The primary goal of the ad is to drive user acquisition by showcasing the core gameplay mechanic in an engaging format, ultimately leading to app installs.

## 2. Project Goals

*   **Primary Goal:** Increase app installs by providing a compelling and interactive preview of the game.
*   **Secondary Goal:** Boost user engagement by demonstrating the game's creative and customization features.
*   **Technical Goal:** Deliver a lightweight, fast-loading, and highly responsive ad that performs seamlessly across all mobile devices and webviews.

## 3. Target Audience

The target audience is players of casual, simulation, and interior design mobile games. These users enjoy creative expression, customization, and relaxing gameplay.

## 4. Key Features

### 4.1. Interactive Cabin Scene
The ad features a high-quality, static image of a mountain cabin interior which serves as the main canvas for the user's interactions.

### 4.2. Interactive Hotspots
There are five distinct interactive zones in the cabin, each marked by an animated, pulsing dot to draw user attention.
*   **Chandelier:** Allows customization of the main lighting fixture.
*   **Windows:** Allows customization of the window frames/style.
*   **Bed Frame:** Allows customization of the bed's frame.
*   **Bed Sheets:** Allows customization of the bedding/sheets.
*   **Floor:** Allows customization of the flooring material.

### 4.3. Object Customization
*   Clicking on a hotspot opens a simple, scrollable catalog.
*   Each catalog contains **nine unique design variants** for the corresponding object.
*   Selecting a variant from the catalog instantly updates the main cabin scene to display the new design.

### 4.4. Call to Action (CTA)
*   A "Download" button is present to direct users to the appropriate app store.
*   The CTA links to both the Google Play Store and the Apple App Store.

### 4.5. Intro Screen
*   The ad begins with an introductory overlay or message (e.g., "Help us decorate the cabin!") to provide context and prompt the user to start.

## 5. Design & UX Requirements

### 5.1. Layout & Responsiveness
*   The ad is designed for a **base portrait resolution of 720x1280**.
*   The ad must be **fully responsive**, scaling to fill the entire browser or webview window on any device.
*   A **"cover" scaling method** (`Math.max`) is used to ensure the ad fills the screen without letterboxing, even if minor cropping of the background occurs on different aspect ratios.
*   The layout must adapt to both portrait and landscape orientations, disabling page scroll.

## 6. Technical Specifications

### 6.1. Platform
*   **Technology:** Built with vanilla HTML5, CSS3, and JavaScript.
*   **Dependencies:** No external libraries or frameworks are used to minimize bundle size and load times.

### 6.2. File Structure
*   The entire ad (HTML, CSS, JS) is self-contained within a single `index.html` file for simplicity and portability.
*   Image assets for object variants are loaded dynamically as needed.

### 6.3. Performance
*   **Bundle Size:** The initial download size must be minimal to meet the strict requirements of ad networks.
*   **Load Time:** The ad must load quickly to prevent user drop-off.

### 6.4. Configuration & Debugging
*   A centralized `CONFIG` object in the JavaScript holds all critical settings, including hotspot coordinates, store URLs, and feature flags.
*   A **debug mode** (`showDebugInfo: true`) can be enabled to display an on-screen HUD with mouse coordinates, facilitating the precise positioning of hotspots.

---
