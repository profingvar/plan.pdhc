# Frontend bundle build

`agentation-loader.jsx` is the source of `../js/agentation.bundle.js`.

Rebuild after editing the .jsx:

```
cd planp
npx esbuild app/static/src/agentation-loader.jsx \
  --bundle --format=iife \
  --outfile=app/static/js/agentation.bundle.js \
  --loader:.js=jsx --loader:.jsx=jsx
```

Commit both the .jsx and the resulting bundle. No watch / CI step yet.
