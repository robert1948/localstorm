// vite.plugins.cachebuster.js
export default function cacheBusterPlugin() {
  const timestamp = new Date().getTime();

  return {
    name: 'html-cache-buster',
    transformIndexHtml(html) {
      return html.replace(
        /(\.(png|jpg|jpeg|svg|ico|webp|gif|js|css|woff2?)(\?v=\d+)?)/g,
        (match) => `${match}?v=${timestamp}`
      );
    },
  };
}
