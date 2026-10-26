export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} b`
  const units = ['kb', 'mb', 'gb']
  let value = bytes
  let unit = -1
  do {
    value /= 1024
    unit += 1
  } while (value >= 1024 && unit < units.length - 1)
  return `${value < 10 ? value.toFixed(1) : Math.round(value)} ${units[unit]}`
}
