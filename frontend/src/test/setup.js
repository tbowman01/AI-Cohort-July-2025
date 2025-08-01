import '@testing-library/jest-dom'
import { beforeAll, afterEach, afterAll, vi } from 'vitest'
import { cleanup } from '@testing-library/react'
import { server } from './mocks/server'

// Import fetch polyfill
import 'whatwg-fetch'

// Setup MSW - must be before any fetch polyfills
beforeAll(() => {
  server.listen({ 
    onUnhandledRequest: (req, print) => {
      // Log unhandled requests for debugging
      console.error(`Unhandled ${req.method} request to ${req.url}`)
      print.error()
    }
  })
})
afterEach(() => {
  cleanup()
  server.resetHandlers()
})
afterAll(() => server.close())

// Mock environment variables
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock import.meta.env
Object.defineProperty(import.meta, 'env', {
  value: {
    VITE_API_BASE_URL: 'http://localhost:8000',
    VITE_API_ENDPOINT: '/api/v1/stories/generate'
  },
  writable: true
})

// Global test setup
global.vi = vi