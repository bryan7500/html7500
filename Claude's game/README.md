# STAR BLASTER — NES-style 8-bit shooter

Open `index.html` in a browser (Chrome, Edge, Firefox, Safari). No install or build step.
If your browser blocks audio from `file://`, run `python3 -m http.server` in this folder and open http://localhost:8000.

## Controls
| Action | Keyboard | Other |
|---|---|---|
| Move | Arrows / A-D | Gamepad stick or D-pad; touch: drag |
| Fire | Space / Z / Up | Gamepad A; touch: auto-fire while touching |
| Start | Enter | Tap / gamepad Start |
| Pause / Mute | P (or Esc) / M | Game auto-pauses when the window loses focus |

## Gameplay
- 256x240 NES resolution, 16x16 sprites, 3 lives (extra life every 2000 points, max 5).
- Enemies: blue beast = 10, purple bat = 20 (aims shots), green gello = 30 (top row). From wave 3 enemies dive-bomb you.
- Every 5th wave is a boss fight (boss gets tougher each time).
- Shot-down enemies sometimes drop a coin: collect it for 10 seconds of triple shot. Getting hit loses the power-up.
- Reach the bottom and it's game over. High score is saved in your browser.

## Files
- `index.html` — the whole game (canvas + JS).
- `assets/sprites/` — CC0 art; `assets/audio/` — SFX and music. Credits and licenses: `assets/ASSET_CREDITS.md`.
