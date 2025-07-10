# SnapPic - Ephemeral Image Sharing PWA

SnapPic is a lightweight, Progressive Web App (PWA) for quick image sharing with an ephemeral gallery experience.

## Features

- 📸 Instant photo upload via camera or gallery
- 🖼️ Temporary image gallery with automatic rotation
- 💬 Optional image comments
- 📱 Mobile-first, responsive design
- 🌐 Progressive Web App with offline support

## Screenshots

### Upload Interface
![Upload Interface](/index.png)

### Gallery View
![Gallery View](/gallery.png)

## Technical Specifications

- **Backend:** Flask (Python)
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **Storage:** Local JSON and file system
- **Constraints:**
  - Max 10 images in gallery
  - Images visible for 5 seconds
  - Max 5MB per image
  - Supports JPG, PNG, WEBP

## Installation

1. Ensure Python 3.8+ is installed
2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Run the application:
   ```bash
   python snappic/app.py
   ```

4. Open browser to `http://localhost:5000`

## Project Structure

```
snappic/
├── app.py                 # Flask application
├── data.json             # Image metadata
├── templates/
│   ├── index.html        # Upload page
│   └── gallery.html      # Gallery page
├── static/
│   ├── style.css         # Styling
│   ├── script.js         # Client-side logic
│   ├── manifest.json     # PWA manifest
│   └── icon-192.png      # App icon
└── uploads/              # Uploaded images
```

## Deployment

- Runs directly with `python snappic/app.py`
- Serves on `localhost:5000`
- No additional configuration required

## Contributing

Feel free to open issues or submit pull requests.

## License

MIT License

---

## Project Generation

- Created with [opencode](https://opencode.ai) v0.2.21
- AI Assistant: Claude Haiku 3.5