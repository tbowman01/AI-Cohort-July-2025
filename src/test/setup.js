// Test setup for Vitest
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

// Extend Vitest's expect with Testing Library matchers
expect.extend(matchers)

// Clean up after each test case
afterEach(() => {
  cleanup()
})

// Mock environment variables for tests
process.env.NODE_ENV = 'test'

// Global test configuration
global.IS_REACT_ACT_ENVIRONMENT = true