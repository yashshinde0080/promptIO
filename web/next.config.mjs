/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return [
      {
        source: '/dashboard',
        destination: '/prompt-studio',
        permanent: false,
      },
      {
        source: '/evaluations',
        destination: '/prompt-studio',
        permanent: false,
      },
      {
        source: '/analytics',
        destination: '/prompt-studio',
        permanent: false,
      },
      {
        source: '/teams',
        destination: '/prompt-studio',
        permanent: false,
      },
      {
        source: '/settings',
        destination: '/prompt-studio',
        permanent: false,
      },
      {
        source: '/admin',
        destination: '/prompt-studio',
        permanent: false,
      },
    ];
  },
};

export default nextConfig;
