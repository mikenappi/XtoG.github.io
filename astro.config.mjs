import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://mikenappi.github.io',
  base: '/XtoG.github.io',
  integrations: [starlight({
    title: 'X to G',
    description: 'A philosophical argument from contingency to a necessary mental foundation.',
    head: [{ tag: 'script', attrs: { src: '/XtoG.github.io/reading-transition.js' } }],
    components: {
      PageFrame: './src/components/ExpansionFrame.astro',
      TwoColumnContent: './src/components/ReadingColumn.astro',
    },
    pagination: false,
    customCss: ['./src/styles/reader.css'],
    sidebar: [],
  })],
});
