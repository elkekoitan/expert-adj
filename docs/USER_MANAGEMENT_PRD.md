# 👥 User Management & Social Trading Platform - PRD

> **Product Requirements Document**
> Version: 2.0
> Date: November 10, 2025
> Author: MT Expert Optimizer Team

---

## 📋 Executive Summary

This document outlines the comprehensive user management, social trading, and admin dashboard system for MT Expert Optimizer. The system enables users to manage their trading strategies, share configurations, collaborate with other traders, and provides administrators with powerful analytics and user management capabilities.

### Goals
- ✅ **World-class user management** with Google OAuth integration
- ✅ **Social trading features** for parameter sharing and collaboration
- ✅ **Comprehensive admin dashboard** for platform oversight
- ✅ **Role-based access control** with granular permissions
- ✅ **Analytics and reporting** for informed decision-making
- ✅ **Secure and compliant** with industry best practices

---

## 🔍 Rakip Analizi (Competitive Analysis)

### Analiz Edilen Platformlar

#### 1. MQL5.com Community & Market
**Güçlü Yönler:**
- Signal marketplace with 10,000+ trading signals
- User ratings and reviews for EAs
- Subscription-based signal following
- Detailed performance metrics display
- Cross-server social trading capability

**Zayıf Yönler:**
- Complicated UI/UX for beginners
- Limited parameter customization visibility
- No direct EA configuration sharing
- Weak community interaction features

#### 2. TradingView Social Platform
**Güçlü Yönler:**
- Excellent social features (follow, comment, share)
- Script sharing with public/private options
- Reputation system (followers, likes)
- Clean, modern UI
- Real-time collaboration features

**Zayıf Yönler:**
- Not MT4/MT5 specific
- Limited automated trading integration
- No direct backtesting on platform

#### 3. ZuluTrade & eToro Copy Trading
**Güçlü Yönler:**
- One-click copy trading
- Detailed trader statistics
- Risk management controls
- Social feed and interaction
- Mobile-first design

**Zayıf Yönler:**
- Closed ecosystem
- Limited customization
- High fees
- No EA development tools

### 🎯 Bizim Avantajımız (Our Competitive Advantage)

1. **EA Parameter Sharing** - First platform to enable detailed EA configuration sharing
2. **Hybrid Approach** - Combines social trading + automated optimization + backtesting
3. **Open Ecosystem** - Users own their EAs and data
4. **Free to Start** - No subscription for basic features
5. **Developer-Friendly** - API-first design, extensible architecture
6. **Real-time Collaboration** - Live chat, shared workspaces
7. **Advanced Analytics** - ML-powered insights and recommendations

---

## 🏗️ Sistem Mimarisi (System Architecture)

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   User App   │  │ Admin Panel  │  │  Public Marketplace  │  │
│  │   (Next.js)  │  │   (React)    │  │     (Next.js)        │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼──────────────────┼──────────────────────┼─────────────┘
          │                  │                      │
          └──────────────────┴──────────────────────┘
                             │
          ┌──────────────────▼───────────────────────────────┐
          │            API GATEWAY (Kong/Nginx)              │
          │        Rate Limiting, Auth, Load Balancing       │
          └──────────────────┬───────────────────────────────┘
                             │
          ┌──────────────────▼───────────────────────────────┐
          │              AUTHENTICATION SERVICE               │
          │   JWT, OAuth2, Session Management, RBAC          │
          └──────────────────┬───────────────────────────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
┌───────▼────────┐                    ┌──────────▼──────────┐
│  USER SERVICE  │                    │   SOCIAL SERVICE     │
│                │                    │                      │
│ - Profiles     │◄──────────────────►│ - Comments           │
│ - Settings     │                    │ - Likes/Favorites    │
│ - Preferences  │                    │ - Sharing            │
│ - Permissions  │                    │ - Following          │
└───────┬────────┘                    └──────────┬──────────┘
        │                                        │
        └────────────────────┬───────────────────┘
                             │
        ┌────────────────────▼───────────────────────────────┐
        │                  CORE SERVICES                      │
        │  ┌───────────┐  ┌──────────┐  ┌─────────────────┐ │
        │  │ EA Store  │  │ Backtest │  │  Optimization   │ │
        │  │ Service   │  │ Service  │  │    Service      │ │
        │  └───────────┘  └──────────┘  └─────────────────┘ │
        └────────────────────┬───────────────────────────────┘
                             │
        ┌────────────────────▼───────────────────────────────┐
        │                  DATA LAYER                         │
        │  ┌──────────────┐  ┌──────────┐  ┌──────────────┐ │
        │  │  PostgreSQL  │  │  Redis   │  │  Elasticsearch│ │
        │  │  (Primary)   │  │  (Cache) │  │    (Search)   │ │
        │  └──────────────┘  └──────────┘  └──────────────┘ │
        └─────────────────────────────────────────────────────┘
