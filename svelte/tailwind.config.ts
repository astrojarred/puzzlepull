import { fontFamily } from 'tailwindcss/defaultTheme';
import type { Config } from 'tailwindcss';

const config: Config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				ink: {
					DEFAULT: '#1b2a41',
					soft: '#3a4a63'
				},
				paper: {
					DEFAULT: '#f4f6f8',
					deep: '#e8edf2'
				},
				line: '#c5ced9',
				cobalt: {
					DEFAULT: '#2f6fed',
					deep: '#1f54c4'
				}
			},
			fontFamily: {
				sans: ['DM Sans', ...fontFamily.sans],
				display: ['Fraunces', 'Georgia', 'serif']
			},
			borderRadius: {
				xl: '0.75rem'
			}
		}
	}
};

export default config;
