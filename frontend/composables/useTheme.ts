type Theme = 'light' | 'dark'

const STORAGE_KEY = 'minicargoflow-theme'

export const useTheme = () => {
  const theme = useState<Theme>('mini-cargoflow-theme', () => 'light')

  const setTheme = (value: Theme) => {
    theme.value = value

    if (import.meta.client) {
      document.documentElement.classList.toggle('dark', value === 'dark')
      window.localStorage.setItem(STORAGE_KEY, value)
    }
  }

  const toggle = () => setTheme(theme.value === 'dark' ? 'light' : 'dark')

  const init = () => {
    if (!import.meta.client) return

    const stored = window.localStorage.getItem(STORAGE_KEY)
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    setTheme(stored === 'dark' || stored === 'light' ? stored : prefersDark ? 'dark' : 'light')
  }

  return { theme, setTheme, toggle, init }
}
