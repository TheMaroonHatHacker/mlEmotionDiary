FROM node:lts-bullseye-slim
RUN npm install -g pnpm
WORKDIR /frontend
COPY package.json .
COPY pnpm-lock.yaml .
RUN pnpm install
COPY . .
RUN pnpm build
CMD pnpm start


