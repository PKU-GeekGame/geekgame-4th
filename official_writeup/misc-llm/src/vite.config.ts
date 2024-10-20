import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite';
import {compression} from 'vite-plugin-compression2';
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers';
import zlib from 'zlib';

export default defineConfig({
  build: {
    reportCompressedSize: false,
    minify: 'terser',
    terserOptions: {
        ecma: 2020,
        module: true,
        compress: {
            passes: 2,
        },
    },
  },
  esbuild: {
    legalComments: 'none',
  },
  plugins: [
    vue(),
    Components({
      resolvers: [
        AntDesignVueResolver({
          importStyle: false, // css in js
        }),
      ],
    }),
    compression({
      include: /\.*$/,
      exclude: /\.(png|jpg|jpeg|webp|mp3|ogg|webm)$/i,
      algorithm: 'brotliCompress',
      compressionOptions: {
          params: {
              [zlib.constants.BROTLI_PARAM_MODE]: zlib.constants.BROTLI_MODE_TEXT,
              [zlib.constants.BROTLI_PARAM_QUALITY]: zlib.constants.BROTLI_MAX_QUALITY,
          },
      },
    }),
    compression({
      include: /\.*$/,
      exclude: /\.(png|jpg|jpeg|webp|mp3|ogg|webm)$/i,
      algorithm: 'gzip',
      compressionOptions: {
        level: 9,
      },
    }),
  ],
})
