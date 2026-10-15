import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "../custom_components/air_traffic_merge/frontend",
    emptyOutDir: true,
    lib: { entry: "src/air-traffic-card.ts", formats: ["es"], fileName: () => "air-traffic-card.js" },
    rollupOptions: { output: { inlineDynamicImports: true } },
  },
  test: { environment: "jsdom", setupFiles: ["./tests/setup.ts"] },
});
