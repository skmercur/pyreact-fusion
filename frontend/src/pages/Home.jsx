import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import { isAuthenticated } from '../utils/auth'

function Home() {
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const authenticated = isAuthenticated()

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await api.health()
        setHealth(response.data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    checkHealth()
  }, [])

  return (
    <div className="px-4 py-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          {health?.app_name || 'Welcome to PyReact Fusion'}
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-4">
          {health?.app_name ? 
            (health.app_description || 'A production-ready full-stack application') :
            'A production-ready full-stack application template'
          }
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">
          Created by{' '}
          <a
            href="https://github.com/skmercur"
            target="_blank"
            rel="noopener noreferrer"
            className="text-primary-600 dark:text-primary-400 hover:underline"
          >
            Sofiane Khoudour
          </a>
        </p>

        {loading && (
          <div className="flex justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            Error: {error}
          </div>
        )}

        {health && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            <p className="font-semibold">Status: {health.status}</p>
            {health.app_name && <p>App: {health.app_name} v{health.app_version || ''}</p>}
            <p>Environment: {health.environment}</p>
            <p>Database: {health.database}</p>
            {health.mode && <p>Mode: {health.mode}</p>}
          </div>
        )}

        <div className="mt-8 space-x-4">
          {!authenticated ? (
            <>
              <Link
                to="/register"
                className="inline-block px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Get Started
              </Link>
              <Link
                to="/login"
                className="inline-block px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Login
              </Link>
            </>
          ) : (
            <Link
              to="/dashboard"
              className="inline-block px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              Go to Dashboard
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}

export default Home

