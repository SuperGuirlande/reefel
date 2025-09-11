/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        '../templates/**/*.html',

        '../../templates/**/*.html',

        '../../**/templates/**/*.html',

        /* JS 1: Ignore any JavaScript in node_modules folder. */
        '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        '../../**/*.py'

    ],
    theme: {
        extend: {
            fontFamily: {
                'poppins': ['Poppins', 'sans-serif'],
                'montserrat': ['Montserrat', 'sans-serif'],
                'raleway': ['Raleway', 'sans-serif'],
            },
            fontWeight: {
                'thin': '100',
                'extralight': '200',
                'light': '300',
                'normal': '400',
                'medium': '500',
                'semibold': '600',
                'bold': '700',
                'extrabold': '800',
                'black': '900',
            },
            colors: {
                'minsk': {
                    '50': '#edf1ff',
                    '100': '#dfe5ff',
                    '200': '#c5cfff',
                    '300': '#a1afff',
                    '400': '#7c84fd',
                    '500': '#5f5df7',
                    '600': '#4f40eb',
                    '700': '#4332d0',
                    '800': '#372ba8',
                    '900': '#362f92',
                    '950': '#1e194d',
                },

            }
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
