/** @type {import('./$types').LayoutLoad} */
export const load = async ({ fetch }) => {
    try {
        const response = await fetch('/counter');
        const data = await response.json();
        console.log("Pageload counter:", data.counter);
        return { counter: data.counter };
    } catch (error) {
        console.error('Error fetching counter:', error);
        return { counter: '0' };
    }
}
