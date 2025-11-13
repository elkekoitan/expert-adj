FROM node:20-alpine as base

WORKDIR /app

COPY frontend/package*.json ./

# Development stage
FROM base as development

RUN npm install

COPY frontend/ .

EXPOSE 3000

CMD ["npm", "run", "dev"]

# Production build stage
FROM base as builder

RUN npm ci --only=production

COPY frontend/ .

# Create public folder if it doesn't exist
RUN mkdir -p public

RUN npm run build

# Production stage
FROM node:20-alpine as production

WORKDIR /app

ENV NODE_ENV=production

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy Next.js standalone output
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Create public directory (Next.js may need it)
RUN mkdir -p ./public && chown -R nextjs:nodejs ./public

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