```

---

## 💎 Özellik Detayları (Feature Details)

### 1. 🔐 Gelişmiş Kullanıcı Yönetimi (Advanced User Management)

#### 1.1 Authentication Methods

**Email/Password Registration**
- Strong password requirements (min 12 chars, uppercase, lowercase, number, symbol)
- Email verification with 24-hour expiry
- Password reset via email with token
- Account lockout after 5 failed attempts (15-minute cooldown)

**Google OAuth 2.0**
```python
# Implementation approach
- OAuth2 flow with PKCE (Proof Key for Code Exchange)
- Automatic account creation on first login
- Profile sync (name, email, avatar)
- Revokable access tokens
- Support for multiple Google accounts per user
```

**Two-Factor Authentication (2FA)**
- TOTP-based (Google Authenticator, Authy)
- Backup codes (10 single-use codes)
- SMS 2FA (optional, via Twilio)
- Recovery email option

#### 1.2 User Profiles

**Basic Information**
- Full name, username (unique)
- Email (verified)
- Phone (optional)
- Country/timezone
- Language preference
- Avatar (uploadable or Gravatar)

**Trading Information**
- Trading experience level (Beginner, Intermediate, Advanced, Expert)
- Preferred markets (Forex, Crypto, Stocks, Commodities)
- Risk tolerance (Low, Medium, High)
- Trading style (Scalper, Day Trader, Swing Trader, Position Trader)
- Broker accounts linked

**Social Profile**
- Bio (500 chars)
- Website/social links
- Verification badge (verified traders)
- Public/private profile toggle
- Activity status (online/offline)

**Statistics**
- Member since date
- Total EAs uploaded
- Total backtests run
- Shared configurations count
- Followers count
- Following count
- Total likes received
- Reputation score (0-1000)

#### 1.3 User Settings

**Privacy Settings**
```yaml
Profile Visibility:
  - Public: Anyone can see
  - Followers Only: Only people who follow you
  - Private: Only you

EA Library Visibility:
  - All EAs public
  - Selected EAs public
  - All EAs private

Activity Visibility:
  - Show recent activity
  - Hide activity from profile
  - Show to followers only

Search Visibility:
  - Appear in search results
  - Hide from public search
```

**Notification Settings**
```yaml
Email Notifications:
  - New follower
  - Comment on my EA
  - Someone liked my configuration
  - Reply to my comment
  - Optimization completed
  - Backtest finished
  - Trading account alert

In-App Notifications:
  - Real-time notifications
  - Desktop notifications
  - Sound alerts

Frequency:
  - Instant
  - Daily digest
  - Weekly summary
  - Never
```

**Security Settings**
- Change password
- Enable/disable 2FA
- Manage OAuth connections
- Active sessions viewer
- Login history (last 30 days)
- Download personal data (GDPR)
- Delete account (with 30-day grace period)

#### 1.4 Role-Based Access Control (RBAC)

**User Roles**

1. **Guest** (Unauthenticated)
   - View public EAs
   - View public marketplace
   - View public profiles
   - Read public comments

2. **User** (Free Tier)
   - Upload 3 EAs
   - Run 10 backtests/day
   - 1 optimization session/day
   - Share configurations (public/private)
   - Follow users
   - Comment and like
   - Connect 1 demo account

3. **Pro User** (Paid Tier - $29/month)
   - Upload unlimited EAs
   - Unlimited backtests
   - Unlimited optimizations
   - Priority processing
   - Connect 3 demo accounts
   - Advanced analytics
   - Private workspaces
   - API access

4. **Enterprise User** (Custom)
   - All Pro features
   - Custom worker allocation
   - Dedicated support
   - White-label option
   - On-premise deployment
   - SLA guarantees

5. **Moderator**
   - All User features
   - Review reported content
   - Hide inappropriate comments
   - Ban users (temporary)
   - Edit public EA descriptions

6. **Admin**
   - All platform access
   - User management (create, edit, delete, ban)
   - System configuration
   - View all analytics
   - Access logs and audits
   - Billing management
   - Feature flags control

**Permission Matrix**

```typescript
interface Permission {
  resource: string;
  actions: ('create' | 'read' | 'update' | 'delete' | 'execute')[];
}

