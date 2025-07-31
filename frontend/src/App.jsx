import { useState } from 'react'
import './App.css'
import StoryGenerator from './components/StoryGenerator'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>AutoDevHub Story Generator</h1>
        <p>Generate compelling user stories for your development projects</p>
      </header>
      <main className="app-main">
        <StoryGenerator />
      </main>
      <footer className="app-footer">
        <p>© 2025 AutoDevHub - AI-Powered Development Tools</p>
      </footer>
    </div>
  )
}

export default App
