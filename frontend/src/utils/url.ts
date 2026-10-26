/**
 * Postel's law for pasted text: guess whether it is a web url.
 * A bare word ("todo") stays a note; anything host-shaped
 * ("piedpiper.com/handbook", "https://...") becomes a link.
 */
export function normalizeUrl(input: string): string | null {
  const trimmed = input.trim()
  if (!trimmed || /\s/.test(trimmed)) return null

  const candidate = /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`
  try {
    const url = new URL(candidate)
    return url.hostname.includes('.') ? url.href : null
  } catch {
    return null
  }
}
