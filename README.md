KBC-Style Quiz Game

This project is a real-time, multiplayer quiz game inspired by the popular TV show "Kaun Banega Crorepati" (KBC). It uses FastAPI for the backend, WebSockets for real-time communication, and HTML/JavaScript for the frontend.

Repository: [@https://github.com/Vaibhavbasidoni/KBC](https://github.com/Vaibhavbasidoni/KBC)

Features

- Host screen displays questions and QR code for players to join
- Players can join by scanning the QR code or accessing a URL
- Real-time question updates and answer submission
- Immediate feedback for correct and incorrect answers
- Automatic progression to the next question after a correct answer

Technologies Used

- Backend: FastAPI (Python)
- Frontend: HTML, JavaScript
- Real-time Communication: WebSockets
- QR Code Generation: qrcode library

Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/Vaibhavbasidoni/KBC.git
   cd KBC
   ```

2. Install the required dependencies:
   ```
   pip install fastapi uvicorn websockets qrcode pillow
   ```

3. Run the application:
   ```
   python main.py
   ```

4. Access the game:
   - Host screen: Open `http://localhost:8002/host` in a web browser
   - Player screen: Scan the QR code on the host screen or open `http://localhost:8002/static/player.html`

How to Play

1. The host opens the host screen, which displays the current question and a QR code.
2. Players join by scanning the QR code or accessing the player URL.
3. Players enter their names to join the game.
4. The current question is displayed on both the host and player screens.
5. Players submit their answers.
6. For correct answers:
   - A congratulatory message is shown on the host screen.
   - The game automatically moves to the next question after a short delay.
7. For incorrect answers:
   - Players receive a message indicating their answer was wrong.
   - They can try again until someone answers correctly.

Project Structure

- `main.py`: FastAPI backend server
- `static/host.html`: Host screen frontend
- `static/player.html`: Player screen frontend

Customization

You can customize the game by modifying the questions in the `main.py` file. Add, remove, or change questions as needed.

Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

License

This project is open source and available under the [MIT License](LICENSE).
