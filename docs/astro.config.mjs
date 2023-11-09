import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	integrations: [
		starlight({
			title: '',
			logo: {
				src: './src/assets/bookshelf.png',
			},
			social: {
				github: 'https://github.com/jossmoff/bookshelf',
			},
			sidebar: [
				{
					label: 'Getting Started',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Installation', link: '/getting-started/installation/' },
						{ label: 'Enabling Autocomplete', link: '/getting-started/autocomplete/' },
						{ label: 'Glossary', link: '/getting-started/glossary/' },
					],
				},
				{
					label: 'Bookshelf CLI Reference',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Use the bookshelf command line', link: '/reference/use-bookshelf-cli/' },
						{ label: 'bookshelf cancel', link: '/reference/cancel/' },
						{ label: 'bookshelf create', link: '/reference/create/' },
						{ label: 'bookshelf finish', link: '/reference/finish/' },
						{ label: 'bookshelf info', link: '/reference/info/' },
						{ label: 'bookshelf ls', link: '/reference/ls/' },
						{ label: 'bookshelf rm', link: '/reference/rm/' },
						{ label: 'bookshelf start', link: '/reference/start/' },
						{ label: 'bookshelf stop', link: '/reference/stop/' },
					]
				},
			],
		}),
	],

	// Process images with sharp: https://docs.astro.build/en/guides/assets/#using-sharp
	image: { service: { entrypoint: 'astro/assets/services/sharp' } },
});
