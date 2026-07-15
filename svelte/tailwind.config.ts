import { fontFamily } from 'tailwindcss/defaultTheme';
import type { Config } from 'tailwindcss';

const config: Config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				ink: {
					DEFAULT: '#121212',
					soft: '#5c5c5c'
				},
				paper: {
					DEFAULT: '#fafaf8',
					deep: '#f3f3ef'
				},
				line: '#d6d6d0',
				signal: {
					DEFAULT: '#e23d28',
					deep: '#c43220'
				},
				cell: '#ecece6'
			},
			fontFamily: {
				sans: ['Source Sans 3', ...fontFamily.sans],
				display: ['Syne', 'system-ui', 'sans-serif'],
				mono: ['IBM Plex Mono', ...fontFamily.mono]
			}
		}
	}
};

export default config;
