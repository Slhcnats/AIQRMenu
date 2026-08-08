# AIQRMenu - AI-Powered Smart QR Menu System

🌐 **Language**

🇬🇧 English | [🇹🇷 Türkçe](README.tr.md)

---

AIQRMenu is a full-stack web application that transforms traditional restaurant menus into an interactive digital experience. By scanning a QR code placed on the table, customers can browse the menu and receive personalized food recommendations through an integrated AI assistant.

## Project Overview

Traditional restaurant menus often make it difficult for customers to quickly find nutritional information, dietary options, or suitable meals. AIQRMenu addresses this by providing an intelligent digital menu where users can instantly filter menu items and receive personalized recommendations based on their preferences.

## Key Features

- **AI-Powered Assistant:** Integrated with the Groq API to provide personalized food recommendations based on the customer's mood, budget, or dietary preferences.
- **Dynamic Menu Filtering:** Browse menu categories instantly without reloading the page using asynchronous filtering.
- **Modern User Interface:** Responsive, mobile-first design with a clean user experience and smooth animations.
- **Automatic QR Code Generation:** Built-in Python-based QR code generator that creates QR codes linked to the live application (via Ngrok), making deployment quick and convenient for restaurants.

## Technology Stack

This project was built using modern web development technologies.

### Backend

- Python
- FastAPI
- Uvicorn

### Artificial Intelligence

- Groq API

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

### Tools

- Ngrok
- qrcode

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Slhcnats/AIQRMenu.git
cd AIQRMenu
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn groq qrcode[pil]
```

### 3. Configure the API

Open the `antigravity.py` file and replace the existing API key with your own Groq API key.

### 4. Run the Application

```bash
uvicorn antigravity:app --reload
```

After starting the server, open:

```
http://localhost:8000
```

Alternatively, you can expose the local server using Ngrok and access the application from any mobile device by scanning the generated QR code.

## Developer

**Salih Can Ateş**

Computer Engineering Student

Fırat University
