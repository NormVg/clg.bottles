export type ItemType = 'link' | 'note' | 'media'

export interface ApiFolder {
  id: number
  parent_id: number | null
  name: string
  path: string
  created_at: string
}

export interface ApiMedia {
  id: number
  filename: string
  mime_type: string
  size: number
  created_at: string
}

export interface ApiItem {
  id: number
  folder_id: number | null
  type: ItemType
  title: string
  url: string | null
  note: string | null
  media: ApiMedia | null
  created_at: string
  updated_at: string
}

export interface ApiDirectory {
  path: string
  folder: ApiFolder | null
  folders: ApiFolder[]
  items: ApiItem[]
}

export interface ApiSearchResult {
  folders: ApiFolder[]
  items: ApiItem[]
}
