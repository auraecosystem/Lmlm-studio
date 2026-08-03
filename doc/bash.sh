# Install
npm install --save-dev typedoc

# Build docs using package.json "exports" or "main" fields as entry points
npx typedoc
# Build docs using exports from src/index.ts
npx typedoc src/index.ts
# Generate docs for all TypeScript files under src
npx typedoc --entryPointStrategy Expand src
