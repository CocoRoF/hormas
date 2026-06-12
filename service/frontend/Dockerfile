FROM node:21.2.0

RUN apt-get update && apt-get install -y git

WORKDIR /home/app/frontend

# Create new Next.js app (scaffold only)
RUN echo "Creating new Next.js app scaffolding..." && \
    npx create-next-app@15.3.2 . --no-typescript --use-npm --no-eslint --tailwind --src-dir --app --yes --import-alias @

# Remove default files (just in case)
RUN echo "Removing default src and public folders..." && \
    rm -rf ./src ./public && \
    rm -f package.json package-lock.json

EXPOSE 3000
