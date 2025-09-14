# Functional Requirements Document: Mountain Cabin Interior Design Playable Ad

## 1. Introduction

This document provides a detailed outline of the functional requirements for the HTML5 Mountain Cabin Playable Ad. It describes the features, interactions, and rules that govern the ad's behavior from the user's perspective. The purpose of this document is to define the "what" the system will do.

## 2. System Scope

The system is a self-contained, interactive HTML5 playable ad designed to run in mobile and desktop web browsers and in-app webviews. Its primary function is to showcase the gameplay of the "Venue" interior design app and drive installs.

## 3. Functional Requirements

| ID      | Requirement                                                                                                                              | Details                                                                                                                                                                                            |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FR-001** | **Ad Initialization & Intro Screen**                                                                                                        | The ad shall load and display an initial introductory screen. This screen must contain a "Start" button to begin the experience.                                                                      |
| **FR-002** | **Start Interaction**                                                                                                                    | Upon user interaction with the "Start" button, the intro screen shall be hidden, and the main interactive cabin scene shall become visible and active.                                                 |
| **FR-003** | **Display of Interactive Hotspots**                                                                                                      | The system shall display five distinct, interactive hotspots on the cabin scene at predefined coordinates. Each hotspot corresponds to a customizable object: Chandelier, Windows, Bed Frame, Bed Sheets, Floor. |
| **FR-004** | **Hotspot Interactivity**                                                                                                                | Each hotspot must be clickable. When a user clicks a hotspot, the system shall open a catalog UI corresponding to that object.                                                                         |
| **FR-005** | **Display Customization Catalog**                                                                                                        | The catalog UI must display nine unique design variants for the selected object. The variants shall be presented as selectable thumbnails.                                                             |
| **FR-006** | **Variant Selection & Scene Update**                                                                                                     | When a user selects a variant from the catalog, the system shall instantly update the main cabin scene to render the chosen design for the corresponding object. The catalog must remain open for further selections. |
| **FR-007** | **Call-to-Action (CTA)**                                                                                                                 | The system shall display a "Download" button. Upon clicking this button, the user shall be redirected to a specified App Store or Google Play Store URL.                                                  |
| **FR-009** | **Tutorial Hand Guidance**                                                                                                      | On initialization, the Windows catalog opens. A guiding hand animates through each option, highlighting the option bubble in green and applying the corresponding design. The hand moves every 1.5 seconds to the next option. The tutorial ends when the user interacts (mouse movement or tap), and the game proceeds once the user selects an option. |
| **FR-008** | **Debug Mode Functionality**                                                                                                             | When debug mode is enabled (`showDebugInfo: true`), the system shall display an on-screen HUD showing the real-time X/Y coordinates of the mouse pointer to assist with positioning.                      |

## 4. User Interface (UI) Requirements

| ID      | Requirement               | Details                                                                                                    |
| :------ | :------------------------ | :--------------------------------------------------------------------------------------------------------- |
| **UI-001** | **Main Scene View**       | The ad shall render a high-quality, static background image of a mountain cabin interior.                  |
| **UI-002** | **Hotspot Visuals**       | Hotspots shall be rendered as animated, pulsing circular dots to clearly indicate they are interactive elements. |
| **UI-003** | **Catalog UI**            | The catalog shall be presented as a non-intrusive, scrollable overlay panel.                               |
| **UI-004** | **Variant Thumbnails**    | Each item in the catalog shall be represented by a clear thumbnail image previewing the design variant.    |

## 5. Non-Functional Requirements

| ID       | Requirement         | Details                                                                                                                                                                      |
| :------- | :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **NFR-001** | **Responsiveness**    | The ad's layout must be fully responsive, scaling via a CSS `transform` to fill the available screen space while maintaining its 720x1280 aspect ratio using "cover" logic. |
| **NFR-002** | **Performance**       | The ad must be highly performant, with a minimal initial load size and instantaneous feedback for all user interactions (e.g., variant selection).                            |
| **NFR-003** | **Compatibility**     | The ad must render and function correctly across all modern mobile and desktop browsers, including Chrome, Safari, and Firefox.                                             |
| **NFR-004** | **Portability**       | The ad must be delivered as a single, self-contained `index.html` file with no external dependencies (JS libraries, CSS frameworks, etc.).                                     |

---
