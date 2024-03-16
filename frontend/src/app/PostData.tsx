const handleSubmit = async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);
  const promptValue = formData.get("prompt");

  try {
    const res = await fetch("http://localhost:8080/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt: promptValue })
    });

    if (res.ok) {
      const js = await res.json();
      console.log(js);
      return js;
    } else {
      console.error("Failed to fetch data");
      return {};
    }
  } catch (error) {
    console.error("Error occurred:", error);
    return {};
  }
};

const PostData = () => {
  return (
    <form
      onSubmit={handleSubmit}
      className="w-full flex flex-row justify-end"
    >
      <textarea
        name="prompt"
        placeholder="Make me a vegetarian meal with products of carrefour."
        className="max-h-96 min-h-12 h-10 w-2/5 rounded-xl flex flex-row justify-start bg-slate-100 p-3 text-gray-500"
      ></textarea>
      <button type="submit">Send</button>
    </form>
  );
};

export { PostData };