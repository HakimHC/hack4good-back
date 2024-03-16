async function mango() {
    try {
        const headers = {
            "Content-Type": "application/json",
        };
        const response = await fetch("https://planeat.pro/api/search", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                prompt: "Make me a vegetarian meal with products of somewhere",
            }),
        });
        console.log(headers); // This will log the headers object you've defined

        const data = await response.json(); // Correctly parsing the response body as JSON
        console.log(data); // This will log the actual JSON response body
    } catch (err) {
        console.error(err); // This will log any errors that occur during the fetch operation
    }
}

mango();
