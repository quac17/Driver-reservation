# Drive Coach Reservation - Frontend (Next.js + TypeScript)

This is a starter Next.js (App Router, v14) + TypeScript + Ant Design frontend for the Drive Coach Reservation API. It provides a minimal authentication flow (login -> dashboard) and an API helper.

Quick start (Windows PowerShell):

```powershell
cd Client
npm install
npm run dev
```

App will be available at `http://localhost:3000`.

Notes:
- Login sends `application/x-www-form-urlencoded` POST to `/authen/login` on the API (default `http://localhost:8000`).
- After successful login, `access_token` is stored in `localStorage` and `loginData` is saved from the response.
- You can change the API base URL by setting environment variable `NEXT_PUBLIC_API_BASE` before running.

Files of interest:
- `app/login/page.tsx` — login page (client)
- `app/dashboard/page.tsx` — simple dashboard showing saved profile
- `components/LoginForm.tsx` — Ant Design form to login
- `lib/api.ts` — axios helper with `login()` helper

Next steps I can implement for you:
- Add registration page and `POST /user/` flow
- Implement reserves list and create-reserve UI
- Add role-based UI for Mentor vs User
