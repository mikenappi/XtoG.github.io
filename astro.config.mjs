import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://mikenappi.github.io',
  base: '/XtoG.github.io',
  integrations: [starlight({
    title: 'X to G',
    description: 'A philosophical argument from contingency to a necessary mental foundation.',
    head: [{ tag: 'script', attrs: { src: '/XtoG.github.io/reading-transition.js' } }],
    components: { ThemeSelect: './src/components/ThemeSelect.astro' },
    customCss: ['./src/styles/reader.css'],
    sidebar: [
      { label: 'Introduction', items: ['overview', 'glossary'] },
      { label: 'The argument', items: ['argument/contingency', 'argument/necessity', 'argument/mind', 'argument/conclusion'] },
      { label: 'Examination & defense', items: ['examination/objections', 'examination/proof', 'examination/sources'] },
    ],
  })],
});
