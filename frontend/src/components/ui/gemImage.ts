import { emptyPixel, toProcessedGemSmoke } from '@paper-design/shaders'

export interface GemImage {
  image: HTMLImageElement
  objectUrl: string | null
}

function loadImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.crossOrigin = 'anonymous'
    image.onload = () => resolve(image)
    image.onerror = reject
    image.src = url
  })
}

/** Turn the logo into the processed image the gem shader expects. */
export async function processGemImage(rawUrl: string): Promise<GemImage> {
  if (!rawUrl) {
    return { image: await loadImage(emptyPixel), objectUrl: null }
  }

  let fetchUrl = rawUrl
  let tempUrl: string | null = null

  try {
    if (rawUrl.startsWith('/') || rawUrl.startsWith('http')) {
      try {
        const response = await fetch(rawUrl)
        if (response.ok) {
          const blob = await response.blob()
          const isSvg =
            rawUrl.includes('.svg') || response.headers.get('content-type')?.includes('svg')
          const finalBlob = isSvg ? new Blob([blob], { type: 'image/svg+xml' }) : blob
          tempUrl = URL.createObjectURL(finalBlob)
          fetchUrl = tempUrl
        }
      } catch {
        // fall back to the raw url
      }
    }

    const result = await toProcessedGemSmoke(fetchUrl)
    if (tempUrl) URL.revokeObjectURL(tempUrl)

    const objectUrl = URL.createObjectURL(result.pngBlob)
    return { image: await loadImage(objectUrl), objectUrl }
  } catch {
    if (tempUrl) URL.revokeObjectURL(tempUrl)
    return { image: await loadImage(emptyPixel), objectUrl: null }
  }
}
