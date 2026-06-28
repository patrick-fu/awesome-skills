import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// The Playwright harness drives the production `preview` server. Keep its port overridable so a busy
// 4173 (e.g. another Vite app) is escapable: `PORT=4180 npm test` moves preview + specs together.
const PORT = Number(process.env.PORT) || 4173;

export default defineConfig({
  plugins: [react()],
  preview: { port: PORT, strictPort: true },
});
