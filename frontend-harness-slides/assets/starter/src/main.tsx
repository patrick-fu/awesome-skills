import React from 'react';
import ReactDOM from 'react-dom/client';
import { SlideDeck } from './SlideDeck';
import { exposeRegistryForTooling } from './SlideRegistry';
import './index.css';

// Publish a slim registry on window so the Playwright harness knows which scenes exist and how many
// beats each has — a single source of truth.
exposeRegistryForTooling();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <SlideDeck />
  </React.StrictMode>,
);
