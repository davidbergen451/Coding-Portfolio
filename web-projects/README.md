# Web Projects

Two small static sites, polished up for hosting on GitHub Pages.

- **`/chess`** — a site for learning chess: rules, pieces, special moves, media recommendations, and a link out to play a real game on Chess.com.
- **`/piano`** — a site for learning piano chords: an open page for each major chord (C through B), each showing the notes, a little theory, and fingering.
- **`index.html`** at the root — a small landing page linking to both.

## Running it locally

No build step, no dependencies. Just open the files in a browser, or serve the folder with any static server, e.g.:

```bash
python3 -m http.server 8000
```

then visit `http://localhost:8000`.

## Publishing on GitHub Pages

1. Push this folder to a GitHub repository (root of the repo = root of this folder).
2. In the repo, go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to "Deploy from a branch," pick your default branch, and folder `/ (root)`.
4. Save. GitHub will give you a URL like `https://<your-username>.github.io/<repo-name>/`.
5. From there: `.../chess/` for the chess site and `.../piano/` for the piano site.

## Structure

```
.
├── index.html
├── chess/
│   ├── index.html, learn.html, media.html, play.html, source.html, dont-click.html
│   ├── style.css
│   └── assets/
├── piano/
│   ├── index.html, dont-click.html
│   ├── chords/  (c.html … b.html)
│   ├── style.css, script.js
│   └── assets/
```
