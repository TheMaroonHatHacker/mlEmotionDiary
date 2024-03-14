# Install dependencies only when needed
FROM node:18.13.0-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install



FROM node:18.13.0-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
ADD . .
RUN pnpm build

FROM node:18.13.0-alpine AS runner
WORKDIR /app
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules


USER nextjs
EXPOSE 3000

CMD ["pnpm", "start"]
