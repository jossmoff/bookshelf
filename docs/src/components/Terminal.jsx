import React from 'react';
import Terminal, { ColorMode, TerminalOutput } from 'react-terminal-ui';

export default function BookshelfTerminal() {
  // Terminal has 100% width by default so it should usually be wrapped in a container div
  return (
    <div className="container" style={{ width: '90%' }}>
      <Terminal name='' colorMode={ ColorMode.Dark } startingInputValue={'bookshelf create'} >
        <TerminalOutput>
        `╭───────────────── 📖 Story 📖 ──────────────────╮
         │ <b>✏️ Name:</b>                                       │
         │   example-story                                │
         │ <b>🗓️ Start Date:</b>                                 │
         │   22/10/2023                                   │
         │ <b>⏱️ Elapsed Time:</b>                               │
         │   0 hours, 0 minutes, 0 seconds                │
         │ <b>🏷️ Tags:</b>                                       │
         │   []                                           │
         │                                                │
         │ [Press <b>CTRL+C</b> to exit]                         │
         ╰────────────────────────────────────────────────╯`
        </TerminalOutput>
      </Terminal>
    </div>
  )
};