const PERMISSIONS: Record<Role, Permission[]> = {
  guest: [
    { resource: 'ea', actions: ['read'] },
    { resource: 'profile', actions: ['read'] },
  ],
  user: [
    { resource: 'ea', actions: ['create', 'read', 'update', 'delete'] },
    { resource: 'backtest', actions: ['create', 'read', 'execute'] },
    { resource: 'optimization', actions: ['create', 'read', 'execute'] },
    { resource: 'profile', actions: ['read', 'update'] },
    { resource: 'comment', actions: ['create', 'read', 'update', 'delete'] },
  ],
  pro_user: [/* all user permissions plus */
    { resource: 'api', actions: ['create', 'read', 'update', 'delete'] },
    { resource: 'workspace', actions: ['create', 'read', 'update', 'delete'] },
  ],
  admin: [
    { resource: '*', actions: ['*'] }, // Full access
  ],
};
```

---

### 2. 🤝 Sosyal Özellikler (Social Features)

#### 2.1 EA Sharing & Marketplace

**EA Upload**
```yaml
Upload Types:
  - Compiled file (.ex4, .ex5)
  - Source code (.mq4, .mq5) - optional
  - Documentation (PDF, MD)
  - Screenshots (up to 5)
  - Backtest reports

Metadata:
  - Name and description
  - Category (Trend, Scalper, Grid, Martingale, etc.)
  - Tags (max 10)
  - Platform (MT4, MT5, Both)
  - Version number
  - License type (Free, Paid, Open Source)
  - Price (if paid)
  - Changelog

Visibility:
  - Public: Anyone can see and download
  - Unlisted: Only with link
  - Private: Only you
  - Followers Only: Only your followers
```

**EA Discovery**
- Search by name, tags, description
- Filter by:
  - Platform (MT4/MT5)
  - Category
  - Price range
  - Rating
  - Upload date
  - Most downloaded
  - Most liked
  - Best performing
- Sort by: Relevance, Date, Rating, Downloads, Price

**EA Detail Page**
```yaml
Sections:
  Overview:
    - Name, version, author
    - Description
    - Screenshots
    - Video demo (YouTube embed)
    - Tags

  Performance:
    - Average backtest results
    - Win rate distribution
    - Risk metrics
    - Equity curve

  Parameters:
    - Input parameters list
    - Recommended ranges
    - Optimization results

  Reviews:
    - User ratings (1-5 stars)
    - Written reviews
    - Verified purchaser badge

  Configurations:
    - Shared parameter sets
    - Popular configurations
    - Top performing settings

  Comments:
    - Discussion thread
    - Q&A section
    - Author responses highlighted

  Related:
    - Similar EAs
    - Same author
    - Often downloaded together
```

#### 2.2 Configuration Sharing

**Share Configuration**
```python
# User can share:
- EA parameters (JSON)
- Symbol and timeframe
- Backtest period
- Broker settings
- Risk management settings
- Optimization results

# Sharing options:
- Public (appears in marketplace)
- Link only (unlisted)
- Specific users (private)
- Export as file (.set, .ini, .json)
```

**Configuration Marketplace**
- Browse shared configurations
- Filter by EA, symbol, timeframe
- Sort by performance metrics
- One-click import to your EA
- Fork and modify configurations
- Version history
- Compare configurations side-by-side

**Configuration Detail Page**
```yaml
Information:
  - Configuration name
  - Author and upload date
  - Associated EA
  - Symbol and timeframe
  - Backtest period

Performance:
  - Backtest results
  - Key metrics (profit factor, drawdown, etc.)
  - Equity curve
  - Trade analysis

Parameters:
  - Full parameter list
  - Highlighted changes from default
  - Parameter importance (ML-based)

Usage:
  - Import button (one-click)
  - Download as .set file
  - Fork and modify
  - Add to favorites

Social:
  - Likes count
  - Comments
  - Times imported
  - Ratings
```

#### 2.3 Social Interactions

**Following System**
- Follow users to see their activity
- Get notifications for their new EAs/configs
- Followers/following counts on profile
- Mutual follow detection
- Follow suggestions based on:
  - Similar trading style
  - Same markets
  - Mutual followers
  - Popular in your region

**Comments & Discussions**
```yaml
Comment Features:
  - Markdown support
  - Code snippets
  - Image attachments
  - @mentions
  - Reply threading (nested)
  - Emoji reactions
  - Edit history
  - Report inappropriate content

Moderation:
  - Auto-hide spam (ML-based)
  - User can block others
  - Moderator review queue
  - Strike system (3 strikes = ban)
```

**Likes & Favorites**
- Like EAs, configurations, comments
- Favorite EAs for quick access
- Like count displayed publicly
- Private favorite collections
- Share favorite collections

**Activity Feed**
```yaml
User sees:
  - EAs uploaded by followed users
  - Configurations shared by followed users
  - Comments on their EAs
  - Likes on their content
  - Achievements unlocked
  - Optimization milestones

