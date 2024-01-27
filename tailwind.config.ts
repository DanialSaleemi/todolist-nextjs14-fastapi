import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
          'metallic-navy': 'linear-gradient(135deg, #000080 0%, #1a1a1a 50%, #000080 100%)',
      },
      colors: {
        'deep-blue': '#00008B',
        'navy': '#000080'
      }
    },
  },
  plugins: [],
}
export default config
