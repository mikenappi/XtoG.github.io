import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// Netlify supplies its primary address as URL. Pages serves from the repository path.
const onNetlify = process.env.NETLIFY === 'true';
const base = onNetlify ? '/' : '/XtoG.github.io';
const site = onNetlify ? process.env.URL : 'https://mikenappi.github.io';

export default defineConfig({
  site,
  base,
  integrations: [starlight({
    title: 'X → G',
    description: 'A philosophical argument from contingency to a necessary mental foundation.',
    head: [{ tag: 'script', attrs: { src: `${base.replace(/\/$/, '')}/reading-transition.js` } }],
    components: {
      PageTitle: './src/components/ReadingTitle.astro',
      PageFrame: './src/components/ExpansionFrame.astro',
      TwoColumnContent: './src/components/ReadingColumn.astro',
    },
    pagination: false,
    customCss: ['./src/styles/reader.css'],
    sidebar: [],
  })],
});