Feed Filters:
  - All activity
  - Only uploads
  - Only comments
  - Only from specific users
```

**Direct Messaging**
- One-on-one chat
- Real-time messaging (WebSocket)
- Message history
- File sharing (EA files, configs, images)
- Typing indicators
- Read receipts
- Block users
- Report spam

**Collaborative Workspaces**
```yaml
Features:
  - Create shared workspace
  - Invite members
  - Shared EA library
  - Shared optimization results
  - Real-time collaboration
  - Activity log
  - Role-based permissions (Owner, Editor, Viewer)

Use Cases:
  - Trading teams
  - EA development groups
  - Learning communities
  - Research projects
```

#### 2.4 Reputation & Gamification

**Reputation Score (0-1000)**
```python
Points earned for:
  + EA upload (public): +10
  + Configuration shared: +5
  + Helpful comment (upvoted): +2
  + EA downloaded by others: +1 per download
  + Configuration used by others: +3 per use
  + Backtest shared: +2
  + Follower gained: +5
  + EA rated 5 stars: +20
  + Verified trader badge: +50

Points lost for:
  - Comment reported and removed: -20
  - EA removed for policy violation: -50
  - Account warning: -30
```

**Badges & Achievements**
```yaml
Contributor Badges:
  - "First Upload" - Upload first EA
  - "Popular EA" - 100+ downloads
  - "Viral Config" - 500+ uses of your configuration
  - "Helpful Trader" - 50+ upvotes on comments
  - "Influencer" - 1000+ followers

Performance Badges:
  - "Optimizer" - Complete 100 optimizations
  - "Backtester" - Run 1000 backtests
  - "Profitable" - Share config with >80% win rate
  - "Consistent" - 10 EAs with profit factor >2

Community Badges:
  - "Early Adopter" - Joined in first month
  - "Veteran" - 1 year on platform
  - "Legend" - 5 years on platform
  - "Team Player" - Active in 5+ workspaces

Special Badges:
  - "Verified Trader" - Verified live account
  - "Developer" - Contributed to platform code
  - "Moderator" - Trusted community moderator
```

**Leaderboards**
```yaml
Global Leaderboards:
  - Top Contributors (by reputation)
  - Most Downloaded EAs
  - Most Used Configurations
  - Top Optimizers (total optimizations)
  - Most Helpful (comment upvotes)

Weekly/Monthly:
  - Rising Stars
  - Most Active
  - Best New EA
  - Best Configuration

Category-Specific:
  - Best Forex EAs
  - Best Crypto EAs
  - Best Scalpers
  - Best Trend Followers
```

---

### 3. 📊 Admin Dashboard

#### 3.1 Dashboard Overview

**Key Metrics (Real-Time)**
```yaml
Users:
  - Total users
  - Active users (today, week, month)
  - New registrations (today, week)
  - User growth chart
  - Retention rate

Content:
  - Total EAs
  - Total configurations
  - Total backtests run
  - Total optimizations
  - Storage used

Activity:
  - Active sessions
  - API requests/minute
  - Background jobs queue
  - Server load (CPU, RAM, Disk)

Revenue (if applicable):
  - MRR (Monthly Recurring Revenue)
  - New subscriptions
  - Churn rate
  - LTV (Lifetime Value)
```

**Quick Actions**
- Create admin user
- Ban/unban user
- Feature/unfeature EA
- Send platform notification
- Clear cache
- Run database maintenance

#### 3.2 User Management

**User List View**
```yaml
Columns:
  - Avatar + Name
  - Email
  - Role
  - Status (Active, Banned, Pending)
  - Registration date
  - Last login
  - EAs count
  - Backtests count
  - Actions (Edit, Ban, Impersonate, Delete)

Filters:
  - Role
  - Status
  - Registration date range
  - Last login date range
  - Has uploaded EAs
  - Has subscription

Search:
  - By name, email, username
  - Fuzzy search

Bulk Actions:
  - Send email
  - Change role
  - Ban/unban
  - Export CSV
```

**User Detail View**
```yaml
Tabs:
  Overview:
    - Profile information
    - Account status
    - Subscription details
    - Login history (last 50)
    - IP addresses
    - Browser/device info

  Activity:
    - Timeline of all actions
    - EAs uploaded
    - Backtests run
    - Comments posted
    - Configurations shared

  Analytics:
    - Usage statistics
    - Engagement metrics
    - Storage usage
    - API usage

  Billing:
    - Subscription history
    - Payment methods
    - Invoices
    - Credits/refunds

  Security:
    - Failed login attempts
    - 2FA status
    - OAuth connections
    - Active sessions
    - Security alerts

  Moderation:
    - Reported content
    - Warnings issued
    - Ban history
    - Notes (admin-only)
