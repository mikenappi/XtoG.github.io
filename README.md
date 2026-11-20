# X to G

An Astro Starlight reading site for the Contingency Argument. The introduction, four argument chapters and examination pages live in `src/content/docs/`. The landing page is `src/pages/index.astro`. Edit the reading order in `astro.config.mjs` and the article theme in `src/styles/reader.css`.

## Local development

Use Node 22.12 or newer. Run `npm install` and `npm run dev`. Open the local URL with the project path `/XtoG.github.io/`. Run `npm run build`, then `python scripts/check-site.py`, to build and check page links, fragment links and local resources. Use `npm run preview` for the production build.

## GitHub Pages

Select **Settings → Pages → Build and deployment → Source → GitHub Actions**. The workflow checks pull requests. A successful build on `main` uploads the static output and deploys to https://mikenappi.github.io/XtoG.github.io/. The repository name makes this a project site under the owner's domain. Keep the configured base path when linking from custom components.
