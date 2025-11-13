import { useEffect } from 'react'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'next/navigation'

export function useAuth() {
  const router = useRouter()
  const { user, token, isAuthenticated, isLoading, error, login, logout, fetchUser, clearError } =
    useAuthStore()

  useEffect(() => {
    if (token && !user) {
      fetchUser()
    }
  }, [token, user, fetchUser])

  const requireAuth = () => {
    if (!isAuthenticated) {
      router.push('/login')
      return false
    }
    return true
  }

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    fetchUser,
    clearError,
    requireAuth,
  }
}