```

**Admin Actions**
```python
# Available actions:
- Edit user profile
- Change role/permissions
- Reset password (send email)
- Ban user (with reason and duration)
- Unban user
- Delete user (soft delete, 30-day grace)
- Permanently delete user
- Impersonate user (for support)
- Send direct message
- Add internal notes
- Grant credits/refunds
- Override limits
```

#### 3.3 Content Moderation

**EA Review Queue**
```yaml
Pending EAs:
  - New EA uploads awaiting approval
  - Auto-flagged EAs (virus scan, suspicious code)
  - User-reported EAs

Review Interface:
  - EA details
  - Uploaded files (sandboxed preview)
  - VirusTotal scan results
  - Code analysis (if source provided)
  - User report reasons
  - Similar EAs detected

Actions:
  - Approve
  - Reject (with reason)
  - Request changes
  - Ban uploader
  - Add to safe list
```

**Comment Moderation**
```yaml
Reported Comments:
  - Comment text
  - Reporter and reason
  - Comment author
  - Context (EA, configuration)
  - Automatic analysis (toxicity score)

Actions:
  - Approve (ignore report)
  - Hide comment
  - Delete comment
  - Warn user
  - Ban user
  - Ban reporter (false report)
```

**Spam Detection**
```python
# ML-based spam detection:
- Repeated content
- External links
- Promotional language
- Bot-like behavior
- New accounts with high activity
- Geographic anomalies

