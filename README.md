# 🎓 Quiz Master — Advanced Python Quiz Application

A polished, fully object-oriented desktop quiz application built with **Python 3** and **Tkinter (ttk)**. Players log in, choose a category, race a 20-second countdown per question, and see their results, leaderboard ranking, and full score history — all backed by JSON storage.

---

## ✨ Features

- **Login screen** with name validation
- **Home menu** with Start Quiz, Leaderboard, Score History, Add Questions, and Exit
- **4 quiz categories** (Python, General Knowledge, Science, Mathematics), 15+ questions each
- **Randomized** question order and option order every game
- **20-second countdown timer** per question with auto-advance on timeout
- **Instant feedback**: green for correct, red for wrong, then auto-advance
- **Live scoring**: current score, correct/wrong counts, percentage
- **Result screen** with final score, grade (A+ / A / B / C / Fail), and a motivational quote
- **Leaderboard** — Top 10 scores, persisted in `data/leaderboard.json`, with a reset option
- **Score History** — every attempt logged to `data/history.json`, with search-by-player, delete single entries, clear all, and **CSV export**
- **Add Questions screen** — add new questions to any category with validation against empty fields and duplicates
- **Light / Dark mode toggle**
- **Full-screen mode** (F11 to toggle, Esc to exit)
- **Pause / Resume** during a quiz
- **Hover effects**, progress bar, and a modern ttk-based interface
- **Graceful error handling** — missing or corrupted JSON files are automatically recreated

---

## 🗂 Project Structure

```
Quiz_App/
│
├── main.py                  # Entry point / QuizApp controller
├── questions/                # One JSON file per category
│   ├── python.json
│   ├── science.json
│   ├── maths.json
│   └── gk.json
├── data/
│   ├── leaderboard.json      # Auto-created if missing
│   └── history.json          # Auto-created if missing
├── models/                   # Non-UI logic (OOP core)
│   ├── question_manager.py   # QuestionManager
│   ├── timer.py               # Timer
│   ├── score_manager.py       # ScoreManager
│   ├── leaderboard.py         # Leaderboard
│   └── history_manager.py     # HistoryManager
├── ui/                        # Tkinter screens
│   ├── login_page.py          # LoginPage
│   ├── home_page.py           # HomePage
│   ├── quiz_page.py            # QuizSetupPage + QuizPage
│   ├── result_page.py          # ResultPage
│   ├── leaderboard_page.py     # LeaderboardPage
│   ├── history_page.py         # HistoryPage
│   └── question_editor.py      # QuestionEditorPage
├── utils/
│   └── helpers.py              # JSON I/O, theming, grading, quotes, CSV export
└── assets/                     # Icons / logo (optional)
```

### Object-Oriented Design

| Class | File | Responsibility |
|---|---|---|
| `QuizApp` | `main.py` | Root Tk window, frame navigation, shared state |
| `LoginPage` | `ui/login_page.py` | Name entry & validation |
| `HomePage` | `ui/home_page.py` | Main menu |
| `QuizSetupPage` / `QuizPage` | `ui/quiz_page.py` | Category picker & live quiz screen |
| `QuestionManager` | `models/question_manager.py` | Loads/shuffles/adds questions |
| `Timer` | `models/timer.py` | 20-second countdown logic |
| `ScoreManager` | `models/score_manager.py` | Score/correct/wrong/percentage tracking |
| `Leaderboard` | `models/leaderboard.py` | Top-10 persistence |
| `HistoryManager` | `models/history_manager.py` | Attempt history, search, delete, CSV export |
| `ResultPage` | `ui/result_page.py` | Post-quiz summary & grading |
| `QuestionEditorPage` | `ui/question_editor.py` | Add-question form with validation |

No global variables are used — all state lives on `QuizApp` or the relevant manager instance, passed around via the `controller` reference each frame holds.

---

## 🛠 Requirements

- **Python 3.8+**
- **Tkinter** (bundled with most Python installations; on Linux you may need to install it separately)

No third-party pip packages are required — everything uses the Python standard library (`tkinter`, `json`, `csv`, `random`, `datetime`, `os`).

### Installing Tkinter (if missing)

```bash
# Debian/Ubuntu
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (Homebrew Python usually includes Tk already)
brew install python-tk
```

---

## ▶️ How to Run

1. Download or clone the `Quiz_App/` folder.
2. Open a terminal inside the folder.
3. Run:

```bash
python main.py
```

(On some systems the command is `python3 main.py`.)

The app will:
- Auto-create `data/leaderboard.json` and `data/history.json` if they don't exist
- Auto-create the `questions/` folder if missing (though question files ship with the app)
- Open on the Login screen

---

## 🎮 How to Play

1. **Enter your name** on the login screen and press **Continue**.
2. From the **Home** screen, click **Start Quiz**.
3. Pick one of the four **categories**.
4. Answer each question before the **20-second timer** runs out — options and question order are shuffled every game.
5. See instant **green/red** feedback, then the app auto-advances.
6. At the end, view your **Score, Grade, Correct/Wrong count, and Percentage**.
7. Check your ranking on the **Leaderboard**, or review past attempts in **Score History** (with search, delete, and CSV export).
8. Use **Add Questions** to contribute new questions to any category.
9. Toggle **🌙 Dark Mode** or **⛶ Fullscreen** from the Home screen at any time.

---

## 📸 Screenshots

> Screenshots are best captured after first run on your machine (Tkinter UI appearance varies slightly by OS). Suggested shots to include here:
> - Login screen
> - Home menu
> - Quiz screen mid-question (timer + options)
> - Result screen with grade
> - Leaderboard
> - Score History
> - Add Questions form
> - Dark mode view

---

## 🧩 Extending the App

- **Add a new category**: add an entry to `QuestionManager.CATEGORY_FILES` in `models/question_manager.py` and drop a matching JSON file into `questions/`.
- **Change question count per game**: currently all questions in a category are used per attempt; slice the list in `QuizPage.start()` if you want a fixed subset (e.g., `questions[:10]`).
- **Adjust timer length**: change `QUESTION_TIME_SECONDS` in `ui/quiz_page.py`.
- **Sounds**: `QuizApp.play_sound()` uses `winsound` on Windows and a terminal bell elsewhere as a lightweight, dependency-free stand-in — swap in a library like `playsound` or `pygame.mixer` for richer audio.

---

## ⚠️ Error Handling Notes

- All JSON reads/writes go through `utils/helpers.py`, which auto-creates missing files with sensible defaults and resets corrupted JSON rather than crashing.
- Adding a question validates against empty fields, incomplete options, and duplicate question text (case-insensitive) within the same category.
- The login screen blocks empty names before proceeding.

---

## 📄 License

This project is provided as-is for educational and personal use.
