# Flappy Angry Bird - Premium Arcade Game
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-CE-00D4AA?style=for-the-badge&logo=python&logoColor=white)](https://pygame.org/)
[![WebAssembly](https://img.shields.io/badge/WebAssembly-Pygbag-654FF0?style=for-the-badge&logo=webassembly&logoColor=white)](https://pypi.org/project/pygbag/)
[![Flask](https://img.shields.io/badge/Flask-Server-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## Why Flappy Angry Bird?
As a **B.Tech CSE student at VIT** and **B.S. Data Science student at IIT Madras**, I wanted to explore the intersection of classical game development and modern web deployment. 
This project pushes the boundaries of how Python games can be experienced on the web, utilizing **Pygbag** to transpile **Pygame** into **WebAssembly** for a seamless, cross-platform arcade experience without plugins or downloads.

### Key Features
- **Iconic Character Design** - Features a custom, programmatically drawn "Red Angry Bird" with dynamic rotation physics.
- **Physics-Based Gameplay** - Realistic gravity, velocity, and collision detection systems for authentic arcade feel.
- **Cross-Platform Web Play** - Runs directly in the browser at 60 FPS using WebAssembly technology.
- **Responsive Controls** - Intelligent input handling supporting both Keyboard (Space) and Touch (Tap) for mobile devices.
- **Dynamic Environment** - Moving clouds, parallax scrolling ground, and randomized pipe generation.
- **Deployment Ready** - Fully configured with a Flask wrapper and Gunicorn for enterprise-grade web hosting.

---

### Game Interaction
| Feature | Action | Experience |
|---------|--------|------------|
| **Start Game** | Press `SPACE` or Tap | The bird leaps into action, activating gravity and physics immediately |
| **Flight Control** | Press `SPACE` or Tap | The bird flaps upwards with an angular rotation animation mimicking flight |
| **System** | `R` Key or Click after death | Instantly resets the game state for rapid replayability |

### Engineering Highlights
- **Core Engine**: Built on **Python 3** and **Pygame Community Edition** for robust game loops and rendering.
- **Web Porting**: Utilizes **Pygbag** to compile Python bytecode to WebAssembly (Wasm) for browser execution.
- **Rendering**: Custom geometric drawing algorithms for the bird and environment (no static image assets used).
- **Backend wrapper**: References a lightweight **Flask** server to serve the Wasm assets efficiently in production.

---

## Future Enhancements
Ideas for the next version:
- [ ] **Leaderboard System** - Global high scores using a lightweight cloud database
- [ ] **Power-ups** - Shield or speed boost collectibles
- [ ] **Difficulty scaling** - Pipes moving faster as score increases
- [ ] **Skin Store** - Unlockable birds (Blue, Yellow) based on score milestones
- [ ] **Sound Effects** - 8-bit retro audio integration

---

## License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for full details.

---

## Acknowledgments
Special recognition to:
- **My professors at VIT Vellore** for their encouragement in exploring diverse tech stacks.
- **IIT Madras coursework** for emphasizing algorithmic efficiency.
- **The Pygame Community** for maintaining the excellent library.
- **Pygbag Developers** for enabling Python on the web.

---

## About the Developer

**Yuvraj Chopra**  
*B.Tech Computer Science Engineering - VIT Vellore*  
*B.S. Data Science - IIT Madras*  
Vellore, Tamil Nadu, India

*Passionate about building simple, effective solutions to everyday problems. Currently exploring the intersection of software engineering and data science.*

### Connect With Me

[![GitHub](https://img.shields.io/badge/GitHub-chopra--yuvraj-181717?style=for-the-badge&logo=github)](https://github.com/chopra-yuvraj)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-chopra--yuvraj-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/chopra-yuvraj)
[![Email](https://img.shields.io/badge/Email-yuvrajchopra19%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:yuvrajchopra19@gmail.com)

---

<div align="center">

**Made with ❤️ and ☕ by Yuvraj Chopra**

[ **View on GitHub**](https://github.com/chopra-yuvraj/flappy-angry-bird)

</div>