# Actions:
- Auto-hide (pending review)
- Shadow ban (user doesn't know)
- Challenge (CAPTCHA)
- Require email verification
```

#### 3.4 Analytics & Reporting

**User Analytics**
```yaml
Engagement:
  - DAU (Daily Active Users)
  - WAU (Weekly Active Users)
  - MAU (Monthly Active Users)
  - Stickiness (DAU/MAU ratio)
  - Session duration
  - Pages per session

Acquisition:
  - New user signups
  - Signup sources (Google, Email, Referral)
  - Referral tracking
  - Campaign performance
  - Conversion funnel

Retention:
  - Cohort analysis
  - Churn rate
  - User lifecycle stages
  - Return frequency

Demographics:
  - Geographic distribution
  - Language preferences
  - Trading experience levels
  - Device types
```

**Content Analytics**
```yaml
EA Performance:
  - Most downloaded EAs
  - Highest rated EAs
  - Most profitable EAs (by backtest)
  - Category distribution
  - Upload trends

Configuration Usage:
  - Most used configurations
  - Configuration success rate
  - Fork tree analysis
  - Parameter popularity

Social Metrics:
  - Comments per day
  - Likes per day
  - Follower growth
  - Message volume
  - Workspace activity
```

**System Analytics**
```yaml
Performance:
  - API response times (P50, P95, P99)
  - Database query performance
  - Cache hit rates
  - Error rates
  - Background job processing times

Infrastructure:
  - Server uptime
  - CPU/RAM/Disk usage
  - Network traffic
  - Database size
  - Storage usage by user

Optimization Workers:
  - Active workers
  - Queue length
  - Jobs completed per hour
  - Average job duration
  - Worker failure rate
```

**Reports Generation**
```yaml
Built-in Reports:
  - Daily/Weekly/Monthly summaries (PDF)
  - User growth report
  - Revenue report
  - Content moderation report
  - System health report

Custom Reports:
  - Query builder interface
  - Save report templates
  - Schedule automatic generation
  - Export to CSV, Excel, PDF
  - Email delivery
```

#### 3.5 System Configuration

**Feature Flags**
```yaml
# Toggle features on/off without deployment
Features:
  - new_user_registration: true
  - google_oauth: true
  - direct_messaging: false
  - workspaces: true
  - paid_subscriptions: false
  - ea_marketplace: true
  - public_profiles: true

Per-Role Features:
  - pro_users_only: ['api_access', 'workspaces']
  - beta_features: ['ai_recommendations', 'advanced_charts']
```

**System Settings**
```yaml
Limits:
  - max_eas_per_user_free: 3
  - max_eas_per_user_pro: 999
  - max_file_size_mb: 50
  - max_backtest_per_day_free: 10
  - max_backtest_per_day_pro: 999
  - session_timeout_minutes: 60
  - password_min_length: 12

Rate Limits:
  - api_requests_per_minute: 100
  - login_attempts_before_lockout: 5
  - comment_posts_per_hour: 20

Email Settings:
  - smtp_host, port, username, password
  - from_email, from_name
  - email_templates

Notification Settings:
  - enable_email_notifications: true
  - enable_push_notifications: false
  - admin_alert_email: admin@example.com

Security:
  - require_email_verification: true
  - enforce_2fa_for_admins: true
  - password_expiry_days: 90
  - allowed_oauth_providers: ['google']
```

#### 3.6 Audit Logs

**Log Everything**
```yaml
User Actions:
  - Login/Logout
  - Profile changes
  - Password changes
  - EA uploads/deletions
  - Configuration shares
  - Permission changes

Admin Actions:
  - User management actions
  - Role changes
  - Bans/unbans
  - Content moderation
  - System configuration changes
  - Impersonation sessions

System Events:
  - Errors and exceptions
  - Security alerts
  - Performance issues
  - Deployment events
  - Database migrations
```

**Audit Log Interface**
```yaml
Columns:
  - Timestamp
  - Action type
  - User (who did it)
  - Target (what was affected)
  - Details (JSON)
  - IP address
  - Status (success/failure)

Filters:
  - Date range
  - Action type
  - User
  - IP address
  - Status

Search:
  - Full-text search in details

Export:
  - CSV, JSON
  - Send to SIEM system
```

---

## 🗄️ Database Schema Additions

### New Tables

**1. user_profiles**
```sql
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  -- Bio & social
  bio TEXT,
  website VARCHAR(500),
  twitter VARCHAR(100),
  linkedin VARCHAR(100),

  -- Trading info
  experience_level VARCHAR(20),
  preferred_markets JSONB DEFAULT '[]',
  risk_tolerance VARCHAR(20),
  trading_style VARCHAR(50),

  -- Privacy
  profile_visibility VARCHAR(20) DEFAULT 'public',
  show_activity BOOLEAN DEFAULT true,
  show_in_search BOOLEAN DEFAULT true,

  -- Stats
  reputation_score INTEGER DEFAULT 0,
  followers_count INTEGER DEFAULT 0,
  following_count INTEGER DEFAULT 0,
  eas_uploaded INTEGER DEFAULT 0,
  configs_shared INTEGER DEFAULT 0,

  -- Verification
  is_verified BOOLEAN DEFAULT false,
  verification_date TIMESTAMP,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**2. user_follows**
```sql
CREATE TABLE user_follows (
  id UUID PRIMARY KEY,
  follower_id UUID REFERENCES users(id) ON DELETE CASCADE,
  following_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(follower_id, following_id),
  CHECK (follower_id != following_id)
);
```

**3. ea_configurations**
```sql
CREATE TABLE ea_configurations (
  id UUID PRIMARY KEY,
  ea_version_id UUID REFERENCES ea_versions(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  name VARCHAR(255) NOT NULL,
  description TEXT,
  parameters JSONB NOT NULL,

  -- Trading context
  symbol VARCHAR(20),
  timeframe VARCHAR(10),
  backtest_from DATE,
  backtest_to DATE,

  -- Performance (if backtested)
  profit_factor NUMERIC(10, 4),
  win_rate NUMERIC(5, 2),
  total_trades INTEGER,
  net_profit NUMERIC(15, 2),
  max_drawdown NUMERIC(15, 2),

  -- Sharing
  visibility VARCHAR(20) DEFAULT 'private',
  is_featured BOOLEAN DEFAULT false,

  -- Engagement
  likes_count INTEGER DEFAULT 0,
  uses_count INTEGER DEFAULT 0,
  forks_count INTEGER DEFAULT 0,
  parent_config_id UUID REFERENCES ea_configurations(id),

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**4. comments**
```sql
CREATE TABLE comments (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  -- Polymorphic - can comment on EA, config, etc.
  commentable_type VARCHAR(50) NOT NULL,
  commentable_id UUID NOT NULL,

  content TEXT NOT NULL,
  parent_comment_id UUID REFERENCES comments(id) ON DELETE CASCADE,

  -- Moderation
  is_hidden BOOLEAN DEFAULT false,
  is_deleted BOOLEAN DEFAULT false,
  deleted_at TIMESTAMP,

  -- Engagement
  likes_count INTEGER DEFAULT 0,
  replies_count INTEGER DEFAULT 0,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  INDEX idx_commentable (commentable_type, commentable_id)
);
```

**5. likes**
```sql
CREATE TABLE likes (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  -- Polymorphic
  likeable_type VARCHAR(50) NOT NULL,
  likeable_id UUID NOT NULL,

  created_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(user_id, likeable_type, likeable_id)
);
```

**6. notifications**
```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  content TEXT,
  data JSONB,

  is_read BOOLEAN DEFAULT false,
  read_at TIMESTAMP,

  -- For action notifications (click to open)
  action_url VARCHAR(500),

  created_at TIMESTAMP DEFAULT NOW(),

  INDEX idx_user_unread (user_id, is_read, created_at)
);
```

**7. direct_messages**
```sql
CREATE TABLE direct_messages (
  id UUID PRIMARY KEY,
  sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
  recipient_id UUID REFERENCES users(id) ON DELETE CASCADE,

  content TEXT NOT NULL,
  attachments JSONB DEFAULT '[]',

  is_read BOOLEAN DEFAULT false,
  read_at TIMESTAMP,

  is_deleted_by_sender BOOLEAN DEFAULT false,
  is_deleted_by_recipient BOOLEAN DEFAULT false,

  created_at TIMESTAMP DEFAULT NOW(),

  INDEX idx_conversation (sender_id, recipient_id, created_at),
  INDEX idx_unread (recipient_id, is_read)
);
```

**8. workspaces**
```sql
CREATE TABLE workspaces (
  id UUID PRIMARY KEY,
  owner_id UUID REFERENCES users(id) ON DELETE CASCADE,

  name VARCHAR(255) NOT NULL,
  description TEXT,

  visibility VARCHAR(20) DEFAULT 'private',

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**9. workspace_members**
```sql
CREATE TABLE workspace_members (
  id UUID PRIMARY KEY,
  workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  role VARCHAR(20) DEFAULT 'viewer',  -- owner, editor, viewer

  joined_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(workspace_id, user_id)
);
```

**10. badges**
```sql
CREATE TABLE badges (
  id UUID PRIMARY KEY,

  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  icon VARCHAR(100),
  category VARCHAR(50),

  -- Criteria (for automatic awarding)
  criteria JSONB,

  created_at TIMESTAMP DEFAULT NOW()
);
```

**11. user_badges**
```sql
CREATE TABLE user_badges (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  badge_id UUID REFERENCES badges(id) ON DELETE CASCADE,

  earned_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(user_id, badge_id)
);
```

**12. audit_logs**
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY,

  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(50),
  resource_id UUID,

  details JSONB,

  ip_address VARCHAR(45),
  user_agent TEXT,

  status VARCHAR(20),  -- success, failure

  created_at TIMESTAMP DEFAULT NOW(),

  INDEX idx_user_action (user_id, action, created_at),
  INDEX idx_resource (resource_type, resource_id)
);
```

**13. oauth_connections**
```sql
CREATE TABLE oauth_connections (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  provider VARCHAR(50) NOT NULL,  -- google, github, etc.
  provider_user_id VARCHAR(255) NOT NULL,

  access_token TEXT,
  refresh_token TEXT,
  expires_at TIMESTAMP,

  profile_data JSONB,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  UNIQUE(provider, provider_user_id)
);
```

---

## 🔐 Güvenlik Gereksinimleri (Security Requirements)

### Authentication Security

1. **Password Requirements**
   - Minimum 12 characters
   - Must contain: uppercase, lowercase, number, special character
   - Cannot contain username or email
   - Check against common password lists (HIBP)
   - Password history (cannot reuse last 5 passwords)

2. **Session Management**
   - JWT tokens with 30-minute expiry
   - Refresh tokens with 7-day expiry
   - HttpOnly, Secure, SameSite cookies
   - CSRF protection
   - Concurrent session limits (max 5 devices)

3. **OAuth Security**
   - PKCE flow for OAuth 2.0
   - State parameter validation
   - Nonce for replay attack prevention
   - Token rotation
   - Revocation support

4. **Rate Limiting**
   ```yaml
   Login:
     - 5 attempts per IP per 15 minutes
     - Account lockout after 5 failures

   API:
     - 100 requests per minute (anonymous)
     - 1000 requests per minute (authenticated)
     - Burst: 20 requests

   Registration:
     - 3 registrations per IP per day
     - Email verification required
   ```

### Data Protection

1. **Encryption**
   - Data at rest: AES-256
   - Data in transit: TLS 1.3
   - Database: Transparent Data Encryption (TDE)
   - Backups: Encrypted with separate keys

2. **Sensitive Data Handling**
   - Passwords: Bcrypt (12 rounds)
   - Trading account passwords: AES-256 with per-user keys
   - API keys: Hashed, never logged
   - PII data: Encrypted fields

3. **GDPR Compliance**
   - Data export functionality
   - Right to deletion (30-day grace period)
   - Data retention policies
   - Cookie consent
   - Privacy policy

### Application Security

1. **Input Validation**
   - All user inputs sanitized
   - SQL injection prevention (parameterized queries)
   - XSS prevention (content security policy)
   - File upload validation (type, size, virus scan)

2. **Authorization**
   - Every API endpoint checks permissions
   - Resource-level authorization
   - Impersonation audit trail
   - Principle of least privilege

3. **Security Headers**
   ```
   Content-Security-Policy
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   X-XSS-Protection: 1; mode=block
   Strict-Transport-Security
   ```

4. **Monitoring & Alerts**
   - Failed login tracking
   - Unusual activity detection
   - Admin action alerts
   - Security event logging

---

## 📝 Implementation Tasks

### Phase 1: Core User Management (Week 1-2)

**Backend**
- [ ] Update User model with new fields
- [ ] Create UserProfile model and API
- [ ] Implement Google OAuth 2.0 flow
- [ ] Add 2FA support (TOTP)
- [ ] Create permissions middleware
- [ ] Implement RBAC system
- [ ] Create audit logging system

**Frontend**
- [ ] Build registration flow
- [ ] Build login page with Google button
- [ ] Create user profile page
- [ ] Build settings page
- [ ] Implement 2FA setup flow
- [ ] Create password reset flow

**Testing**
- [ ] Unit tests for auth logic
- [ ] Integration tests for OAuth
- [ ] E2E tests for registration/login

### Phase 2: Social Features (Week 3-4)

**Backend**
- [ ] Create EA configuration model
- [ ] Implement following system
- [ ] Build comment system
- [ ] Create like/favorite system
- [ ] Implement notification system
- [ ] Build direct messaging
- [ ] Create activity feed API

**Frontend**
- [ ] Build EA detail page with social features
- [ ] Create configuration sharing UI
- [ ] Implement follow button and followers list
- [ ] Build comment section
- [ ] Create notification center
- [ ] Build messaging interface
- [ ] Create activity feed

**Testing**
- [ ] Test comment threading
- [ ] Test notification delivery
- [ ] Test real-time messaging

### Phase 3: Admin Dashboard (Week 5-6)

**Backend**
- [ ] Create admin analytics API
- [ ] Build user management endpoints
- [ ] Implement content moderation API
- [ ] Create audit log viewer API
- [ ] Build reporting system
- [ ] Implement system configuration API

**Frontend**
- [ ] Build admin dashboard overview
- [ ] Create user management interface
- [ ] Build content moderation queue
- [ ] Create analytics dashboard
- [ ] Implement audit log viewer
- [ ] Build system settings page

**Testing**
- [ ] Test admin permissions
- [ ] Test user impersonation
- [ ] Test content moderation flows

### Phase 4: Advanced Features (Week 7-8)

**Backend**
- [ ] Implement workspace system
- [ ] Build reputation scoring
- [ ] Create badge system
- [ ] Implement search functionality (Elasticsearch)
- [ ] Build recommendation engine
- [ ] Add export/import features

**Frontend**
- [ ] Build workspace interface
- [ ] Create leaderboards
- [ ] Display badges on profiles
- [ ] Implement advanced search
- [ ] Build marketplace UI
- [ ] Create data export page

**Testing**
- [ ] Load testing for social features
- [ ] Performance testing for search
- [ ] Security penetration testing

### Phase 5: Polish & Launch (Week 9-10)

**Backend**
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation
- [ ] API versioning
- [ ] Monitoring setup
- [ ] Backup procedures

**Frontend**
- [ ] UX improvements
- [ ] Mobile responsiveness
- [ ] Accessibility (WCAG 2.1)
- [ ] Analytics integration
- [ ] Error tracking (Sentry)
- [ ] User onboarding flow

**Launch**
- [ ] Create admin user (turhanhamza@gmail.com)
- [ ] Seed initial data
- [ ] Beta testing
- [ ] Performance monitoring
- [ ] Go live!

---

## 🎯 Success Metrics

### User Engagement
- DAU/MAU ratio > 0.3
- Average session duration > 10 minutes
- Return rate > 60% (within 7 days)

### Social Features
- 30% of users follow at least 3 others
- Average 5 comments per EA
- 50% of users share at least 1 configuration

### Content Growth
- 100+ public EAs in first month
- 500+ configurations shared
- 10,000+ backtests run

### Admin Efficiency
- <5 minutes to handle content report
- <2 hours to resolve user issue
- 99.9% uptime

---

## 🚀 Future Enhancements (Phase 2)

1. **AI Features**
   - AI-powered EA recommendations
   - Automatic parameter optimization suggestions
   - Sentiment analysis on comments
   - Fraud detection

2. **Mobile Apps**
   - iOS app
   - Android app
   - Push notifications

3. **Marketplace**
   - Paid EA sales
   - Subscription models
   - Revenue sharing for creators
   - Escrow system

4. **Advanced Trading**
   - Live trading copy
   - Portfolio management
   - Risk management tools
   - Multi-account sync

5. **Integrations**
   - TradingView integration
   - Discord/Telegram bots
   - Webhook support
   - Zapier integration

---

**📧 Contact**
For questions about this PRD, contact the development team.
