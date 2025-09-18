# 👽 ASTROULETTE 👽

[Astroulette](https://astroulette.com) is a retro-futuristic chat roulette where users have real-time conversations with alien characters generated on the spot by AI.

I built this project for three main reasons:  
👾 Because I love Sci-Fi.  
🤖 Because I love AI engineering.  
👨🏻‍💻 Because I wanted to sharpen my dev skills.

Pretty much, it's a labor of love! ❤️

---

## 🧠 Tech Stack

- Typescript: Svelte 5, SvelteKit 2
- Python: FastAPI, SQLModel, SQLAlchemy
- Database: SQLite3
- Deployment: Fly.io, Docker, NGINX, supervisord
- AI Integration: OpenAI API, Leonardo.Ai
- Auth: Magic link via JWT and email

> **Why didn’t I write backend with TS/Sveltekit?**  
> I wanted to hone my skills with both Python and Typescript. Splitting this project gave me the chance to do so, and to experiment with Svelte. That said, I may migrate the API to TS in the future.

---

## 🚦 How It Works

🧑🏻‍🚀 User lands on the login page and enters a username and email.  
📧 A magic link is emailed to them with a JWT token.  
🚪 Once validated, a loading screen appears while...  
👽 A brand-new alien character is generated in the background.  
💬 The user enters a WebSocket chat with the character!

---

## 🧬 Character Creation & The AI of It All

Every character starts with randomized traits:  
_sex, species, and archetype_ (e.g. **male cyborg galactic emperor**).  
These are passed into the AI prompt.

The generation process is two-fold:

1. **[OpenAI API](https://platform.openai.com/docs/overview)**  
   A structured chat request returns:

   - An image prompt
   - The alien’s name, planet, and detailed personality

2. **[Leonardo.Ai API](https://docs.leonardo.ai/docs/getting-started)**  
   The image prompt is used to generate a matching portrait of the alien.

This ensures that each character’s look, backstory, and personality are thematically coherent.

🚀 **Time for a galactic chat!**  
A new OpenAI chat request streams responses into a WebSocket.  
The frontend displays:

- The alien’s portrait
- A real-time chat window

And because it’s a roulette, if you're not vibing with your alien... you can spin again.

---

## 🚀 Deployment

The app is deployed on [Fly.io](https://fly.io/) in a single container, using NGINX and supervisord to stitch the frontend and backend together.

This extra complexity is the main reason I would migrate the API into Sveltekit, at least when the endpoints are really only useful for one product.

---

## 🛠 What's Next?

This is just the beginning. Future improvements include:

- Add e2e test coverage, and incorproate into the CI/CD pipeline
- Migrate local sqlite db file to Turso for better data persistence
- Exploring better prompt tuning and alternate LLMs
- Integrating [Hedra](https://www.hedra.com/) or similar to animate characters as they speak

---

🪐 **Please enjoy the ride!** 🪐
