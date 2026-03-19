const rawApiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const normalizedApiUrl =
  rawApiUrl.startsWith('http://') || rawApiUrl.startsWith('https://')
    ? rawApiUrl
    : `https://${rawApiUrl}`

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    domains: ['localhost'],
    unoptimized: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: normalizedApiUrl,
  },
}

module.exports = nextConfig
