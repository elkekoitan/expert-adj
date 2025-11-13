# 🎨 Frontend Quick Setup Guide

## Durum: Temel Altyapı Hazır

### ✅ Tamamlanan
1. shadcn/ui dependencies kuruldu
2. Dizin yapısı oluşturuldu:
   - `frontend/components/ui/` - shadcn components
   - `frontend/stores/` - Zustand stores  
   - `frontend/hooks/` - Custom hooks
3. Utils fonksiyonu (`cn`) eklendi

### 📦 Kurulu Paketler
```json
{
  "class-variance-authority": "^0.7.0",
  "clsx": "^2.0.0", 
  "tailwind-merge": "^2.0.0",
  "lucide-react": "^0.294.0",
  "@radix-ui/react-slot": "^1.0.2"
}
```

### 🔄 Sonraki Adımlar (30-60 dakika)

#### 1. Tailwind Config Güncelle
`frontend/tailwind.config.ts` dosyasını `FRONTEND_ARCHITECTURE_MASTERPLAN.md` Line 299-397'den kopyala.

Design tokens ekle:
- Colors (profit, loss, neutral)
- Animations (fade-in, slide-up)
- Custom theme variables

#### 2. Global Styles Güncelle  
`frontend/app/globals.css` dosyasını Line 409-494'ten kopyala.

CSS variables ekle:
- Light/dark mode colors
- Custom scrollbar styles

#### 3. Zustand Stores Oluştur

**Auth Store** (`frontend/stores/authStore.ts`):
```typescript
// Line 554-670'den kopyala
interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}
```

**UI Store** (`frontend/stores/uiStore.ts`):
```typescript  
// Line 679-735'ten kopyala
interface UIState {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  toggleSidebar: () => void
}
```

#### 4. React Query Setup

**Query Client** (`frontend/lib/queryClient.ts`):
```typescript
// Line 861-875'ten kopyala
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      retry: 1
    }
  }
})
```

#### 5. Base Components Oluştur

Aşağıdaki komutlarla shadcn components ekle:

```bash
cd frontend

# Core components
npx shadcn@latest add button
npx shadcn@latest add card  
npx shadcn@latest add input
npx shadcn@latest add label
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add table
npx shadcn@latest add tabs
npx shadcn@latest add badge
npx shadcn@latest add alert
```

#### 6. Layout Components

**Header** (`frontend/components/layout/Header.tsx`):
- Logo
- User menu
- Theme toggle
- Command palette trigger

**Sidebar** (`frontend/components/layout/Sidebar.tsx`):
- Navigation links
- Collapsible
- Active state highlighting

#### 7. Providers Setup

**Root Providers** (`frontend/app/providers.tsx`):
```typescript
'use client'

import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '@/lib/queryClient'

export function Providers({ children }: { children: React.Node }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

**Root Layout Güncelle** (`frontend/app/layout.tsx`):
```typescript
import { Providers } from './providers'

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
```

#### 8. Login Page Refactor

`frontend/app/login/page.tsx` dosyasını Line 2245-2387'den refactor et:
- React Hook Form + Zod validation
- Auth store integration
- Loading states
- Error handling

### 🎯 Hızlı Başlangıç Komutu

```bash
cd C:\Users\qw\Desktop\expert-adj\frontend

# Components ekle (tek komutta)
npx shadcn@latest add button card input label dialog table badge alert

# Development server başlat  
npm run dev
```

### 📊 İlerleme Takibi

- [ ] Tailwind config güncellendi
- [ ] Global styles eklendi
- [ ] Auth store oluşturuldu
- [ ] UI store oluşturuldu
- [ ] Query client setup
- [ ] Base components eklendi
- [ ] Layout components oluşturuldu
- [ ] Providers setup
- [ ] Login page refactor

### 💡 İpuçları

1. **Masterplan'ı Referans Alın**: Tüm kod örnekleri `FRONTEND_ARCHITECTURE_MASTERPLAN.md`'de mevcut
2. **Önce Test Edin**: Her component'i oluşturduktan sonra `npm run dev` ile test edin
3. **Type Safety**: TypeScript strict mode'da çalışın
4. **Incremental**: Her adımı tamamlayıp commit edin

### 🚀 Sonraki Oturum Hedefleri

1. **Real-time Features** (Week 5-6):
   - WebSocket integration
   - Live backtest progress
   - Real-time trade updates

2. **AI Features** (Week 7-8):
   - Risk Meter component
   - AI Recommendations
   - Predictive charts

3. **3D Visualization** (Week 9-10):
   - React Three Fiber setup
   - 3D Equity curves
   - Parameter heatmaps

### 📁 Dosya Yapısı

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── providers.tsx       # Query + other providers
│   ├── login/page.tsx      # Login page (refactored)
│   └── dashboard/page.tsx  # Dashboard (refactored)
├── components/
│   ├── ui/                 # shadcn components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── ...
│   └── layout/             # Layout components
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── PageHeader.tsx
├── stores/
│   ├── authStore.ts        # Auth state
│   ├── uiStore.ts          # UI state
│   └── notificationStore.ts
├── hooks/
│   ├── useWebSocket.ts     # WebSocket hook
│   └── useBacktests.ts     # Query hooks
├── lib/
│   ├── utils.ts            # cn() utility
│   ├── queryClient.ts      # React Query config
│   └── api.ts              # API client
└── types/
    └── index.ts            # Shared types
```

### 🔗 Kaynaklar

- **Masterplan**: `docs/FRONTEND_ARCHITECTURE_MASTERPLAN.md`
- **shadcn/ui Docs**: https://ui.shadcn.com
- **Tailwind Docs**: https://tailwindcss.com
- **Zustand Docs**: https://zustand-demo.pmnd.rs
- **React Query Docs**: https://tanstack.com/query

---

**Hazırlayan**: Claude (2025-11-13)  
**Durum**: Altyapı Hazır, Implementation Başlayabilir  
**Tahmini Süre**: 2-3 saat (temel features için)
