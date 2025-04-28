/** @type {import('./$types').LayoutLoad} */
export const load = async ({ fetch }) => {
    try {
        console.log("Starting counter fetch in layout load");
        const response = await fetch('/counter');
        console.log("Counter fetch response status:", response.status);
        if (!response.ok) {
            console.error("Counter fetch failed with status:", response.status);
            return { counter: '0' };
        }
        const data = await response.json();
        console.log("Pageload counter data:", data);
        return { counter: data.counter };
    } catch (error) {
        console.error('Error fetching counter:', error);
        return { counter: '0' };
    }
}
